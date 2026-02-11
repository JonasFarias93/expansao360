# ADR-026 — Introdução de Subprojetos no Registry

**Data:** 2026-01-25  
**Status:** Aceito

## Decisão
Introduzir a entidade **Subprojeto** no Registry (Cadastro Mestre)
como recorte organizacional quando aplicável.

## Contexto
Projetos reais de expansão exigem segmentação operacional
por linhas de entrega ou frentes específicas.

Sem Subprojetos, o modelo ficaria excessivamente simplificado,
dificultando organização, relatórios e rastreabilidade.

## Consequências
- `Subprojeto` pertence ao Registry.
- Chamados podem referenciar um Subprojeto quando aplicável.
- Subprojetos não são deletados destrutivamente (preservação histórica).
- Permite relatórios e métricas segmentadas.
- Mantém separação entre estrutura organizacional e execução.