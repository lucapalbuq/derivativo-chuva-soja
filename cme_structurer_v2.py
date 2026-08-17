"""
============================================================================
CME-STYLE RAINFALL PUT STRUCTURER v2 - SOJA MEDIO-NORTE MT
============================================================================
Evolucao do cme_structurer.py (v1) com 4 melhorias:
  1. Taxa de desconto como INPUT explicito + curva de juros futura (ETTJ
     ANBIMA) descontando cada contrato pelo seu proprio vencimento, nao
     por uma taxa spot unica.
  2. (graficos corrigidos no gerador de Excel, nao neste modulo)
  3. Modelo de safra rolante: ciclo Marco Y - Fevereiro Y+1, com rollover
     automatico da base historica em Marco.
  4. Estrutura pronta para repricing diario (funcao reprecificar_com_nova_chuva).

Mantem a metodologia de precificacao da v1 (HBA + Monte Carlo Gamma).
"""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from datetime import date
import warnings
warnings.filterwarnings('ignore')

import curva_juros
import safra

np.random.seed(42)
BASE = Path(__file__).parent
UPLOADS = Path(__file__).parent / 'uploads'

# ============================================================================
# PARAMETROS DO PRODUTO (contract spec - INPUTS explicitos e editaveis)
# ============================================================================
TICK_RS_POR_MM = 150.0        # R$ por mm de deficit (contract unit / tick value)
CAP_MM = 60.0                 # payoff maximo em mm de deficit
CARGA_RISCO = 0.20            # risk loading sobre o payoff esperado (markup do vendedor)
N_SIM = 50000                 # simulacoes Monte Carlo

# --- TAXA DE DESCONTO: agora um INPUT, nao mais hardcoded no meio do codigo ---
# Fonte: Banco Central do Brasil / Copom, reuniao de 05-06/08/2026.
# Usada como FALLBACK caso a curva ETTJ nao esteja disponivel por algum motivo;
# o calculo principal usa a curva de juros futura (ver curva_juros.py).
SELIC_ATUAL = 0.1400          # 14,00% a.a. (corrigido - valor anterior de 10,75% estava desatualizado)
USAR_CURVA_FUTURA = True      # se False, usa SELIC_ATUAL flat para todos os vencimentos (modo simplificado)

STRIKE_PCTS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80]

CIDADES = {
    'Sorriso': 'POWER_NASA_Sorriso.csv',
    'Sinop': 'POWER_NASA_Sinop.csv',
    'Lucas do Rio Verde': 'POWER_NASA_Lucas_Do_RV.csv',
}


# ============================================================================
# 1. CARREGAR CHUVA MENSAL HISTORICA POR CIDADE
# ============================================================================
def load_weather(path):
    with open(path) as f:
        lines = f.readlines()
    h = next(i for i, l in enumerate(lines) if l.startswith('YEAR,DOY'))
    df = pd.read_csv(path, skiprows=h).replace(-999, np.nan)
    df['data'] = pd.to_datetime(df['YEAR'].astype(str), format='%Y') + pd.to_timedelta(df['DOY'] - 1, unit='D')
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    return df


def chuva_mensal(df):
    m = df.groupby(['ano', 'mes'])['PRECTOTCORR'].sum().reset_index()
    m.columns = ['ano', 'mes', 'chuva_mm']
    return m


# ============================================================================
# 2. HBA e MONTE CARLO (identicos a v1 - metodologia ja validada)
# ============================================================================
def hba_put(historico_mm, strike_mm, tick, cap):
    deficit = np.minimum(np.maximum(0, strike_mm - historico_mm), cap)
    payoffs = tick * deficit
    return {
        'premio_hba_bruto': payoffs.mean(),
        'prob_acionamento': (deficit > 0).mean(),
    }


