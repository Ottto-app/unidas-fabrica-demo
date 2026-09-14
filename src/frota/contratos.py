"""Modelos mínimos de contrato de locação (fictícios, para o laboratório)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Contrato:
    """Contrato de locação de um veículo.

    km_incluido: quilometragem contratada para o período.
    franquia_avarias: valor (R$) que o cliente paga antes do seguro cobrir avarias.
    """

    numero: str
    placa: str
    km_incluido: int
    franquia_avarias: float
