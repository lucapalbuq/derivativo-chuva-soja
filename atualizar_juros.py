"""
============================================================================
ATUALIZAR_JUROS.PY - Atualizacao diaria da curva ETTJ + repricing completo
============================================================================
Fluxo:
  1. Busca a curva ETTJ mais recente da ANBIMA (URL estatica, sempre
     retorna o ultimo pregao publicado).
  2. Atualiza o cache local (curva_juros.py / ettj_cache.json).
  3. Reprecifica TODOS os contratos (cme_structurer_v2.construir_strip),
     que automaticamente usa a curva nova por causa do cache.
  4. Atualiza o Excel EM LUGAR (sem regenerar a planilha do zero, para
     nao apagar o historico acumulado pelo daily_update.py na aba
     Monitor Diario): sobrescreve os valores nas tabelas "Cadeia de
     Strikes" e nas matrizes de cada aba de cidade.

Pensado para rodar dentro do MESMO job diario que ja atualiza a chuva
(daily_update.py) - ver instrucoes no final deste arquivo para integrar.

USO:
  python3 atualizar_juros.py
"""
import sys
import traceback
from datetime import date
from pathlib import Path

import requests
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

import curva_juros
import cme_structurer_v2 as motor

BASE = Path(__file__).parent
EXCEL_PATH = BASE / 'Derivativo_Precipitacao_Soja_MT.xlsx'
ANBIMA_URL = 'https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp'

MESES_ORDEM = ['Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Janeiro', 'Fevereiro']
STRIKES_ORDEM = ['30%', '40%', '50%', '60%', '70%', '80%']


def buscar_curva_anbima(timeout=20) -> str:
    resp = requests.get(ANBIMA_URL, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = 'latin-1'  # a ANBIMA serve o CSV em latin-1 (acentos ficam corretos so assim)
    return resp.text


def atualizar_cadeia_de_strikes(ws, strip: pd.DataFrame):
    """Sobrescreve os valores da tabela 'Cadeia de Strikes' EM LUGAR,
    casando cada linha existente por (Cidade, Mes, Strike_Pct) - nao
    insere nem remove linhas, so atualiza os numeros."""
    header_row = None
    for row in ws.iter_rows(min_col=1, max_col=2):
        c1, c2 = row[0], row[1]
        if c1.value == 'Cidade' and c2.value == 'Mês':
            header_row = c1.row
            break
    if header_row is None:
        raise ValueError('Cabecalho da Cadeia de Strikes nao encontrado')

    lookup = {}
    for _, r in strip.iterrows():
        lookup[(r['Cidade'], r['Mes'], r['Strike_Pct'])] = r

    COL_MAP = {
        3: 'Data_Liquidacao', 5: 'Taxa_Juros_Usada_pct',
        9: 'Prob_Acionamento_Hist', 10: 'Prob_Acionamento_MC',
        11: 'Premio_HBA_RS', 12: 'Premio_MC_RS', 13: 'Premio_Medio_RS',
        15: 'VaR95_Vendedor_RS', 16: 'Payoff_P99_RS',
    }

    n_atualizadas = 0
    r_atual = header_row + 1
    while True:
        cidade = ws.cell(row=r_atual, column=1).value
        mes = ws.cell(row=r_atual, column=2).value
        strike_pct = ws.cell(row=r_atual, column=7).value
        if cidade is None:
            break
        chave = (cidade, mes, strike_pct)
        if chave in lookup:
            row_novo = lookup[chave]
            for col, campo in COL_MAP.items():
                c = ws.cell(row=r_atual, column=col)
                if campo == 'Data_Liquidacao':
                    c.value = row_novo[campo]
                elif campo == 'Taxa_Juros_Usada_pct':
                    c.value = round(float(row_novo[campo]), 4)
                elif 'RS' in campo:
                    c.value = round(float(row_novo[campo]), 2)
                else:
                    c.value = round(float(row_novo[campo]), 4)
            n_atualizadas += 1
        r_atual += 1
    return n_atualizadas


def atualizar_matriz_cidade(ws, strip_cidade: pd.DataFrame, cidade: str):
    """Sobrescreve as duas matrizes (premio medio e probabilidade) da
    aba de uma cidade, celula por celula, sem tocar nos graficos (que
    ja referenciam essas mesmas celulas e atualizam sozinhos)."""
    lookup_premio = {}
    lookup_prob = {}
    for _, r in strip_cidade.iterrows():
        lookup_premio[(r['Strike_Pct'], r['Mes'])] = round(float(r['Premio_Medio_RS']), 2)
        lookup_prob[(r['Strike_Pct'], r['Mes'])] = round(float(r['Prob_Acionamento_MC']), 4)

    # localiza a matriz de premio (cabecalho "Strike" na coluna A, meses na linha)
    header_premio_row = None
    for row in ws.iter_rows(min_col=1, max_col=1):
        for cell in row:
            if cell.value == 'Strike':
                header_premio_row = cell.row
                break
        if header_premio_row:
            break
    if header_premio_row is None:
        raise ValueError(f'Matriz de premio nao encontrada na aba {cidade}')

    for i, strike in enumerate(STRIKES_ORDEM, start=1):
        rr = header_premio_row + i
        for j, mes in enumerate(MESES_ORDEM, start=2):
            chave = (strike, mes)
            if chave in lookup_premio:
                ws.cell(row=rr, column=j).value = lookup_premio[chave]

    # localiza a segunda ocorrencia de "Strike" (matriz de probabilidade)
    header_prob_row = None
    for row in ws.iter_rows(min_col=1, max_col=1, min_row=header_premio_row + 8):
        for cell in row:
            if cell.value == 'Strike':
                header_prob_row = cell.row
                break
        if header_prob_row:
            break
    if header_prob_row is None:
        raise ValueError(f'Matriz de probabilidade nao encontrada na aba {cidade}')

    for i, strike in enumerate(STRIKES_ORDEM, start=1):
        rr = header_prob_row + i
        for j, mes in enumerate(MESES_ORDEM, start=2):
            chave = (strike, mes)
            if chave in lookup_prob:
                ws.cell(row=rr, column=j).value = lookup_prob[chave]


def atualizar_referencias_data_na_capa(wb, ref_antiga: date, ref_nova: date):
    """Substitui o texto '(ref. DD/MM/AAAA)' hardcoded nas abas Capa e
    Metodologia (escrito pela ultima vez que gerar_excel.py rodou) pela
    data da curva atual - evita ficar um texto descritivo desatualizado
    ao lado de numeros ja atualizados."""
    txt_antigo = ref_antiga.strftime('%d/%m/%Y')
    txt_novo = ref_nova.strftime('%d/%m/%Y')
    n_trocas = 0
    for nome_aba in ['Capa', 'Metodologia']:
        ws = wb[nome_aba]
        for row in ws.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str) and txt_antigo in cell.value:
                    cell.value = cell.value.replace(txt_antigo, txt_novo)
                    n_trocas += 1
    return n_trocas


