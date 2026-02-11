# ADR-017 — Classificação de Equipamentos: Rastreáveis vs Contáveis

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
Equipamentos passam a ser classificados como:

- **Rastreáveis** (`tem_ativo=True`)
- **Contáveis** (`tem_ativo=False`)

## Contexto
Nem todos os itens exigem ativo ou número de série.
Alguns itens precisam de rastreabilidade individual,
enquanto outros são apenas confirmados por quantidade.

Sem essa distinção, o fluxo de execução ficava inconsistente
ou excessivamente rígido.

## Consequências
- A execução valida campos conforme o tipo do equipamento.
- Itens rastreáveis exigem ativo/bipagem individual.
- Itens contáveis exigem apenas confirmação quantitativa.
- Relatórios diferenciam ativos e consumíveis.
- Gates de NF passam a considerar tipos diferentes de validação.