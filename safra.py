"""
============================================================================
MODELO DE SAFRA ROLANTE (CROP-YEAR ROLL)
============================================================================
Define o ciclo de safra como Marco do ano Y ate Fevereiro do ano Y+1.
Os contratos precificados em um dado momento sao sempre os da safra em
curso dentro desse ciclo (Set Y a Fev Y+1, dentro da janela Mar Y-Fev Y+1).

Quando o calendario vira Marco do ano Y+1, a safra Y/Y+1 fica completa e
passa a integrar a base historica; a safra ativa passa a ser Y+1/Y+2.
"""

from datetime import date

MESES_SAFRA = [
    (9, 'Setembro', 'Plantio'),
    (10, 'Outubro', 'Emergência/Vegetativo'),
    (11, 'Novembro', 'Vegetativo'),
    (12, 'Dezembro', 'Veg/Início Reprodutivo'),
    (1, 'Janeiro', 'Reprodutivo (R) - CRÍTICO'),
    (2, 'Fevereiro', 'Reprodutivo (R) - CRÍTICO'),
]


def get_safra_atual(data_referencia: date) -> int:
    """
    Retorna Y, o ano de INICIO do ciclo de safra vigente (Marco Y a
    Fevereiro Y+1), para uma data de referencia qualquer.
    """
    if data_referencia.month >= 3:
        return data_referencia.year
    return data_referencia.year - 1


def get_contratos_da_safra(safra_y: int):
    """
    Retorna a lista de contratos da safra Y/Y+1, cada um com o ano
    calendario correto (Set-Dez pertencem a Y; Jan-Fev pertencem a Y+1) e
    a data de liquidacao estimada (5 dias uteis apos o fim do mes de
    medicao - alinhado ao contract spec: liquidacao financeira poucos dias
    apos o fim do mes).
    """
    contratos = []
    for mes_num, mes_nome, fase in MESES_SAFRA:
        ano_calendario = safra_y if mes_num >= 9 else safra_y + 1
        # ultimo dia do mes de medicao
        if mes_num == 12:
            fim_mes = date(ano_calendario + 1, 1, 1)
        else:
            fim_mes = date(ano_calendario, mes_num + 1, 1)
        # data de liquidacao ~5 dias corridos apos fim do mes (aprox. contratual)
        from datetime import timedelta
        data_liquidacao = fim_mes + timedelta(days=5)
        contratos.append({
            'mes_num': mes_num, 'mes_nome': mes_nome, 'fase': fase,
            'ano_calendario': ano_calendario, 'data_liquidacao': data_liquidacao,
        })
    return contratos


def anos_historicos_elegiveis(safra_y: int, ano_min: int = 1990) -> list:
    """
    Retorna a lista de anos-calendario de SETEMBRO das safras completas
    anteriores a safra_y (a safra_y, em curso, NAO entra na base historica
    ate que role para o proximo ciclo em Marco). Usado para filtrar a base
    de HBA/Monte Carlo por mes.
    """
    return list(range(ano_min, safra_y))  # exclui safra_y (em curso)


def descricao_ciclo(safra_y: int) -> str:
    return f"Safra {safra_y}/{safra_y+1} (ciclo Mar/{safra_y} a Fev/{safra_y+1})"


if __name__ == '__main__':
    for teste in [date(2026, 8, 13), date(2027, 1, 15), date(2027, 3, 2), date(2027, 6, 1)]:
        y = get_safra_atual(teste)
        print(f"Data ref {teste} -> {descricao_ciclo(y)}")
        print(f"  Anos historicos elegiveis para HBA/MC: {anos_historicos_elegiveis(y)[-3:]}...(ate {y-1})")
        contratos = get_contratos_da_safra(y)
        for c in contratos:
            print(f"    {c['mes_nome']}/{c['ano_calendario']} -> liquidação {c['data_liquidacao']}")
        print()
