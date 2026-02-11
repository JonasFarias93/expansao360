# ADR-014 — Template dedicado para Setup do Chamado

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
Criar um template dedicado `execucao/chamado_setup.html`
para o estágio de planejamento do chamado,
mantendo `execucao/chamado_execucao.html`
apenas para os estágios operacionais (`EM_EXECUCAO` e posteriores).

## Contexto
O template principal estava acumulando responsabilidades
de planejamento e execução, exigindo múltiplos `if status == ...`
no HTML e aumentando o risco de mistura de ações operacionais
no estado `ABERTO`.

Isso tornava o contrato de cada tela ambíguo e aumentava
a chance de regressões.

## Consequências
- `ChamadoSetupView` passa a renderizar `chamado_setup.html`.
- `ChamadoExecucaoView` fica restrita aos estágios operacionais.
- Caso `status == ABERTO`, o fluxo deve redirecionar para setup.
- Redução significativa de branching condicional nos templates.
- Contrato de responsabilidade por estágio fica explícito.