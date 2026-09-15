"""Memória de cálculo detalhada por item e por bloco (US-6, RN-07).

Gera um texto legível, a partir do resultado consolidado do motor de cálculo
(itens com status e valores, totais por bloco), para anexar como evidência
à fatura (seção 4.3 do PRD).

Este módulo NÃO decide classificação, preço, franquia ou km excedente — essas
regras (RN-01 a RN-06) são responsabilidade das histórias que alimentam o
``ResultadoConsolidado`` usado aqui como entrada.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ItemMemoria:
    """Um item avaliado na vistoria, já classificado e precificado.

    codigo: identificador do item (ex.: código da avaria).
    classificacao: categoria/tipo do item.
    preco_aplicado: valor em R$ atribuído ao item; ``None`` quando não há
        preço definido (status ``SEM_PRECO``).
    status: um de ``COBRADO``, ``ABSORVIDO_SEGURO``, ``ISENTO`` ou
        ``SEM_PRECO``.
    bloco: bloco ao qual o item pertence (ex.: ``avarias``,
        ``franquia_avarias``, ``km_excedente``).
    """

    codigo: str
    classificacao: str
    preco_aplicado: Optional[float]
    status: str
    bloco: str


@dataclass(frozen=True)
class ResultadoConsolidado:
    """Resultado consolidado do motor de cálculo (entrada desta história).

    itens: lista de :class:`ItemMemoria` avaliados no cálculo.
    totais_por_bloco: mapa bloco -> total agregado em R$; espera-se ao menos
        as chaves ``avarias``, ``franquia_avarias``, ``km_excedente`` e
        ``total_geral``.
    """

    itens: list[ItemMemoria] = field(default_factory=list)
    totais_por_bloco: dict[str, float] = field(default_factory=dict)


_TITULOS_BLOCO = {
    "avarias": "Avarias",
    "franquia_avarias": "Franquia aplicada",
    "km_excedente": "Km excedente",
}


def gerar_memoria_calculo(resultado: ResultadoConsolidado) -> str:
    """Gera o texto legível da memória de cálculo.

    Lista cada item individualmente (código, classificação, preço aplicado
    e status) e, em seguida, os totais agregados por bloco — incluindo o
    total geral — de forma consistente com os itens individuais.
    """
    linhas = ["MEMÓRIA DE CÁLCULO", ""]

    linhas.append("Itens avaliados:")
    for item in resultado.itens:
        preco_txt = f"R$ {item.preco_aplicado:.2f}" if item.preco_aplicado is not None else "sem preço"
        linhas.append(
            f"- {item.codigo} | {item.classificacao} | {preco_txt} | {item.status}"
        )

    linhas.append("")
    linhas.append("Totais por bloco:")
    for chave, titulo in _TITULOS_BLOCO.items():
        valor = resultado.totais_por_bloco.get(chave, 0.0)
        linhas.append(f"- {titulo}: R$ {valor:.2f}")

    total_geral = resultado.totais_por_bloco.get("total_geral", 0.0)
    linhas.append(f"- Total geral: R$ {total_geral:.2f}")

    return "\n".join(linhas)
