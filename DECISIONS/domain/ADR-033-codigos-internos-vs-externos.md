# ADR-033 — Padronização de Códigos (Internos vs Externos)

**Data:** 2026-02-03  
**Status:** Proposto

## Decisão
Diferenciar explicitamente dois tipos de identificadores no sistema:

- **Códigos externos** (ex.: Loja/Java) — manuais ou importados.
- **Códigos internos** (ex.: Equipamento, TipoEquipamento) — automáticos e governados pelo sistema.

## Contexto
Sem uma distinção clara, há risco de confusão entre:

- Identificadores operacionais usados por sistemas externos e usuários
- Identificadores internos usados para governança e integridade do Registry

Isso afeta UX, testes, integrações e consistência de dados.

## Consequências
- A UI trata códigos conforme seu tipo:
  - externos: entrada/importação, validações de formato, não necessariamente imutáveis
  - internos: somente leitura (quando aplicável), geração automática
- Testes específicos por categoria de código.
- Maior clareza e segurança para integrações.
- Redução de ambiguidade em documentação e onboarding.