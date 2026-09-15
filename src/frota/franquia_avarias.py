"""Motor de aplicação da franquia contratual sobre avarias (US-5).

Regra de negócio RN-04: a soma das avarias cobráveis é comparada à franquia
do contrato. O cliente paga o menor valor entre a soma das avarias e a
franquia. O que exceder a franquia é absorvido pelo seguro e sai da
cobrança, mas fica registrado na memória de cálculo com status
ABSORVIDO_SEGURO.
"""
from dataclasses import dataclass, field


STATUS_ABSORVIDO_SEGURO = "ABSORVIDO_SEGURO"


@dataclass(frozen=True)
class ItemAvaria:
    """Item de avaria precificado (saída da história de RN-03).

    descricao: identificação do item avariado.
    valor_tabela: valor (R$) aplicado ao item conforme tabela de preços,
        mantido para a memória de cálculo independentemente do rateio
        da franquia.
    """

    descricao: str
    valor_tabela: float


@dataclass(frozen=True)
class ResultadoFranquiaAvarias:
    """Resultado da aplicação da franquia sobre o bloco de avarias.

    itens: itens individuais, preservando seu valor de tabela original.
    soma_avarias: soma dos valores de tabela de todos os itens.
    franquia: valor da franquia de avarias do contrato.
    valor_cobrado: valor efetivamente cobrado do cliente no bloco avarias
        (o menor entre soma_avarias e franquia).
    valor_absorvido_seguro: parte da soma que excede a franquia e é
        absorvida pelo seguro (0.0 quando não há excedente).
    status_excedente: STATUS_ABSORVIDO_SEGURO quando há excedente absorvido
        pelo seguro; None quando a soma não excede a franquia.
    """

    itens: list
    soma_avarias: float
    franquia: float
    valor_cobrado: float
    valor_absorvido_seguro: float
    status_excedente: str = None


def aplicar_franquia_avarias(itens, franquia):
    """Aplica a franquia contratual (RN-04) sobre a soma das avarias cobráveis.

    Compara a soma dos valores de tabela dos itens de avaria com a franquia
    do contrato e cobra o menor valor entre os dois. O excedente, quando
    houver, é absorvido pelo seguro e registrado na memória de cálculo com
    status ABSORVIDO_SEGURO, sem entrar no total cobrado.

    Args:
        itens: lista de ItemAvaria com valor de tabela já aplicado (RN-03).
        franquia: valor (R$) da franquia de avarias do contrato.

    Returns:
        ResultadoFranquiaAvarias com o valor cobrado, o valor absorvido pelo
        seguro (se houver) e os itens individuais intactos.
    """
    soma_avarias = sum(item.valor_tabela for item in itens)
    valor_cobrado = min(soma_avarias, franquia)
    valor_absorvido_seguro = max(soma_avarias - franquia, 0.0)
    status_excedente = STATUS_ABSORVIDO_SEGURO if valor_absorvido_seguro > 0 else None

    return ResultadoFranquiaAvarias(
        itens=list(itens),
        soma_avarias=soma_avarias,
        franquia=franquia,
        valor_cobrado=valor_cobrado,
        valor_absorvido_seguro=valor_absorvido_seguro,
        status_excedente=status_excedente,
    )
