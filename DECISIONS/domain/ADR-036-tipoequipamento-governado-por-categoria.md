# ADR-036 — TipoEquipamento só existe no contexto de uma Categoria

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
O cadastro de `TipoEquipamento` deve acontecer exclusivamente dentro do fluxo de `Categoria`
(inline no update da Categoria). Não haverá criação “solta” de Tipo sem Categoria.

## Contexto
Tipos sem Categoria (ou Categorias sem Tipos mínimos) geram:

- selects vazios
- inconsistência na abertura de Chamados
- fragilidade no uso do Registry

Como `TipoEquipamento` é cadastro mestre, ele deve ser governado por `Categoria`
para garantir consistência.

## Consequências
- UI: fluxo padrão é **criar Categoria → cadastrar Tipos** (na mesma tela).
- Evita cadastro de Tipo sem Categoria e reduz “tipos vazios” no Chamado.
- Testes de view devem cobrir:
  - atualização de Categoria com formset de Tipos
  - validações mínimas
- Qualquer quick-create deve garantir Categoria persistida antes de permitir Tipos.