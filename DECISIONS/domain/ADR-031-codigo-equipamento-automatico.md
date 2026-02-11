# ADR-031 — Código de Equipamento Gerado Automaticamente

**Data:** 2026-02-03  
**Status:** Aceito

## Decisão
O campo `Equipamento.codigo` passa a ser:

- Gerado automaticamente
- Único
- Normalizado
- Imutável após criação

## Contexto
Identificadores inseridos manualmente geravam:

- Inconsistência
- Erros humanos
- Duplicidade
- Problemas em relatórios e integrações

O código do equipamento é utilizado no dia a dia operacional
e precisa ser confiável e estável.

## Consequências
- A lógica de geração passa a viver no model.
- O campo pode ser oculto ou somente leitura na UI.
- Garantia de unicidade via constraint.
- Testes cobrindo:
  - Geração correta
  - Colisão
  - Imutabilidade após persistência
- Maior segurança para integrações e relatórios.