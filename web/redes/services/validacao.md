# Serviço de validação/classificação de IP (MVP)

## Contrato público

### classificar_ip(perfil, base_ip, ip) -> ClassificationResult
Retorna o tipo provável (MVP: apenas `TC`) e severidade.

Campos:
- `probable_tipo`: str | None
- `severity`: INFO | WARN | ERROR
- `reason`: string curta e consistente
- `suggestion`: opcional

### validar_ip_para_tipo(perfil, base_ip, ip, tipo) -> ValidationResult
Valida IP para um `tipo` (MVP: `tipo` é o `codigo` da regra).

Campos:
- `is_valid`: bool
- `reason`: string curta e consistente
- `severity`: INFO | WARN | ERROR
- `suggestion`: opcional

## Reasons padronizados (MVP)

- `INVALID_IP_FORMAT`
- `PREFIX_MISMATCH` (não pertence à loja)
- `NOT_IMPLEMENTED`
- `TC_LEGACY_OK`
- `TC_LEGACY_REJECT_134`
- `TC_LEGACY_REJECT`
- `TC_SEGMENTADO_OK`
- `TC_SEGMENTADO_REJECT_11`
- `TC_SEGMENTADO_REJECT`
- `TYPO_WARNING`

## Regras MVP

### Global
- Se prefixo /24 não bate com `base_ip` -> `ERROR / PREFIX_MISMATCH`

### TC (LEGACY_FLAT)
- aceita: finais `.11/.13/.14/.15`
- rejeita: `.134`

### TC (SEGMENTADO)
- aceita: `.134+`
- rejeita: `.11`

### Typo warning
- `.111` quando esperado `.11` -> `WARN / TYPO_WARNING` (não bloqueia)