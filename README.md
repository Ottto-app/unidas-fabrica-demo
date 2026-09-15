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

## Classificação de itens da vistoria de devolução (US-4)

Função que classifica cada item avaliado na vistoria de devolução segundo sua
classificação de dano e a cobertura do contrato, determinando se o item entra
ou não na cobrança antes das demais etapas de cálculo (precificação e
franquia, tratadas em histórias futuras).

Regras aplicadas:
- RN-01: item `SEM_DANO` não gera cobrança (status `ISENTO`, valor `0`).
- RN-02: item `DESGASTE_NATURAL` fica `ISENTO` quando o contrato tem cobertura
  de desgaste natural; sem cobertura, é tratado como `LEVE` (status
  `A_PRECIFICAR`, classificação efetiva `LEVE`).

Como usar:
```python
from frota.classificacao_item import classificar_item

classificar_item("SEM_DANO", cobertura_desgaste_natural=False)
# {"status": "ISENTO", "valor": 0}

classificar_item("DESGASTE_NATURAL", cobertura_desgaste_natural=False)
# {"status": "A_PRECIFICAR", "classificacao_efetiva": "LEVE"}
```

Como testar:
```bash
pytest -q tests/test_classificacao_item.py
```
