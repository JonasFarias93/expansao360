# ADR-050 — Typo warning não bloqueante (ex.: `.111` vs `.11`)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Adicionar regra de **alerta de digitação** (não bloqueante):

- Quando o usuário informa `.111` quando era esperado `.11`,
  retornar `WARN / TYPO_WARNING` com sugestão.

Essa regra **não invalida** o IP por si só — apenas alerta.

## Contexto
Erros de digitação em IP são comuns e caros operacionalmente.
Nem todo typo deve bloquear o fluxo, mas deve orientar o técnico.

O objetivo é reduzir retrabalho sem criar fricção excessiva.

## Consequências
- Melhor UX: o técnico é alertado antes de finalizar.
- Mantém validação principal (prefixo/regra TC) como fonte de verdade.
- `TYPO_WARNING` vira reason oficial, testável e traduzível na UI.