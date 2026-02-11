# ADR-049 — Regras MVP para tipo TC por perfil de rede (LEGACY vs SEGMENTADO)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Definir regras MVP para o tipo `TC` (MVP: único tipo classificado/validado inicialmente),
variando conforme o perfil de rede.

### TC (LEGACY_FLAT)
- aceita finais: `.11`, `.13`, `.14`, `.15`
- rejeita explicitamente: `.134`
- demais casos: rejeitar (`TC_LEGACY_REJECT`)

### TC (SEGMENTADO)
- aceita: `.134+`
- rejeita explicitamente: `.11`
- demais casos: rejeitar (`TC_SEGMENTADO_REJECT`)

## Contexto
A transição de rede “flat” para “segmentada” altera o range esperado de IP por tipo.
O sistema precisa refletir isso de forma explícita e testável.

Começar pelo tipo `TC` permite validar o modelo e o contrato do serviço
antes de expandir para outros tipos.

## Consequências
- Regras são determinísticas e cobertas por unit tests.
- Perfis de rede passam a ter impacto real no comportamento do serviço.
- Base pronta para adicionar novos tipos (ex.: impressoras, PDVs etc.) via ADRs futuras.