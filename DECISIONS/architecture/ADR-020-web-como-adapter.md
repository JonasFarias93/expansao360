# ADR-020 — Web atua como Adapter (Camada de Entrega)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
A camada Web atua apenas como adapter responsável por:

- Interface de usuário (UI)
- Persistência via ORM
- Orquestração de casos de uso

As regras de negócio permanecem fora da camada de entrega.

## Contexto
Era necessário evitar que regras operacionais migrassem para:

- Views
- Templates
- Forms
- Signals

Sem essa separação, o sistema tenderia a acoplar domínio à camada Web,
dificultando evolução futura (API, CLI, mobile).

## Consequências
- O Core permanece independente de framework.
- CLI e Web compartilham o mesmo domínio.
- A Web não contém regras de negócio.
- Facilita futura exposição via API ou app mobile.
- Reduz risco de acoplamento indevido.