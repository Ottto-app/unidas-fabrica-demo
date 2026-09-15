"""Cálculo da quilometragem excedente da devolução (US-3, RN-05).

RN-05: a quilometragem excedente é a diferença entre a km rodada
(km de devolução menos km de entrega) e a km incluída no contrato,
nunca podendo ser negativa (piso em zero).
"""


def calcular_km_excedente(km_entrega, km_devolucao, km_incluida):
    """Calcula a quilometragem excedente de um contrato.

    Args:
        km_entrega: leitura do odômetro na entrega do veículo.
        km_devolucao: leitura do odômetro na devolução do veículo.
        km_incluida: quilometragem incluída no contrato para o período.

    Returns:
        A quilometragem excedente (km rodada menos km incluída), nunca
        negativa. Se a km rodada for menor ou igual à km incluída,
        retorna zero (RN-05).
    """
    km_rodada = km_devolucao - km_entrega
    excedente = km_rodada - km_incluida
    return max(excedente, 0)
