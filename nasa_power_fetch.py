"""
============================================================================
BUSCA DIARIA - NASA POWER API (execucao LOCAL via Claude Code / cron)
============================================================================
Este modulo faz chamadas de rede reais a API publica do NASA POWER.
NAO FUNCIONA no ambiente de chat do Claude (rede restrita) - foi escrito
para rodar localmente, onde voce (ou o cron) tem acesso de rede normal.

API publica, sem chave de acesso: https://power.larc.nasa.gov/docs/services/api/
"""
import requests
import pandas as pd
from pathlib import Path
from datetime import date, timedelta

API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

COORDENADAS = {
    'Sorriso': (-12.5453, -55.7093),
    'Sinop': (-11.8642, -55.5025),
    'Lucas do Rio Verde': (-13.0508, -55.9092),
}

PARAMETROS = "PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,RH2M,ALLSKY_SFC_SW_DWN,WS2M,GWETROOT"

CACHE_DIR = Path(__file__).parent / 'clima_cache'
CACHE_DIR.mkdir(exist_ok=True)


def buscar_dias(cidade: str, data_inicio: date, data_fim: date, timeout=30) -> pd.DataFrame:
    """
    Busca dados diarios da API do NASA POWER para uma cidade, no intervalo
    [data_inicio, data_fim] (inclusive). Retorna um DataFrame.
    Lanca excecao se a chamada falhar (tratamento de erro fica a cargo do
    chamador - ver daily_update.py, que loga e aborta o repricing daquele
    dia sem quebrar o cron).
    """
    lat, lon = COORDENADAS[cidade]
    params = {
        "parameters": PARAMETROS,
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": data_inicio.strftime("%Y%m%d"),
        "end": data_fim.strftime("%Y%m%d"),
        "format": "JSON",
    }
    resp = requests.get(API_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()

    props = payload["properties"]["parameter"]
    datas = sorted(props[PARAMETROS.split(',')[0]].keys())
    linhas = []
    for d in datas:
        linha = {'data': pd.to_datetime(d, format='%Y%m%d')}
        for p in PARAMETROS.split(','):
            valor = props[p].get(d)
            linha[p] = None if valor == -999 else valor
        linhas.append(linha)
    df = pd.DataFrame(linhas)
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['dia'] = df['data'].dt.day
    return df


def atualizar_cache_diario(cidade: str, dias_retroativos: int = 7) -> pd.DataFrame:
    """
    Busca os ultimos `dias_retroativos` dias (medido em producao: a API do
    NASA POWER tem defasagem de consolidacao de ate ~3 dias para o dado
    "near real time" - D-1 e D-2 costumam vir nulos, so D-3 vem preenchido -
    por isso buscar so "ontem" pode retornar vazio; buscar uma janela maior
    que essa defasagem e fazer merge/dedup e mais robusto, e permite ao
    cache se autocorrigir nos dias seguintes conforme o dado consolida) e
    atualiza o cache local em CSV, sem duplicar datas ja existentes.

    Em caso de falha de rede, propaga a excecao (NAO cai silenciosamente
    para o cache antigo) - o chamador (daily_update.py) decide o que fazer
    e loga o erro claramente. Isso evita mascarar uma falha real de
    atualizacao como se o dado do dia tivesse chegado.
    """
    novo = buscar_dias(cidade, date.today() - timedelta(days=dias_retroativos),
                        date.today() - timedelta(days=1))

    cache_path = CACHE_DIR / f'{cidade.replace(" ", "_")}_diario.csv'
    if cache_path.exists():
        existente = pd.read_csv(cache_path, parse_dates=['data'])
        combinado = pd.concat([existente, novo]).drop_duplicates(subset='data', keep='last')
        combinado = combinado.sort_values('data').reset_index(drop=True)
    else:
        combinado = novo

    combinado.to_csv(cache_path, index=False)
    return combinado


if __name__ == '__main__':
    import sys
    print("Testando conexao com a API do NASA POWER...")
    print("(Este teste SO funciona rodando localmente - vai falhar no chat do Claude)")
    try:
        df_teste = buscar_dias('Sorriso', date.today() - timedelta(days=5), date.today() - timedelta(days=1))
        print(f"OK - {len(df_teste)} dias retornados:")
        print(df_teste[['data', 'PRECTOTCORR', 'T2M_MAX']])
    except Exception as e:
        print(f"FALHOU: {e}")
        sys.exit(1)
