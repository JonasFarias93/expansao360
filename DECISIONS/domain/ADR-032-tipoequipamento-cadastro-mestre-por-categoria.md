# ADR-032 — TipoEquipamento como Cadastro Mestre por Categoria

**Data:** 2026-02-03  
**Status:** Aceito

## Decisão
Criar a entidade `TipoEquipamento` como parte do Registry,
vinculada obrigatoriamente a uma `Categoria`.

Essa entidade substitui o uso de texto livre
em itens de Kit e fluxos operacionais.

## Contexto
O uso de texto livre para representar tipos de equipamento gerava:

- Inconsistência de nomenclatura
- Dificuldade de histórico
- Problemas de filtro e relatório
- Falta de integridade referencial

Era necessário elevar o conceito de tipo para cadastro mestre governado.

## Consequências
- Criação de novo model `TipoEquipamento`.
- Migração de schema.
- Atualização de forms e testes.
- Integridade referencial garantida via FK.
- Redução de inconsistência e ambiguidade.