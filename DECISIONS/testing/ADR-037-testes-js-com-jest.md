# ADR-037 — Adoção de testes JavaScript com Jest

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Adotar **Jest + jsdom** para testar JavaScript puro do frontend,
especialmente comportamentos de formsets dinâmicos.

## Contexto
O bug do “tipo vazio” em linhas adicionadas dinamicamente
não era coberto por testes backend.

Lógicas críticas de UI não podem depender apenas de `pytest`.

## Consequências
- Node/npm passam a ser dependência de desenvolvimento.
- Testes JS ficam próximos aos arquivos estáticos do app.
- Base para cobrir regressões em scripts de UI.
- Integração esperada no Makefile (`pytest` + `jest`) para execução unificada.