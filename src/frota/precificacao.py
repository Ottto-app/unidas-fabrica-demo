"""Motor de precificacao de itens de reparo (RN-03).

Busca, para cada item a precificar, o valor correspondente na tabela de
precos pelo par (codigo do item, classificacao). Itens sem correspondencia
na tabela sao bloqueados com o motivo "SEM PREÇO NA TABELA" -- nunca
recebem valor zero assumido.
"""

MOTIVO_SEM_PRECO = "SEM PREÇO NA TABELA"


def precificar_itens(itens, tabela_precos):
    """Precifica itens a partir da tabela de precos de reparo (RN-03).

    Args:
        itens: lista de dicts com pelo menos "codigo_item" e "classificacao"
            (itens com status A_PRECIFICAR, saida da classificacao RN-01/RN-02).
        tabela_precos: dict {(codigo_item, classificacao): valor} com os
            precos de reparo cadastrados.

    Returns:
        Tupla (itens_precificados, bloqueios):
        - itens_precificados: lista de dicts, cada item original com
          "status" atualizado para "PRECIFICADO" (+ "valor") ou "SEM_PRECO"
          (sem a chave "valor").
        - bloqueios: lista de dicts {"codigo_item", "classificacao", "motivo"}
          para cada item sem correspondencia na tabela de precos.
    """
    itens_precificados = []
    bloqueios = []

    for item in itens:
        codigo_item = item["codigo_item"]
        classificacao = item["classificacao"]
        chave = (codigo_item, classificacao)

        item_resultado = dict(item)

        if chave in tabela_precos:
            item_resultado["status"] = "PRECIFICADO"
            item_resultado["valor"] = tabela_precos[chave]
        else:
            item_resultado["status"] = "SEM_PRECO"
            item_resultado.pop("valor", None)
            bloqueios.append({
                "codigo_item": codigo_item,
                "classificacao": classificacao,
                "motivo": MOTIVO_SEM_PRECO,
            })

        itens_precificados.append(item_resultado)

    return itens_precificados, bloqueios
