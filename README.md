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


## US-3 — Cálculo de quilometragem excedente (RN-05)
- **O que faz**: calcula a quilometragem excedente de um contrato a partir da km de entrega, km de devolução e km incluída, aplicando piso em zero (nunca retorna valor negativo), conforme RN-05.
- **Como usar**:
  ```python
  from frota.km_excedente import calcular_km_excedente

  excedente = calcular_km_excedente(km_entrega=10000, km_devolucao=10500, km_incluida=300)
  # excedente == 200
  ```
- **Como testar**:
  ```bash
  pytest -q tests/test_km_excedente.py
  ```
