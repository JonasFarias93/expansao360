# ADR-029 — Refinamento do Cadastro de Equipamentos (Registry)

**Data:** 2026-02-02  
**Status:** Aceito

## Decisão
Equipamentos são tratados como entidade de **Registry** (Cadastro Mestre),
com foco em padronização e reutilização operacional.

## Contexto
O CRUD inicial não refletia o uso real do cadastro nem as validações necessárias,
gerando risco de inconsistência e retrabalho.

Era necessário alinhar o cadastro ao papel de governança do Registry,
seguindo o padrão aplicado em Lojas.

## Consequências
- Ajustes em model, form, testes e UI.
- Possível migração de dados (quando existirem registros persistidos).
- Padronização de campos e validações.
- Reuso de padrões de UX e consistência adotados em Lojas.
- Base mais estável para execução e relatórios.