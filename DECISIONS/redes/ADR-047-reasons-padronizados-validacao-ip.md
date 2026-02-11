# ADR-047 — Reasons padronizados para validação/classificação de IP (MVP)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Padronizar o campo `reason` retornado pelo serviço de redes como **strings curtas, consistentes e testáveis**.

Reasons MVP:

- `INVALID_IP_FORMAT`
- `PREFIX_MISMATCH` (não pertence à loja)
- `NOT_IMPLEMENTED`

Regras `TC` (MVP):
- `TC_LEGACY_OK`
- `TC_LEGACY_REJECT_134`
- `TC_LEGACY_REJECT`
- `TC_SEGMENTADO_OK`
- `TC_SEGMENTADO_REJECT_11`
- `TC_SEGMENTADO_REJECT`

Warning:
- `TYPO_WARNING`

## Contexto
Sem reasons padronizados, a aplicação tende a:

- gerar mensagens inconsistentes
- dificultar assert de testes
- dificultar observabilidade (logs/analytics)
- misturar regra de negócio com texto de UI

O domínio precisa devolver *códigos* (reasons) e permitir que UI traduza isso.

## Consequências
- Testes automatizados validam `reason` (contrato forte).
- UI pode mapear reasons para mensagens amigáveis.
- Mudanças em texto de mensagem não quebram regra de negócio.
- Novos reasons devem ser adicionados de forma incremental e versionada via ADR.