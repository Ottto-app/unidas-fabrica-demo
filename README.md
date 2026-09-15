# unidas-fabrica-demo

Repositório de LABORATÓRIO para a demonstração "Federação de Agentes" (Tess × Unidas).
Conteúdo fictício. Simula o par Azure Boards + Azure Repos usando GitHub Issues + este repositório.

## Convenções do board (Issues)
- `epic` — épico. Corpo lista as histórias filhas como task list.
- `user-story` / `tech-story` — história. Corpo no template do P.O. (descrição, regras, critérios de aceite, contrato_dev). Linha `Parent: #N` aponta o épico.
- `ready-for-dev` — pronta para o agente de desenvolvimento pegar.
- `in-progress` — o agente de desenvolvimento assumiu.
- `in-review` — PR aberto, aguardando revisão humana.
- `bloqueada` — falta informação (ver "PERGUNTAS AO NEGÓCIO").

## Convenções do código
- Python 3.12+, `src/frota/`, testes em `tests/` com pytest.
- Branch por história: `feature/US-<numero>-<slug>` a partir de `master` atualizada.
- Nunca merge direto em `master`; sempre Pull Request.

## Rodar
```bash
pip install -r requirements.txt
pytest -q
```

## US-5 — Motor: aplicar franquia contratual sobre a soma das avarias (RN-04)

O que faz: dado um bloco de itens de avaria já precificados (saída da história
de RN-03, tabela de preços) e a franquia de avarias do contrato, compara a
soma dos valores de tabela com a franquia e cobra o menor valor entre os
dois. O que exceder a franquia é absorvido pelo seguro e fica registrado na
memória de cálculo com status `ABSORVIDO_SEGURO`, sem entrar no total
cobrado. Os itens individuais mantêm seu valor de tabela original,
independentemente do rateio da franquia.

Como usar:
```python
from frota.franquia_avarias import ItemAvaria, aplicar_franquia_avarias

itens = [
    ItemAvaria(descricao="para-brisa trincado", valor_tabela=800.0),
    ItemAvaria(descricao="farol quebrado", valor_tabela=200.0),
]

resultado = aplicar_franquia_avarias(itens, franquia=600.0)
# resultado.valor_cobrado == 600.0
# resultado.valor_absorvido_seguro == 400.0
# resultado.status_excedente == "ABSORVIDO_SEGURO"
```

Como testar:
```bash
pytest -q tests/test_franquia_avarias.py
```
