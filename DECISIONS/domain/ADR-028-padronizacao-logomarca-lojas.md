# ADR-028 — Padronização de Logomarca no Cadastro de Lojas

**Data:** 2026-02-02  
**Status:** Aceito

## Decisão
Padronizar o campo **Logomarca** no cadastro de Lojas:

- Normalizar o valor para maiúsculo.
- Preferir uso de dropdown no cadastro manual.

## Contexto
Valores inseridos manualmente geravam divergências como:

- RAIA
- raia
- RaIa

Essa inconsistência compromete relatórios, filtros e integridade visual.

## Consequências
- Redução de inconsistência de dados.
- UI mais segura via seleção controlada.
- Lógica de normalização implementada no model ou form.
- Testes cobrindo normalização e persistência correta.
- Maior previsibilidade para relatórios e integrações.