def atualizar_nota_curva_na_capa(ws_capa, data_ref_curva: date, data_execucao: date):
    """Escreve/atualiza uma linha visivel na Capa mostrando quando a
    curva de juros foi atualizada pela ultima vez - prova visual rapida
    de que a automacao esta rodando, sem precisar abrir log nenhum."""
    texto = (f"Última atualização automática: curva ETTJ ref. "
             f"{data_ref_curva.strftime('%d/%m/%Y')} "
             f"(script rodou em {data_execucao.strftime('%d/%m/%Y %H:%M')})")
    # usa a linha logo abaixo do bloco de specs (coluna B, ultima linha + 2)
    ultima_linha = ws_capa.max_row + 2
    ws_capa.cell(row=ultima_linha, column=2, value=texto)
    c = ws_capa.cell(row=ultima_linha, column=2)
    c.font = Font(name='Arial', size=8, italic=True, color='808080')


def rodar():
    print("=" * 70)
    print(f"ATUALIZACAO DE JUROS - {date.today().isoformat()}")
    print("=" * 70)

    try:
        texto = buscar_curva_anbima()
    except Exception as e:
        print(f"[ERRO] Falha ao buscar curva da ANBIMA: {e}")
        traceback.print_exc()
        return False

    ref_antiga = curva_juros.ETTJ_DATA_REF
    ref_nova, vertices_novos = curva_juros.atualizar_curva_de_texto_anbima(texto)

    if len(vertices_novos) < 5:
        print(f"[ERRO] Curva buscada parece incompleta ({len(vertices_novos)} vertices, "
              f"esperado 10). Abortando para nao gravar dado ruim.")
        return False

    curva_juros.salvar_cache()
    avancou = ref_nova > ref_antiga
    print(f"Curva anterior: {ref_antiga} | Curva nova: {ref_nova} | "
          f"{'AVANCOU' if avancou else 'MESMA DATA (sem pregao novo ainda)'}")

    # reprecifica tudo com a curva atualizada (automatico via cache)
    strip, dados_hist, safra_y, data_ref = motor.construir_strip(date.today())
    strip.to_csv(BASE / 'strip_precificacao_v2.csv', index=False)
    print(f"Reprecificados {len(strip)} contratos (safra {safra_y}/{safra_y+1})")

    if not EXCEL_PATH.exists():
        print(f"[AVISO] Excel nao encontrado em {EXCEL_PATH} - so o CSV foi atualizado")
        return True

    try:
        wb = load_workbook(EXCEL_PATH)
        n = atualizar_cadeia_de_strikes(wb['Cadeia de Strikes'], strip)
        print(f"[OK] Cadeia de Strikes: {n} linhas atualizadas")

        for cidade in motor.CIDADES:
            nome_aba = cidade[:28]
            strip_cidade = strip[strip.Cidade == cidade]
            atualizar_matriz_cidade(wb[nome_aba], strip_cidade, cidade)
            print(f"[OK] Aba {nome_aba}: matrizes atualizadas")

        atualizar_nota_curva_na_capa(wb['Capa'], ref_nova, date.today())
        n_trocas = atualizar_referencias_data_na_capa(wb, ref_antiga, ref_nova)
        print(f"[OK] {n_trocas} referências de data desatualizadas corrigidas (Capa/Metodologia)")

        wb.save(EXCEL_PATH)
        wb.close()
        print(f"[OK] Excel salvo: {EXCEL_PATH}")
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar Excel: {e}")
        traceback.print_exc()
        return False

    return True


if __name__ == '__main__':
    ok = rodar()
    sys.exit(0 if ok else 1)
