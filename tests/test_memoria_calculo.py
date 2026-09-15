"""Testes para a memória de cálculo detalhada por item e por bloco (US-6)."""
from frota.memoria_calculo import ItemMemoria, ResultadoConsolidado, gerar_memoria_calculo


def _resultado_exemplo():
    itens = [
        ItemMemoria(
            codigo="AV-01",
            classificacao="RISCO_LATERAL",
            preco_aplicado=350.0,
            status="COBRADO",
            bloco="avarias",
        ),
        ItemMemoria(
            codigo="AV-02",
            classificacao="AMASSADO_PORTA",
            preco_aplicado=800.0,
            status="ABSORVIDO_SEGURO",
            bloco="avarias",
        ),
        ItemMemoria(
            codigo="FR-01",
            classificacao="FRANQUIA_APLICADA",
            preco_aplicado=2500.0,
            status="COBRADO",
            bloco="franquia_avarias",
        ),
        ItemMemoria(
            codigo="KM-01",
            classificacao="KM_EXCEDENTE",
            preco_aplicado=0.0,
            status="ISENTO",
            bloco="km_excedente",
        ),
        ItemMemoria(
            codigo="AV-03",
            classificacao="RISCO_PARABRISA",
            preco_aplicado=None,
            status="SEM_PRECO",
            bloco="avarias",
        ),
    ]
    totais_por_bloco = {
        "avarias": 350.0,
        "franquia_avarias": 2500.0,
        "km_excedente": 0.0,
        "total_geral": 2850.0,
    }
    return ResultadoConsolidado(itens=itens, totais_por_bloco=totais_por_bloco)


def test_memoria_lista_todos_os_itens_com_status_e_preco():
    resultado = _resultado_exemplo()
    memoria = gerar_memoria_calculo(resultado)

    for item in resultado.itens:
        assert item.codigo in memoria
        assert item.classificacao in memoria
        assert item.status in memoria

    assert "COBRADO" in memoria
    assert "ABSORVIDO_SEGURO" in memoria
    assert "ISENTO" in memoria
    assert "SEM_PRECO" in memoria


def test_memoria_exibe_totais_por_bloco_consistentes_com_itens():
    resultado = _resultado_exemplo()
    memoria = gerar_memoria_calculo(resultado)

    soma_avarias_cobradas_e_isentas = sum(
        item.preco_aplicado or 0.0
        for item in resultado.itens
        if item.bloco == "avarias" and item.status != "ABSORVIDO_SEGURO"
    )

    assert f"{resultado.totais_por_bloco['avarias']:.2f}" in memoria
    assert f"{resultado.totais_por_bloco['franquia_avarias']:.2f}" in memoria
    assert f"{resultado.totais_por_bloco['km_excedente']:.2f}" in memoria
    assert f"{resultado.totais_por_bloco['total_geral']:.2f}" in memoria
    assert soma_avarias_cobradas_e_isentas == resultado.totais_por_bloco["avarias"]
