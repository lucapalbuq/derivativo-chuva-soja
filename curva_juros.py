"""
============================================================================
CURVA DE JUROS FUTURA (ETTJ) - ANBIMA
============================================================================
Fonte: ANBIMA, Estrutura a Termo de Taxas de Juros, curva PREFIXADOS
(base "PREFIXADOS (CIRCULAR 3.361)" - vertices operacionais, mais adequados
para interpolacao de curto/medio prazo do que os 14 vertices fixos da
curva de referencia longa).

URL fonte: https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp
Esta URL retorna sempre a curva do ULTIMO PREGAO DISPONIVEL (nao precisa de
parametros de data) - o que a torna adequada para automacao diaria: basta
buscar a mesma URL todo dia para obter a curva mais recente publicada.

IMPORTANTE SOBRE ATUALIZACAO DIARIA:
Este modulo funciona em dois modos:
  1. CACHE ESTATICO (default): usa o snapshot real capturado em 11/08/2026,
     embutido abaixo. Funciona sempre, sem dependencia de rede.
  2. ATUALIZACAO: quando uma nova curva for buscada (por Claude, via
     web_fetch, ou por voce manualmente no site da ANBIMA), cole o texto
     bruto em atualizar_curva_de_texto_anbima() para atualizar o cache.

Este modulo NAO tenta fazer requests HTTP diretamente (o sandbox de
execucao de codigo nao tem a anbima.com.br liberada na rede) - a busca
real acontece via a ferramenta de web_fetch do Claude, fora deste script
Python. Ver README_ATUALIZACAO_DIARIA.md para o fluxo operacional completo.
"""

from datetime import date, datetime, timedelta
import re
import json
from pathlib import Path

CACHE_PATH = Path(__file__).parent / 'ettj_cache.json'

# ============================================================================
# CACHE DA CURVA (snapshot embutido como fallback; sobrescrito por
# ettj_cache.json quando existir - ver atualizar_juros.py para o fluxo
# de atualizacao diaria que gera esse arquivo)
# Fonte: https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp
# Tabela "PREFIXADOS (CIRCULAR 3.361)" - vertices em dias uteis, taxa em % a.a.
# ============================================================================
ETTJ_DATA_REF = date(2026, 8, 11)
ETTJ_VERTICES_DIAS_UTEIS = {
    21: 13.7242,
    42: 13.6647,
    63: 13.6279,
    126: 13.6095,
    252: 13.7545,
    504: 14.1173,
    756: 14.3731,
    1008: 14.5380,
    1260: 14.6403,
    2520: 14.6951,
}


def carregar_cache():
    """Se ettj_cache.json existir (gerado por uma atualizacao diaria
    anterior), sobrescreve o snapshot embutido acima com o dado mais
    recente. Roda automaticamente na importacao do modulo."""
    global ETTJ_DATA_REF, ETTJ_VERTICES_DIAS_UTEIS
    if not CACHE_PATH.exists():
        return
    try:
        dado = json.loads(CACHE_PATH.read_text())
        ETTJ_DATA_REF = datetime.strptime(dado['data_ref'], '%Y-%m-%d').date()
        ETTJ_VERTICES_DIAS_UTEIS = {int(k): float(v) for k, v in dado['vertices'].items()}
    except Exception:
        pass  # cache corrompido/incompleto -> mantem o snapshot embutido


def salvar_cache():
    """Persiste a curva atual (apos atualizar_curva_de_texto_anbima) em
    ettj_cache.json, para que a proxima execucao do script (e de
    cme_structurer_v2.py) ja carregue o dado novo automaticamente."""
    CACHE_PATH.write_text(json.dumps({
        'data_ref': ETTJ_DATA_REF.isoformat(),
        'vertices': ETTJ_VERTICES_DIAS_UTEIS,
        'atualizado_em': datetime.now().isoformat(),
    }, indent=2))


carregar_cache()


