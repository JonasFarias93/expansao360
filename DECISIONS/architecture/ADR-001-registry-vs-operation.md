# ADR-001 — Separação conceitual: Registry x Operation

**Data:** 2026-01-20  
**Status:** Aceito

## Decisão
O sistema será modelado com duas camadas conceituais principais:
- **Registry (Cadastro Mestre)**: define “o que existe” e “como deve ser”
- **Operation (Execução de Campo)**: registra “o que foi executado”, com rastreabilidade e histórico

## Contexto
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real em campo
sem poluir o cadastro mestre e sem perder histórico.

## Consequências
- Operation referencia Registry; Registry não depende de Operation.
- O domínio será desenhado para suportar auditoria e evolução segura.