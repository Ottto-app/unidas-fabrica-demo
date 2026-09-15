"""Testes da classificação de itens de vistoria de devolução (US-4).

Cobre RN-01 (SEM_DANO não gera cobrança) e RN-02 (DESGASTE_NATURAL depende
da cobertura de desgaste natural do contrato), conforme os critérios de
aceite da história US-4.
"""
from frota.classificacao_item import classificar_item


def test_item_sem_dano_fica_isento():
    resultado = classificar_item("SEM_DANO", cobertura_desgaste_natural=False)

    assert resultado["status"] == "ISENTO"
    assert resultado["valor"] == 0


def test_desgaste_natural_com_cobertura_fica_isento():
    resultado = classificar_item("DESGASTE_NATURAL", cobertura_desgaste_natural=True)

    assert resultado["status"] == "ISENTO"


def test_desgaste_natural_sem_cobertura_e_tratado_como_leve():
    resultado = classificar_item("DESGASTE_NATURAL", cobertura_desgaste_natural=False)

    assert resultado["status"] == "A_PRECIFICAR"
    assert resultado["classificacao_efetiva"] == "LEVE"
