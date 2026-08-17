"""
============================================================================
DAILY_UPDATE.PY - Orquestrador da Fase 2 (roda via cron, uma vez por dia)
============================================================================
Fluxo:
  1. Busca a chuva dos ultimos dias (NASA POWER) para as 3 cidades e
     atualiza o cache local.
  2. Determina a safra ativa e o contrato do mes vigente (safra.py).
  3. Se hoje cai dentro de um mes de contrato (Set-Fev): projeta a chuva
     do mes (chuva_previsao.py) e reprecifica esse contrato para os 6
     strikes, usando as mesmas funcoes HBA/MC de cme_structurer_v2.py.
  4. Loga o resultado em monitor_diario_log.csv (uma linha por dia por
     cidade/strike) e atualiza a aba "Monitor Diario" do Excel.
  5. Contratos de meses ainda nao iniciados NAO sao alterados por este
     script - continuam com o preco da climatologia pura (cme_structurer_v2).

USO:
  python3 daily_update.py                  # roda para "hoje"
  python3 daily_update.py --data 2027-01-15  # roda para uma data especifica
                                               (util para reprocessar/testar)

AGENDAMENTO (crontab -e), rodar todo dia as 7h, depois da atualizacao das
8h da curva de juros nao ter dependencia entre os dois - qualquer ordem
funciona, mas sugestao de rodar o clima antes:
  0 7 * * * cd /caminho/para/o/projeto && /usr/bin/python3 daily_update.py >> logs/daily_update.log 2>&1
"""
import argparse
import sys
import traceback
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

import safra
import nasa_power_fetch
from cme_structurer_v2 import CIDADES, STRIKE_PCTS, TICK_RS_POR_MM, CAP_MM, UPLOADS, load_weather
from chuva_previsao import projetar_mes_ativo

BASE = Path(__file__).parent
LOG_CSV = BASE / 'monitor_diario_log.csv'
EXCEL_PATH = BASE / 'Derivativo_Precipitacao_Soja_MT.xlsx'

COLUNAS_CLIMA = ['data', 'ano', 'mes', 'dia', 'PRECTOTCORR']


def _carregar_historico(cidade: str) -> pd.DataFrame:
    """Historico decadal (1990-hoje) usado como base de anos analogos para o
    HBA/Monte Carlo - a API do NASA POWER so retorna alguns dias por chamada
    (ver nasa_power_fetch.atualizar_cache_diario), entao o cache diario
    sozinho nunca teria anos suficientes para o repricing. Este historico e
    combinado com o cache diario mais abaixo (ver _cache_completo)."""
    df = load_weather(UPLOADS / CIDADES[cidade])
    df['dia'] = df['data'].dt.day
    return df[COLUNAS_CLIMA]


def _cache_completo(cidade: str, df_api: pd.DataFrame) -> pd.DataFrame:
    """Combina o historico decadal com o cache diario da API (que tem
    prioridade em datas sobrepostas, por ser o dado mais recente)."""
    df_hist = _carregar_historico(cidade)
    combinado = pd.concat([df_hist, df_api[COLUNAS_CLIMA]], ignore_index=True)
    combinado = combinado.drop_duplicates(subset='data', keep='last').sort_values('data').reset_index(drop=True)
    return combinado


def _chuva_do_dia(df_diario: pd.DataFrame, data_ref: date, max_defasagem: int = 7):
    """Chuva do dia mais recente com dado consolidado no cache. A API do
    NASA POWER tem defasagem de consolidacao de ate ~3 dias (medido em
    producao: D-1 e D-2 costumam vir nulos, so D-3 vem preenchido) - por
    isso NAO assume que "ontem" (data_ref-1) esta disponivel, e sim procura
    para tras, dentro de uma janela de `max_defasagem` dias, o dia mais
    recente que ja tem valor. Retorna None se nenhum dia da janela tiver
    dado consolidado ainda."""
    inicio = pd.Timestamp(data_ref - timedelta(days=max_defasagem))
    fim = pd.Timestamp(data_ref)
    janela = df_diario[
        (df_diario['data'] >= inicio) & (df_diario['data'] < fim) & df_diario['PRECTOTCORR'].notna()
    ]
    if janela.empty:
        return None
    ultima = janela.sort_values('data').iloc[-1]
    return round(float(ultima['PRECTOTCORR']), 1)


