# ADR-018 — Renomeação de ChamadoDetailView para ChamadoExecucaoView

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
A view anteriormente chamada `ChamadoDetailView`
foi renomeada para `ChamadoExecucaoView`.

## Contexto
A view não representava apenas uma tela de leitura (detail),
mas sim a execução operacional do chamado, concentrando:

- Regras de progresso
- Evidências
- Gates
- Ações operacionais

O nome anterior não refletia sua responsabilidade real.

## Consequências
- O nome da classe passa a refletir sua responsabilidade.
- URLs e `url name` podem ser mantidos temporariamente
  para compatibilidade.
- Reduz ambiguidade entre leitura e execução.