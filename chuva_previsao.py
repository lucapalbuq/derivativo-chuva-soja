"""
============================================================================
PROJEÇÃO DE CHUVA - MÊS EM CURSO (Fase 2)
============================================================================
Para o mes do contrato ATIVO (o mes corrente dentro da safra vigente), a
chuva total do mes ainda nao e conhecida - parte ja caiu (realizada),
parte ainda vai cair (dias restantes). Este modulo projeta a distribuicao
do TOTAL do mes combinando:

  chuva_projetada = chuva_realizada_ate_hoje (FIXA, conhecida)
                   + chuva_dias_restantes (distribuicao, incerta)

Metodologia da parte incerta (climatological forecast):
  Para cada ano historico elegivel, calcula-se quanto choveu nos MESMOS
  dias restantes daquele mes naquele ano (ex: se hoje e 15/jan, olha
  16/jan a 31/jan de cada ano historico). Isso gera uma amostra empirica
  de "chuva possivel nos dias que faltam", alinhada ao calendario.
  Somando a chuva ja realizada (constante) a cada um desses analogos
  historicos, obtem-se um histórico CONDICIONAL do total do mes - que e
  entao alimentado SEM NENHUMA MODIFICACAO nas funcoes hba_put() e
  monte_carlo_put() ja existentes e validadas em cme_structurer_v2.py.

Isso e deliberado: nao redesenha a precificacao, so desloca o insumo.

LIMITACAO DOCUMENTADA: este e um "climatological forecast" - assume que a
distribuicao de chuva nos dias restantes segue o padrao historico do
calendario, SEM usar nenhuma previsao meteorologica real (ex: modelo
numerico de previsao do tempo, que teria skill preditivo maior nos
primeiros 5-10 dias a frente). Nao captura eventos anomalos em curso
(ex: uma seca ja identificada por orgaos meteorologicos como excepcional
para o mes). Adequado como baseline; pode ser refinado combinando com
previsao meteorologica de curto prazo quando disponivel.
"""
import pandas as pd
import numpy as np
import calendar
from datetime import date

from cme_structurer_v2 import hba_put, monte_carlo_put, TICK_RS_POR_MM, CAP_MM


def ultimo_dia_do_mes(ano: int, mes: int) -> int:
    return calendar.monthrange(ano, mes)[1]


def chuva_realizada_ate_hoje(df_diario: pd.DataFrame, ano: int, mes: int, dia_atual: int) -> float:
    """Soma a chuva do dia 1 ate dia_atual (inclusive) do mes/ano informado."""
    janela = df_diario[
        (df_diario['ano'] == ano) & (df_diario['mes'] == mes) & (df_diario['dia'] <= dia_atual)
    ]
    return janela['PRECTOTCORR'].sum()


def chuva_resto_do_mes_por_ano_historico(df_diario: pd.DataFrame, mes: int, dia_atual: int,
                                          anos_historicos: list) -> np.ndarray:
    """
    Para cada ano historico, soma a chuva dos dias (dia_atual+1) ate o
    fim do mes NAQUELE ano (respeitando fev de ano bissexto etc.).
    Retorna um array com um valor por ano historico elegivel.
    """
    valores = []
    for ano in anos_historicos:
        ultimo_dia = ultimo_dia_do_mes(ano, mes)
        if dia_atual >= ultimo_dia:
            continue  # mes daquele ano nao tem dias "restantes" alem do atual
        janela = df_diario[
            (df_diario['ano'] == ano) & (df_diario['mes'] == mes) &
            (df_diario['dia'] > dia_atual) & (df_diario['dia'] <= ultimo_dia)
        ]
        if janela['PRECTOTCORR'].isna().all() or len(janela) == 0:
            continue
        valores.append(janela['PRECTOTCORR'].sum())
    return np.array(valores)


