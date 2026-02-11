# ADR-023 — Adoção de Capability-Based Access Control (CBAC) na Camada Web

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Adotar um modelo de **Capability-Based Access Control (CBAC)**
na camada Web para controle de ações sensíveis.

A autorização passa a ser baseada em capacidades explícitas,
não apenas em papéis genéricos.

## Contexto
É necessário restringir ações como:

- Finalizar chamado
- Tomar sessão
- Editar referências contábeis
- Alterar estados críticos

Sem acoplar regras de permissão ao domínio.

O domínio deve permanecer permission-agnostic.

## Consequências
- O backend valida permissões via capabilities.
- Templates apenas refletem permissões (não decidem regras).
- O Core permanece independente de IAM.
- A camada Web atua como enforcement de autorização.
- Facilita auditoria e controle granular de acesso.