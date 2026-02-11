# ADR-004 — Repositório stack-agnostic (sem framework definido)

**Data:** 2026-01-20  
**Status:** Deprecado

## Decisão
O projeto permanecerá intencionalmente neutro quanto a stack e framework neste estágio inicial.

## Contexto
Durante a preparação do ambiente (Sprint 1), optou-se por evitar acoplamento prematuro a tecnologias
específicas (ex: Django, FastAPI, Node, etc.), permitindo que decisões sejam tomadas com base
em requisitos reais e não por conveniência inicial.

## Consequências
- `.gitignore` permanece genérico (Python / Node / OS).
- Nenhuma estrutura de framework é criada antecipadamente.
- A definição de stack será registrada explicitamente em decisão futura.

## Nota de deprecação
Esta decisão foi superada por **ADR-005 — Stack web definida: Django (2026-01-21)**.
Mantida para rastreabilidade histórica.