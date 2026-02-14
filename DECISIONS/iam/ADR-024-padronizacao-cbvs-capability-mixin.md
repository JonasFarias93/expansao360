# ADR-024 — Padronização de CBVs + CapabilityRequiredMixin

**Data:** 2026-01-24  
**Status:** Aceito

## Decisão
Padronizar views críticas utilizando Class-Based Views (CBVs)
e centralizar a autorização em um `CapabilityRequiredMixin`.

## Contexto
Durante a Sprint 3 (Execução / Fluxo inverso / IAM),
foi identificado que:

- Views baseadas em função geravam repetição de código.
- Regras de autorização estavam dispersas.
- Não havia padrão claro de enforcement de capabilities.

Era necessário estabelecer uma base consistente para:

- Execução operacional
- Tomada de sessão
- Ações sensíveis do fluxo

## Consequências
- Views críticas passam a utilizar CBVs.
- Autorização é centralizada via `CapabilityRequiredMixin`.
- Redução de repetição de código.
- Padrão consistente de autorização.
- Migração incremental segura de views existentes.