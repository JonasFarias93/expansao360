# ADR-045 — Introdução do status EM_CONFIGURACAO no workflow do Chamado

**Data:** 2026-02-10  
**Status:** Aceito

## Decisão
Adicionar o status `EM_CONFIGURACAO` ao workflow de `Chamado.Status`.

## Contexto
O PR5 introduz o conceito de item configurado:

- `InstalacaoItem.configurado_em`
- `InstalacaoItem.configurado_por`

O Chamado deve refletir explicitamente essa etapa do fluxo,
sem causar regressão nos demais estados.

## Consequências
- `Chamado.Status` passa a suportar `EM_CONFIGURACAO`.
- `recalcular_status()` pode promover:
  - `ABERTO / EM_EXECUCAO → EM_CONFIGURACAO`
    quando houver itens configurados.
- Estados de maior precedência
  (`AGUARDANDO_NF`, `AGUARDANDO_COLETA`)
  continuam prevalecendo.
- Workflow torna-se mais expressivo e auditável.