def projetar_mes_ativo(df_diario: pd.DataFrame, ano_atual: int, mes: int, dia_atual: int,
                        anos_historicos: list, strike_mm: float,
                        tick=TICK_RS_POR_MM, cap=CAP_MM) -> dict:
    """
    Funcao principal: projeta a distribuicao do total do mes ativo e
    reprecifica o contrato daquele strike usando HBA + Monte Carlo,
    reaproveitando as funcoes ja existentes (nenhuma alteracao nelas).
    """
    realizado = chuva_realizada_ate_hoje(df_diario, ano_atual, mes, dia_atual)
    resto_por_ano = chuva_resto_do_mes_por_ano_historico(df_diario, mes, dia_atual, anos_historicos)

    if len(resto_por_ano) < 5:
        return None  # historico insuficiente para esse dia/mes

    # historico CONDICIONAL do total do mes: realizado (fixo) + resto (variavel por ano)
    # convertido para pd.Series pois monte_carlo_put() (cme_structurer_v2.py) espera
    # esse tipo - ajuste no ponto de chamada, sem modificar a funcao original.
    historico_condicional = pd.Series(realizado + resto_por_ano)

    hba = hba_put(historico_condicional, strike_mm, tick, cap)
    mc = monte_carlo_put(historico_condicional, strike_mm, tick, cap)

    # percentis do TOTAL projetado do mes (nao so do payoff) - para visualizar incerteza
    percentis_total = {
        'P10': np.percentile(historico_condicional, 10),
        'P25': np.percentile(historico_condicional, 25),
        'P50_mediana': np.percentile(historico_condicional, 50),
        'P75': np.percentile(historico_condicional, 75),
        'P90': np.percentile(historico_condicional, 90),
    }

    return {
        'ano_atual': ano_atual, 'mes': mes, 'dia_atual': dia_atual,
        'dias_restantes': ultimo_dia_do_mes(ano_atual, mes) - dia_atual,
        'chuva_realizada_mm': round(realizado, 1),
        'n_anos_analogos': len(resto_por_ano),
        'strike_mm': strike_mm,
        'percentis_chuva_total_projetada': {k: round(v, 1) for k, v in percentis_total.items()},
        'prob_acionamento_hist': hba['prob_acionamento'],
        'prob_acionamento_mc': mc['prob_acionamento_mc'],
        'premio_hba_bruto': round(hba['premio_hba_bruto'], 2),
        'premio_mc_bruto': round(mc['premio_mc_bruto'], 2),
        'VaR95_RS': round(mc['VaR_95'], 2),
    }


if __name__ == '__main__':
    # TESTE COM DADOS REAIS: simula "hoje" = 15/jan/2020 (dado historico ja
    # conhecido) para provar que a logica de projecao funciona antes de
    # usar em producao com dado ao vivo.
    from cme_structurer_v2 import load_weather, CIDADES, UPLOADS

    df = load_weather(UPLOADS / CIDADES['Sorriso'])
    df['dia'] = df['data'].dt.day

    print("=" * 70)
    print("TESTE DE VALIDACAO - projecao de chuva com dado historico real")
    print("Simulando 'hoje' = 15/01/2020 (Sorriso) - o restante de jan/2020 e conhecido,")
    print("entao podemos comparar a projecao com o que REALMENTE aconteceu.")
    print("=" * 70)

    anos_hist = [a for a in range(1990, 2020)]  # exclui 2020 (o "ano corrente" do teste)
    strike_teste = 132.0  # ~50% da media historica de janeiro em Sorriso

    resultado = projetar_mes_ativo(df, 2020, 1, 15, anos_hist, strike_teste)
    print(f"\nChuva realizada até 15/jan/2020: {resultado['chuva_realizada_mm']} mm")
    print(f"Anos históricos usados como análogo: {resultado['n_anos_analogos']}")
    print(f"Percentis da chuva TOTAL projetada para jan/2020:")
    for k, v in resultado['percentis_chuva_total_projetada'].items():
        print(f"  {k}: {v} mm")
    print(f"Prob. acionamento (MC): {resultado['prob_acionamento_mc']:.1%}")
    print(f"Prêmio MC (bruto, sem desconto/carga): R$ {resultado['premio_mc_bruto']:.2f}")

    # comparar com o que realmente choveu em jan/2020 inteiro (validacao)
    real_jan2020 = df[(df.ano == 2020) & (df.mes == 1)]['PRECTOTCORR'].sum()
    print(f"\n>>> VALIDAÇÃO: chuva REAL de janeiro/2020 completo = {real_jan2020:.1f} mm")
    p10 = resultado['percentis_chuva_total_projetada']['P10']
    p90 = resultado['percentis_chuva_total_projetada']['P90']
    dentro_do_intervalo = p10 <= real_jan2020 <= p90
    print(f">>> Estava dentro do intervalo P10-P90 projetado ({p10}-{p90}mm)? {dentro_do_intervalo}")
