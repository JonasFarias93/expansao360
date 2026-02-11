# ADR-035 — InstalacaoItem referencia TipoEquipamento via ForeignKey

**Data:** 2026-02-03  
**Status:** Aceito

## Decisão
Alterar o campo `InstalacaoItem.tipo` de string
para `ForeignKey` para `TipoEquipamento`.

## Contexto
Itens de cadastro (Registry) e execução precisam referenciar
o mesmo cadastro mestre para garantir:

- Consistência de nomenclatura
- Integridade referencial
- Filtros estáveis
- Regras operacionais confiáveis

O uso de string impedia governança adequada.

## Consequências
- Migração de schema.
- Ajuste na criação de itens (snapshot).
- Atualização de telas e serialização onde `tipo` era tratado como string.
- Possível migração de dados existentes.
- Maior coerência entre Registry e Execution.