def monte_carlo_put(historico_mm, strike_mm, tick, cap, n_sim=N_SIM):
    dados = historico_mm[historico_mm >= 0].values
    frac_zero = (dados < 1).mean()
    if frac_zero > 0.15:
        molhados = dados[dados >= 1]
        if len(molhados) < 5:
            sim = np.random.choice(dados, n_sim)
        else:
            a, loc, scale = stats.gamma.fit(molhados, floc=0)
            secos = np.random.rand(n_sim) < frac_zero
            sim = np.where(secos, 0, stats.gamma.rvs(a, loc=0, scale=scale, size=n_sim))
    else:
        a, loc, scale = stats.gamma.fit(dados, floc=0)
        sim = stats.gamma.rvs(a, loc=0, scale=scale, size=n_sim)
    sim = np.maximum(0, sim)
    deficit = np.minimum(np.maximum(0, strike_mm - sim), cap)
    payoffs = tick * deficit
    return {
        'premio_mc_bruto': payoffs.mean(),
        'prob_acionamento_mc': (deficit > 0).mean(),
        'payoff_p95_mc': np.percentile(payoffs, 95),
        'payoff_p99_mc': np.percentile(payoffs, 99),
        'VaR_95': np.percentile(payoffs, 95),
    }


# ============================================================================
# 3. PRECIFICACAO COM DESCONTO POR VENCIMENTO ESPECIFICO (a mudanca central)
# ============================================================================
def premio_comercial(payoff_esperado, data_ref, data_liquidacao):
    """
    Premio = Payoff Esperado x (1 + carga) x fator de desconto.
    O fator de desconto usa a taxa da ETTJ ESPECIFICA para o prazo entre
    data_ref (hoje) e data_liquidacao (vencimento daquele contrato) - nao
    uma taxa unica para todos os meses, como na v1.
    """
    if USAR_CURVA_FUTURA:
        df_desconto = curva_juros.fator_desconto(data_ref, data_liquidacao)
    else:
        dias = (data_liquidacao - data_ref).days
        df_desconto = 1 / (1 + SELIC_ATUAL) ** (dias / 365)
    return payoff_esperado * (1 + CARGA_RISCO) * df_desconto, df_desconto


# ============================================================================
# 4. CONSTRUIR A STRIP DA SAFRA VIGENTE (com rolagem automatica)
# ============================================================================
def construir_strip(data_ref: date = None):
    if data_ref is None:
        data_ref = date.today()

    safra_y = safra.get_safra_atual(data_ref)
    contratos_safra = safra.get_contratos_da_safra(safra_y)
    anos_hist = safra.anos_historicos_elegiveis(safra_y, ano_min=1990)

    linhas = []
    dados_hist = {}

    for cidade, arquivo in CIDADES.items():
        df = load_weather(UPLOADS / arquivo)
        cm = chuva_mensal(df)
        # filtra a base historica para incluir apenas safras completas
        # (exclui a safra em curso, conforme regra de rolagem em Marco)
        cm_hist = cm[cm['ano'].isin(anos_hist)]

        for c in contratos_safra:
            hist = cm_hist[cm_hist.mes == c['mes_num']]['chuva_mm']
            hist = hist[hist.notna()]
            if len(hist) < 5:
                continue
            media_mes = hist.mean()
            dados_hist[(cidade, c['mes_nome'])] = hist.values

            for pct in STRIKE_PCTS:
                strike = media_mes * pct
                hba = hba_put(hist, strike, TICK_RS_POR_MM, CAP_MM)
                mc = monte_carlo_put(hist, strike, TICK_RS_POR_MM, CAP_MM)

                premio_hba, df_desc_hba = premio_comercial(
                    hba['premio_hba_bruto'], data_ref, c['data_liquidacao'])
                premio_mc, df_desc_mc = premio_comercial(
                    mc['premio_mc_bruto'], data_ref, c['data_liquidacao'])

                dias_uteis_venc = curva_juros.dias_uteis_entre(data_ref, c['data_liquidacao'])
                taxa_usada = curva_juros.taxa_anual_para_prazo(dias_uteis_venc) if USAR_CURVA_FUTURA else SELIC_ATUAL * 100

                linhas.append({
                    'Safra': f"{safra_y}/{safra_y+1}",
                    'Cidade': cidade,
                    'Mes': c['mes_nome'],
                    'Mes_Num': c['mes_num'],
                    'Ano_Calendario': c['ano_calendario'],
                    'Fase_Fenologica': c['fase'],
                    'Data_Liquidacao': c['data_liquidacao'].isoformat(),
                    'Dias_Uteis_Vencimento': dias_uteis_venc,
                    'Taxa_Juros_Usada_pct': round(taxa_usada, 4),
                    'Chuva_Media_Hist_mm': round(media_mes, 1),
                    'N_Anos_Historico': len(hist),
                    'Strike_Pct': f"{int(pct*100)}%",
                    'Strike_mm': round(strike, 1),
                    'Prob_Acionamento_Hist': round(hba['prob_acionamento'], 3),
                    'Prob_Acionamento_MC': round(mc['prob_acionamento_mc'], 3),
                    'Premio_HBA_RS': round(premio_hba, 2),
                    'Premio_MC_RS': round(premio_mc, 2),
                    'Premio_Medio_RS': round((premio_hba + premio_mc) / 2, 2),
                    'Payoff_Max_RS': round(CAP_MM * TICK_RS_POR_MM, 2),
                    'VaR95_Vendedor_RS': round(mc['VaR_95'], 2),
                    'Payoff_P99_RS': round(mc['payoff_p99_mc'], 2),
                })

    return pd.DataFrame(linhas), dados_hist, safra_y, data_ref


