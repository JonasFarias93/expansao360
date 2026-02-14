# ADR-010 — Ciclo de Vida do Chamado, Prioridade e Ticket Externo

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Evoluir o **Chamado** para operar com regras explícitas de ciclo de vida, incluindo:

- Ticket Externo obrigatório na criação
- Campo de Prioridade para ordenação da fila
- Estados intermediários no fluxo operacional (contábil, NF, coleta)
- `FINALIZADO` como estado terminal do processo

## Contexto
O processo operacional real não permite:

- Emitir NF sem contábil informado
- Finalizar sem confirmação de coleta (quando aplicável)
- Criar chamado sem ticket externo

Sem regras explícitas de ciclo de vida, o sistema permitiria
estados inconsistentes e avanço indevido de fluxo.

## Consequências
- O modelo `Chamado` passa a refletir explicitamente o workflow.
- A criação exige `ticket_externo`.
- A fila operacional utiliza `prioridade` como critério de ordenação.
- A transição de status é governada por regras de negócio (não apenas por UI).
- `FINALIZADO` torna-se estado terminal (sem regressão).
- Testes devem cobrir bloqueios de transição inválida.