def rodar(data_ref: date):
    print(f"\n{'='*70}\nDAILY UPDATE - {data_ref.isoformat()}\n{'='*70}")

    # --- 1. Atualiza cache de chuva (NASA POWER) ---
    caches = {}
    for cidade in CIDADES:
        try:
            df_c = nasa_power_fetch.atualizar_cache_diario(cidade)
            caches[cidade] = df_c
            print(f"[OK] {cidade}: cache atualizado, {len(df_c)} dias no total")
        except Exception as e:
            print(f"[ERRO] {cidade}: falha ao buscar NASA POWER - {e}")
            print("       (o repricing deste dia sera pulado para esta cidade)")
            caches[cidade] = None

    # --- 2. Safra e mes ativo ---
    safra_y = safra.get_safra_atual(data_ref)
    contratos = safra.get_contratos_da_safra(safra_y)
    mes_ativo = next(
        (c for c in contratos if c['ano_calendario'] == data_ref.year and c['mes_num'] == data_ref.month),
        None
    )

    if mes_ativo is None:
        print(f"\nHoje ({data_ref}) nao esta dentro de nenhum mes de contrato "
              f"(Set-Fev) da safra {safra.descricao_ciclo(safra_y)}.")
        print("Nada a reprecificar hoje - contratos futuros mantem o preco da climatologia pura.")
        return []

    print(f"\nSafra ativa: {safra.descricao_ciclo(safra_y)}")
    print(f"Mes de contrato vigente: {mes_ativo['mes_nome']}/{mes_ativo['ano_calendario']} "
          f"({mes_ativo['fase']})")

    anos_hist = safra.anos_historicos_elegiveis(safra_y, ano_min=1990)

    # --- 3. Projeta e reprecifica o mes ativo, por cidade e strike ---
    resultados = []
    for cidade in CIDADES:
        df_api = caches[cidade]
        if df_api is None or df_api.empty:
            continue
        try:
            df_c = _cache_completo(cidade, df_api)
        except FileNotFoundError as e:
            print(f"[ERRO] {cidade}: historico decadal nao encontrado ({e}) - repricing pulado")
            continue

        # media historica do mes (para os mesmos strikes % usados na v2)
        hist_mensal = df_c.groupby(['ano', 'mes'])['PRECTOTCORR'].sum().reset_index()
        media_mes = hist_mensal[
            (hist_mensal.mes == mes_ativo['mes_num']) & (hist_mensal.ano.isin(anos_hist))
        ]['PRECTOTCORR'].mean()

        for pct in STRIKE_PCTS:
            strike = media_mes * pct if pd.notna(media_mes) else None
            if strike is None:
                continue
            proj = projetar_mes_ativo(
                df_c, data_ref.year, mes_ativo['mes_num'], data_ref.day,
                anos_hist, strike, TICK_RS_POR_MM, CAP_MM
            )
            if proj is None:
                continue
            resultados.append({
                'data_execucao': data_ref.isoformat(),
                'cidade': cidade,
                'mes_contrato': mes_ativo['mes_nome'],
                'safra': f"{safra_y}/{safra_y+1}",
                'strike_pct': f"{int(pct*100)}%",
                'strike_mm': round(strike, 1),
                'chuva_do_dia_mm': _chuva_do_dia(df_c, data_ref),
                **proj,
            })

    if not resultados:
        print("\n[AVISO] Nenhum resultado calculado (falhas de rede em todas as cidades?)")
        return []

    df_result = pd.DataFrame(resultados)

    # --- 4a. Log historico (CSV, acumula uma linha por execucao) ---
    if LOG_CSV.exists():
        df_result.to_csv(LOG_CSV, mode='a', header=False, index=False)
    else:
        df_result.to_csv(LOG_CSV, index=False)
    print(f"\n[OK] Log atualizado: {LOG_CSV} (+{len(df_result)} linhas)")

    # --- 4b. Atualiza a aba Monitor Diario do Excel ---
    try:
        atualizar_excel_monitor(df_result, data_ref)
        print(f"[OK] Excel atualizado: {EXCEL_PATH}")
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar Excel: {e}")
        traceback.print_exc()

    # --- Resumo no console ---
    print(f"\nResumo (strike 50%, mes {mes_ativo['mes_nome']}):")
    resumo = df_result[df_result.strike_pct == '50%'][
        ['cidade', 'chuva_realizada_mm', 'dias_restantes', 'prob_acionamento_mc', 'premio_mc_bruto']
    ]
    print(resumo.to_string(index=False))

    return resultados


