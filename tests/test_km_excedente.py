"""Testes do cálculo de quilometragem excedente (US-3, RN-05)."""
from frota.km_excedente import calcular_km_excedente


def test_km_rodada_maior_que_incluida_calcula_excedente_positivo():
    resultado = calcular_km_excedente(km_entrega=10000, km_devolucao=10500, km_incluida=300)
    assert resultado == 200


def test_km_rodada_menor_ou_igual_incluida_resulta_em_zero():
    resultado = calcular_km_excedente(km_entrega=10000, km_devolucao=10200, km_incluida=300)
    assert resultado == 0
