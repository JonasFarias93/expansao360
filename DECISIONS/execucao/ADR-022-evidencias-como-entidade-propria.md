# ADR-022 — Evidências como Entidade Própria vinculada ao Chamado

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Evidências passam a ser modeladas como entidades próprias
vinculadas a `Chamado`.

## Contexto
Documentos como:

- NF
- Carta de Conteúdo
- Documentos de exceção
- Fotos
- Assinaturas

fazem parte do processo operacional real e não devem ser apenas
campos dispersos no modelo do Chamado.

O sistema precisa refletir o caráter auditável desses artefatos.

## Consequências
- Finalização pode exigir evidência.
- Auditoria é fortalecida.
- Modelo torna-se extensível (novos tipos de evidência).
- Evidências possuem ciclo de vida próprio.
- Reduz acoplamento de dados contábeis diretamente no Chamado.