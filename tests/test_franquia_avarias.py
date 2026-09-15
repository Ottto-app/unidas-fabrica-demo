"""Testes do motor de aplicação da franquia contratual sobre avarias (US-5)."""
from frota.franquia_avarias import ItemAvaria, aplicar_franquia_avarias


def test_soma_avarias_menor_que_franquia_cobra_soma_integral():
    """RN-04: soma <= franquia => valor cobrado é a soma integral das avarias."""
    itens = [
        ItemAvaria(descricao="arranhão na porta", valor_tabela=100.0),
        ItemAvaria(descricao="amassado no para-lama", valor_tabela=150.0),
    ]

    resultado = aplicar_franquia_avarias(itens, franquia=500.0)

    assert resultado.soma_avarias == 250.0
    assert resultado.valor_cobrado == 250.0
    assert resultado.valor_absorvido_seguro == 0.0
    assert resultado.status_excedente is None
    assert resultado.itens[0].valor_tabela == 100.0
    assert resultado.itens[1].valor_tabela == 150.0


def test_soma_avarias_maior_que_franquia_cobra_franquia_e_registra_excedente_absorvido():
    """RN-04: soma > franquia => cobra a franquia e registra excedente ABSORVIDO_SEGURO."""
    itens = [
        ItemAvaria(descricao="para-brisa trincado", valor_tabela=800.0),
        ItemAvaria(descricao="farol quebrado", valor_tabela=200.0),
    ]

    resultado = aplicar_franquia_avarias(itens, franquia=600.0)

    assert resultado.soma_avarias == 1000.0
    assert resultado.valor_cobrado == 600.0
    assert resultado.valor_absorvido_seguro == 400.0
    assert resultado.status_excedente == "ABSORVIDO_SEGURO"
    assert resultado.itens[0].valor_tabela == 800.0
    assert resultado.itens[1].valor_tabela == 200.0
