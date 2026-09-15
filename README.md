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

## Memória de cálculo detalhada (US-6)
Gera um texto legível com cada item avaliado (código, classificação, preço
aplicado e status: `COBRADO`, `ABSORVIDO_SEGURO`, `ISENTO` ou `SEM_PRECO`) e
os totais agregados por bloco (avarias, franquia aplicada, km excedente e
total geral), para anexar como evidência à fatura.

Como usar:
```python
from frota.memoria_calculo import ItemMemoria, ResultadoConsolidado, gerar_memoria_calculo

resultado = ResultadoConsolidado(
    itens=[
        ItemMemoria(codigo="AV-01", classificacao="RISCO_LATERAL", preco_aplicado=350.0, status="COBRADO", bloco="avarias"),
    ],
    totais_por_bloco={"avarias": 350.0, "franquia_avarias": 0.0, "km_excedente": 0.0, "total_geral": 350.0},
)
print(gerar_memoria_calculo(resultado))
```

Como testar:
```bash
pytest -q tests/test_memoria_calculo.py
```