def atualizar_excel_monitor(df_result: pd.DataFrame, data_ref: date):
    """
    Acrescenta uma linha por cidade (strike 50%) na tabela "Monitor Diario"
    da aba Proximas Fases. NAO usa insert_rows() (o openpyxl tem bugs
    conhecidos de deslocamento de merged cells com insert_rows) - em vez
    disso, localiza e desfaz o merge da linha de nota manualmente, escreve
    os dados nas linhas livres, e reescreve a nota logo abaixo, remesclada.
    """
    from openpyxl.styles import Border, Side
    borda_fina = Border(*[Side(style='thin', color='BFBFBF')] * 4)

    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel nao encontrado em {EXCEL_PATH}")

    wb = load_workbook(EXCEL_PATH)
    ws = wb['Próximas Fases']

    df50 = df_result[df_result.strike_pct == '50%'].reset_index(drop=True)
    n_novas = len(df50)
    if n_novas == 0:
        wb.close()
        return

    # 1. localiza cabecalho "Data"
    header_row = None
    for row in ws.iter_rows(min_col=1, max_col=1):
        for cell in row:
            if cell.value == 'Data':
                header_row = cell.row
                break
        if header_row:
            break
    if header_row is None:
        raise ValueError('Cabecalho "Data" da tabela Monitor Diario nao encontrado')

    # 2. localiza a linha da nota ("Nota: na Fase 2...") e seu texto/merge atual
    nota_row, nota_texto, nota_range = None, None, None
    for row in ws.iter_rows(min_col=1, max_col=1):
        for cell in row:
            if cell.value and str(cell.value).startswith('Nota: na Fase 2'):
                nota_row = cell.row
                nota_texto = cell.value
    if nota_row is None:
        raise ValueError('Linha de nota do Monitor Diario nao encontrada')
    for mc in list(ws.merged_cells.ranges):
        if mc.min_row <= nota_row <= mc.max_row:
            nota_range = mc
            ws.unmerge_cells(str(mc))
            break

    # 3. primeira linha de dados livre (pula a linha "(ex)" se ainda for placeholder)
    primeira_linha_dados = header_row + 1
    valor_atual = ws.cell(row=primeira_linha_dados, column=1).value
    if valor_atual is None or str(valor_atual).startswith('(ex)'):
        linha_escrita_inicial = primeira_linha_dados
    else:
        # avanca ate a primeira linha vazia ou ate a antiga posicao da nota
        r = primeira_linha_dados
        while ws.cell(row=r, column=1).value not in (None, '') and r < nota_row:
            r += 1
        linha_escrita_inicial = r

    NUM_FORMATS = {3: '#,##0.0', 4: '#,##0.0', 5: '#,##0.0', 6: '#,##0.0', 7: 'R$ #,##0.00', 8: '0.0%'}

    linha_alvo = linha_escrita_inicial
    for _, r in df50.iterrows():
        chuva_real = round(float(r['chuva_realizada_mm']), 1)
        strike_mm = round(float(r['strike_mm']), 1)
        deficit = round(strike_mm - chuva_real, 1) if chuva_real < strike_mm else 0.0
        valores = [
            data_ref.strftime('%d/%m/%Y'), r['cidade'], r.get('chuva_do_dia_mm'),
            chuva_real, strike_mm, deficit,
            round(float(r['premio_mc_bruto']), 2), round(float(r['prob_acionamento_mc']), 4),
        ]
        for col, val in enumerate(valores, start=1):
            c = ws.cell(row=linha_alvo, column=col)
            c.value = val
            c.font = Font(name='Arial', size=9)
            c.alignment = Alignment(horizontal='center', vertical='center')
            c.border = borda_fina
            if col in NUM_FORMATS:
                c.number_format = NUM_FORMATS[col]
        linha_alvo += 1

    # 4. reescreve a nota logo abaixo da ultima linha escrita (com 1 linha de respiro)
    nova_linha_nota = max(linha_alvo + 1, nota_row)
    # limpa qualquer resto de conteudo antigo entre a ultima linha escrita e a nova posicao da nota
    for r in range(linha_alvo, nova_linha_nota):
        for c in range(1, 9):
            ws.cell(row=r, column=c).value = None

    ws.merge_cells(start_row=nova_linha_nota, start_column=1, end_row=nova_linha_nota, end_column=8)
    nota_cell = ws.cell(row=nova_linha_nota, column=1)
    nota_cell.value = nota_texto
    nota_cell.font = Font(name='Arial', size=8, italic=True, color='808080')
    nota_cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws.row_dimensions[nova_linha_nota].height = 28

    wb.save(EXCEL_PATH)
    wb.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default=None,
                        help='Data de referencia (AAAA-MM-DD). Default: hoje.')
    args = parser.parse_args()

    data_ref = datetime.strptime(args.data, '%Y-%m-%d').date() if args.data else date.today()

    try:
        rodar(data_ref)
    except Exception as e:
        print(f"\n[ERRO FATAL] {e}")
        traceback.print_exc()
        sys.exit(1)
