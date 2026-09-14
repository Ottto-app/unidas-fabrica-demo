"""Testes do motor de precificacao (RN-03).

Cobre os casos de teste do contrato_dev da US-2:
- test_item_com_preco_na_tabela_recebe_valor_exato
- test_item_sem_preco_na_tabela_gera_bloqueio_sem_assumir_zero
"""
from frota.precificacao import precificar_itens


def _item(codigo_item, classificacao):
    return {
        "codigo_item": codigo_item,
        "classificacao": classificacao,
        "status": "A_PRECIFICAR",
    }


def test_item_com_preco_na_tabela_recebe_valor_exato():
    itens = [_item("PARACHOQUE_TRASEIRO", "AVARIA")]
    tabela_precos = {("PARACHOQUE_TRASEIRO", "AVARIA"): 850.0}

    itens_precificados, bloqueios = precificar_itens(itens, tabela_precos)

    assert bloqueios == []
    assert len(itens_precificados) == 1
    item = itens_precificados[0]
    assert item["status"] == "PRECIFICADO"
    assert item["valor"] == 850.0


def test_item_sem_preco_na_tabela_gera_bloqueio_sem_assumir_zero():
    itens = [_item("FAROL_DIREITO", "AVARIA")]
    tabela_precos = {("PARACHOQUE_TRASEIRO", "AVARIA"): 850.0}

    itens_precificados, bloqueios = precificar_itens(itens, tabela_precos)

    assert len(itens_precificados) == 1
    item = itens_precificados[0]
    assert item["status"] == "SEM_PRECO"
    assert "valor" not in item

    assert len(bloqueios) == 1
    bloqueio = bloqueios[0]
    assert bloqueio["codigo_item"] == "FAROL_DIREITO"
    assert bloqueio["classificacao"] == "AVARIA"
    assert bloqueio["motivo"] == "SEM PREÇO NA TABELA"
