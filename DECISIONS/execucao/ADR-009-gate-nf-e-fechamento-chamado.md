# ADR-009 — Gate de NF e Critérios de Fechamento do Chamado

**Data:** 2026-02-03  
**Status:** Aceito

## Decisão
O Chamado só será liberado para NF quando:

- Todos os itens rastreáveis estiverem bipados.
- Todos os itens contáveis estiverem confirmados.

O fechamento do Chamado exige:

- NF informada.
- Confirmação de coleta, quando aplicável ao tipo do chamado.

## Contexto
A emissão da NF de saída depende da bipagem completa do kit
e da conferência dos itens.

Além disso, o Chamado não pode ser encerrado
sem evidências mínimas do processo.

## Consequências
- Implementação de método/flag de liberação para NF no `Chamado`
  (ex.: `pode_liberar_nf()`).
- Campos de NF e controle de coleta conforme fluxo.
- `finalizar()` valida pré-condições conforme tipo do chamado (ex.: ENVIO).
- Integração natural com classificação rastreável vs contável.