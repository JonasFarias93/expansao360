# ADR-012 — Nomes semânticos e separação de templates do fluxo de Chamado

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Renomear templates e componentes do app `execucao` para nomes semânticos
que expressem claramente a responsabilidade de cada tela/fragmento,
reduzindo o risco de misturar etapas do fluxo
(abertura/planejamento vs execução operacional).

Separar explicitamente a renderização de itens em:

- Planejamento (status `ABERTO`)
- Operação (status `EM_EXECUCAO` e posteriores)

## Contexto
Após mudanças de layout, trechos de execução operacional foram inseridos
em templates de abertura/planejamento, causando confusão de fluxo e regressões.

O problema foi agravado por nomes genéricos como:

- `chamado_detalhe`
- `_itens_execucao`

Esses nomes não evidenciavam o estágio do processo.

## Consequências
- Alteração de nomes de arquivos impacta `includes` e `template_name` nas views.
- A refatoração deve ser entregue em commit atômico (rename + ajustes).
- Reduz significativamente risco de regressões futuras por confusão de responsabilidade.
- Reforça o contrato: cada template representa um estágio claro do workflow.