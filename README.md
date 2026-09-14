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

## Motor de precificação (US-2, RN-03)

Módulo `src/frota/precificacao.py`, função `precificar_itens(itens, tabela_precos)`.

O que faz: para cada item a precificar (com `codigo_item` e `classificacao`), busca o valor
correspondente na tabela de preços de reparo pelo par `(codigo_item, classificacao)`.
- Se o par existe na tabela: o item recebe `status="PRECIFICADO"` e o campo `valor` com o valor exato da tabela.
- Se o par não existe na tabela: o item recebe `status="SEM_PRECO"` (sem assumir valor zero) e é
  adicionado à lista de bloqueios com `motivo="SEM PREÇO NA TABELA"`.

Como usar:
```python
from frota.precificacao import precificar_itens

itens = [{"codigo_item": "PARACHOQUE_TRASEIRO", "classificacao": "AVARIA", "status": "A_PRECIFICAR"}]
tabela_precos = {("PARACHOQUE_TRASEIRO", "AVARIA"): 850.0}

itens_precificados, bloqueios = precificar_itens(itens, tabela_precos)
```

Como testar:
```bash
pytest -q tests/test_precificacao.py
```

Fora do escopo desta história: manutenção/atualização da planilha de preços (processo do
pós-venda) e aplicação da franquia (história de RN-04).
