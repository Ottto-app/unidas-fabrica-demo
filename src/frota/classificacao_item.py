"""Classificação de itens de vistoria de devolução (US-4).

Aplica RN-01 e RN-02 antes das demais etapas de cálculo (precificação e
franquia, que são responsabilidade de histórias futuras).

Contrato:
    Entrada: classificação do item avaliado na vistoria (``str``) e um
    indicador booleano de cobertura de desgaste natural do contrato.
    Saída: ``dict`` com o status intermediário do item (``"ISENTO"`` ou
    ``"A_PRECIFICAR"``) e, quando aplicável, a classificação efetiva a ser
    usada na precificação (por exemplo, ``DESGASTE_NATURAL`` rebaixado para
    ``LEVE`` quando o contrato não tem cobertura).

Fora do escopo: aplicar preço de tabela (RN-03) e aplicar franquia (RN-04).
"""

STATUS_ISENTO = "ISENTO"
STATUS_A_PRECIFICAR = "A_PRECIFICAR"


def classificar_item(classificacao: str, cobertura_desgaste_natural: bool) -> dict:
    """Classifica um item da vistoria de devolução segundo RN-01 e RN-02.

    Args:
        classificacao: Classificação de dano do item (ex.: "SEM_DANO",
            "DESGASTE_NATURAL", "LEVE", "MEDIO", "GRAVE").
        cobertura_desgaste_natural: Indica se o contrato tem cobertura de
            desgaste natural.

    Returns:
        dict com as chaves:
            - "status": "ISENTO" ou "A_PRECIFICAR".
            - "valor": 0 quando "ISENTO"; ausente/não definido quando
              "A_PRECIFICAR" (a precificação é responsabilidade de outra
              história).
            - "classificacao_efetiva": classificação a usar na
              precificação, presente quando o status é "A_PRECIFICAR".
    """
    if classificacao == "SEM_DANO":
        return {"status": STATUS_ISENTO, "valor": 0}

    if classificacao == "DESGASTE_NATURAL":
        if cobertura_desgaste_natural:
            return {"status": STATUS_ISENTO, "valor": 0}
        return {"status": STATUS_A_PRECIFICAR, "classificacao_efetiva": "LEVE"}

    return {"status": STATUS_A_PRECIFICAR, "classificacao_efetiva": classificacao}