def atualizar_curva_de_texto_anbima(texto_bruto: str):
    """
    Faz o parse do texto bruto retornado por CZ-down.asp e atualiza o cache
    em memoria (nao persiste em disco automaticamente - chame salvar_cache()
    depois se quiser persistir).

    Uso: cole aqui o texto retornado pelo web_fetch da URL da ANBIMA.
    """
    global ETTJ_DATA_REF, ETTJ_VERTICES_DIAS_UTEIS

    m_data = re.search(r'(\d{2}/\d{2}/\d{4});Beta', texto_bruto)
    if m_data:
        ETTJ_DATA_REF = datetime.strptime(m_data.group(1), '%d/%m/%Y').date()

    bloco = texto_bruto.split('PREFIXADOS (CIRCULAR 3.361)')[-1]
    linhas = bloco.strip().splitlines()
    novos_vertices = {}
    for linha in linhas[1:]:  # pula so o cabecalho "Vertices;Taxa (%a.a.)"
        partes = linha.strip().split(';')
        if len(partes) != 2:
            continue
        try:
            dias = int(partes[0].replace('.', ''))
            taxa = float(partes[1].replace(',', '.'))
            novos_vertices[dias] = taxa
        except ValueError:
            continue
    if novos_vertices:
        ETTJ_VERTICES_DIAS_UTEIS = novos_vertices
    return ETTJ_DATA_REF, ETTJ_VERTICES_DIAS_UTEIS


def taxa_anual_para_prazo(dias_uteis: float) -> float:
    """
    Interpola linearmente a taxa anual (% a.a.) da ETTJ para um prazo em
    dias uteis. Fora do range dos vertices, usa extrapolacao flat (repete
    a taxa do vertice mais proximo) - conservador e padrao de mercado para
    prazos muito curtos ou muito longos.
    """
    vertices = sorted(ETTJ_VERTICES_DIAS_UTEIS.keys())
    if dias_uteis <= vertices[0]:
        return ETTJ_VERTICES_DIAS_UTEIS[vertices[0]]
    if dias_uteis >= vertices[-1]:
        return ETTJ_VERTICES_DIAS_UTEIS[vertices[-1]]
    for i in range(len(vertices) - 1):
        v0, v1 = vertices[i], vertices[i + 1]
        if v0 <= dias_uteis <= v1:
            t0, t1 = ETTJ_VERTICES_DIAS_UTEIS[v0], ETTJ_VERTICES_DIAS_UTEIS[v1]
            peso = (dias_uteis - v0) / (v1 - v0)
            return t0 + peso * (t1 - t0)
    return ETTJ_VERTICES_DIAS_UTEIS[vertices[-1]]


def dias_uteis_entre(data_ini: date, data_fim: date) -> int:
    """Conta dias uteis (seg-sex) entre duas datas. Nao desconta feriados
    nacionais (simplificacao documentada - impacto marginal em prazos curtos)."""
    if data_fim <= data_ini:
        return 0
    dias = 0
    d = data_ini
    while d < data_fim:
        d += timedelta(days=1)
        if d.weekday() < 5:
            dias += 1
    return dias


def fator_desconto(data_ref: date, data_liquidacao: date) -> float:
    """
    Fator de desconto = 1 / (1 + taxa(prazo))^(dias_uteis/252), usando a
    taxa especifica do vencimento (curva ETTJ), nao uma taxa unica.
    """
    du = dias_uteis_entre(data_ref, data_liquidacao)
    if du <= 0:
        return 1.0
    taxa = taxa_anual_para_prazo(du) / 100
    return 1 / (1 + taxa) ** (du / 252)


def resumo_curva():
    linhas = [f"Curva ETTJ ANBIMA (ref. {ETTJ_DATA_REF.strftime('%d/%m/%Y')}):"]
    for du, taxa in sorted(ETTJ_VERTICES_DIAS_UTEIS.items()):
        linhas.append(f"  {du:>5} d.u. ({du/252*12:4.1f} meses) -> {taxa:.4f}% a.a.")
    return '\n'.join(linhas)


if __name__ == '__main__':
    print(resumo_curva())
    print()
    hoje = date(2026, 8, 13)
    for meses in [1, 2, 3, 4, 5, 6]:
        venc = hoje + timedelta(days=meses * 30)
        du = dias_uteis_entre(hoje, venc)
        taxa = taxa_anual_para_prazo(du)
        df = fator_desconto(hoje, venc)
        print(f"~{meses} mes(es) ({du} d.u.): taxa={taxa:.3f}% a.a. | fator desconto={df:.5f}")
