# ADR-003 — Branches base: main / develop

**Data:** 2026-01-20  
**Status:** Aceito

## Decisão
Usaremos:
- `main` para estabilidade e releases
- `develop` para integração contínua

## Contexto
Separar o que está pronto para release do que está em desenvolvimento reduz risco operacional.

## Consequências
- Mudanças entram via branches derivadas e são integradas em `develop`.
- `main` recebe apenas conteúdo estável e controlado.