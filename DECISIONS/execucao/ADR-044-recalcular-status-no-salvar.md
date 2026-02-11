# ADR-044 — Recalcular status automaticamente no Salvar (Execução)

**Data:** 2026-02-09  
**Status:** Aceito

## Decisão
Implementar o service `execucao.services.chamado_status.recalcular_status(chamado)`
como regra central de promoção automática de status no gatilho **Salvar**
(fora do fluxo de Finalizar).

## Contexto
O progresso salvo (itens / contábil / NF) deve promover status sem intervenção manual,
permitindo continuidade por outro técnico e padronizando o fluxo operacional.

Sem uma função central, a promoção de status tende a ficar dispersa em views/forms,
aumentando risco de inconsistência.

## Consequências
- Promoções automáticas:
  - `ABERTO → EM_EXECUCAO` (primeiro salvar)
  - `contábil + pode_liberar_nf() → AGUARDANDO_NF`
  - `nf_saida_numero → AGUARDANDO_COLETA`
- Sem regressão de status neste PR.
- Função idempotente e coberta por testes unitários.
- Regras de promoção ficam centralizadas em um único ponto.