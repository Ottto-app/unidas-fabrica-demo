from frota.contratos import Contrato


def test_contrato_e_imutavel():
    c = Contrato(numero="C-001", placa="ABC1D23", km_incluido=3000, franquia_avarias=2500.0)
    assert c.km_incluido == 3000
