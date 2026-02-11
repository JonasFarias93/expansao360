# ADR-040 — Cards-resumo interativos na Fila Operacional

**Data:** 2026-02-06  
**Status:** Aceito

## Decisão
Adicionar um header na tela de **Fila Operacional**
contendo cards-resumo clicáveis para:

- Total de chamados na fila
- Quantidade por prioridade (Crítico / Alto / Médio / Baixo)

Os cards funcionam também como filtro rápido
via querystring (`?prio=CRITICO|ALTO|MEDIO|BAIXO`).

## Contexto
A fila operacional precisa oferecer leitura imediata
da carga de trabalho e reduzir o custo de localizar chamados.

A UI já utiliza cards e ações rápidas,
mas faltava uma visão agregada e mecanismo direto de filtragem.

## Consequências
- A view da fila passa a expor:
  - contadores agregados (`counts`)
  - filtro atual (`prio_selected`)
- A filtragem é stateless (URL), facilitando:
  - compartilhamento
  - testes automatizados
- O template permanece simples:
  - apenas renderiza
  - regras de filtro e agregação ficam na view
- Evolução futura prevista:
  - filtros adicionais (ex.: por projeto)
  - nova ADR quando aplicável