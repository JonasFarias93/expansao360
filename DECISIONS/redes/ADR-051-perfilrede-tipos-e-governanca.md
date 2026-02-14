# ADR-051 — PerfilRede como governança de perfis de rede (LEGACY_FLAT vs SEGMENTADO)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Introduzir a entidade de cadastro `PerfilRede` para representar perfis de rede governados pelo sistema,
incluindo um `tipo` padronizado via enum:

- `LEGACY_FLAT`
- `SEGMENTADO`

O `PerfilRede` é referenciado por regras de rede e pode ser desativado via `ativo`.

## Contexto
A validação e a classificação de IP dependem do perfil de rede adotado em uma loja/contexto.
Sem uma entidade explícita, o perfil tende a virar:

- string solta em fixtures
- ifs espalhados em serviços
- inconsistência de nomenclatura

## Consequências
- `PerfilRede` vira referência central para regras e validações de IP.
- O enum `PerfilRede.Tipo` normaliza as categorias de rede.
- Desativação (`ativo=False`) permite manter histórico sem deleção destrutiva.
- Ordenação por `codigo` facilita uso em selects/admin.