# ============================================================================
# 5. REPRICING DIARIO (chamado quando novos dados de chuva chegam)
# ============================================================================
def reprecificar_com_nova_chuva(data_ref: date = None):
    """
    Ponto de entrada para o repricing diario (Fase 2/4). Simplesmente
    rechama construir_strip() com a data de referencia atual - como os
    arquivos CSV de clima sao lidos do disco a cada chamada, um novo
    dado de chuva (arquivo atualizado) e uma nova data de referencia
    (para a curva de juros e o calculo de dias uteis ate o vencimento)
    automaticamente produzem um novo preco.

    Ver README_ATUALIZACAO_DIARIA.md para o fluxo operacional completo
    de como os arquivos de clima e a curva de juros sao atualizados.
    """
    return construir_strip(data_ref)


# ============================================================================
# EXECUCAO
# ============================================================================
if __name__ == '__main__':
    print("=" * 70)
    print("CME-STYLE RAINFALL PUT STRUCTURER v2 - SOJA MT")
    print("=" * 70)

    hoje = date(2026, 8, 13)  # data de referencia desta execucao
    strip, dados_hist, safra_y, data_ref = construir_strip(hoje)

    strip.to_csv(BASE / 'strip_precificacao_v2.csv', index=False)
    hist_rows = []
    for (cidade, mes), vals in dados_hist.items():
        for v in vals:
            hist_rows.append({'Cidade': cidade, 'Mes': mes, 'Chuva_mm': v})
    pd.DataFrame(hist_rows).to_csv(BASE / 'historico_chuva_mensal_v2.csv', index=False)

    print(f"\nData de referência (hoje): {hoje}")
    print(f"Safra ativa: {safra.descricao_ciclo(safra_y)}")
    print(f"Anos históricos usados no HBA/MC: {safra.anos_historicos_elegiveis(safra_y)[0]}"
          f"-{safra.anos_historicos_elegiveis(safra_y)[-1]} ({len(safra.anos_historicos_elegiveis(safra_y))} anos)")
    print(f"\nTick: R$ {TICK_RS_POR_MM:.0f}/mm | Cap: {CAP_MM:.0f}mm | Carga de risco: {CARGA_RISCO*100:.0f}%")
    print(f"Modo de desconto: {'Curva ETTJ (ANBIMA, ref. ' + curva_juros.ETTJ_DATA_REF.isoformat() + ')' if USAR_CURVA_FUTURA else f'Selic flat {SELIC_ATUAL*100:.2f}%'}")
    print(f"\nTotal de contratos precificados: {len(strip)}")

    print("\n" + "=" * 70)
    print("TAXA DE JUROS USADA POR CONTRATO (Sorriso, strike 50%) - a diferença-chave vs v1")
    print("=" * 70)
    ex = strip[(strip.Cidade == 'Sorriso') & (strip.Strike_Pct == '50%')][
        ['Mes', 'Ano_Calendario', 'Data_Liquidacao', 'Dias_Uteis_Vencimento', 'Taxa_Juros_Usada_pct', 'Premio_Medio_RS']]
    print(ex.to_string(index=False))
