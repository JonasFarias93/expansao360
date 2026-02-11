# Serviço de Validação/Classificação de IP (MVP)

Este documento descreve o **contrato público atual (MVP)** do serviço de
validação e classificação de IP do domínio `redes`.

⚠️ Este é o comportamento **as-is** implementado em código.
Evoluções estruturais exigem ADR.

---

## Source of Truth

- Implementação: `web/redes/services/validacao.py`
- Testes: `web/redes/tests/test_validacao_ip.py`
- ADRs relacionados:
  - ADR-046 — Serviço de validação/classificação de IP
  - ADR-047 — Reasons padronizados
  - ADR-048 — Regra global de prefixo da loja
  - ADR-049 — Regras MVP TC (legacy vs segmentado)
  - ADR-050 — Typo warning não bloqueante

---

# 1. Contrato Público

## 1.1 classificar_ip(perfil, base_ip, ip) -> ClassificationResult

Responsável por determinar o **tipo provável** da regra aplicável ao IP.

No MVP, o único tipo suportado é: `TC`.

### Retorno: ClassificationResult

Campos:

- `probable_tipo: str | None`  
  Tipo provável identificado (ex.: `"TC"`).  
  Pode ser `None` quando não classificável.

- `severity: INFO | WARN | ERROR`  
  Nível de severidade associado à classificação.

- `reason: str`  
  Reason padronizado (`REASON_*`).

- `suggestion: str | None`  
  Sugestão opcional para correção.

---

## 1.2 validar_ip_para_tipo(perfil, base_ip, ip, tipo) -> ValidationResult

Valida um IP para um tipo específico.

No MVP, `tipo` corresponde ao `codigo` da regra (ex.: `"TC"`).

### Retorno: ValidationResult

Campos:

- `is_valid: bool`  
  Indica se o IP é válido para a regra informada.

- `reason: str`  
  Reason padronizado (`REASON_*`).

- `severity: INFO | WARN | ERROR`

- `suggestion: str | None`

---

# 2. Reasons Padronizados (MVP)

Todos os reasons abaixo estão definidos em:

`web/redes/services/validacao.py`

---

## 2.1 Gerais

- `INVALID_IP_FORMAT`  
  IP não parseável ou formato inválido.

- `PREFIX_MISMATCH`  
  IP não pertence ao prefixo base da loja (`/24`).

- `NOT_IMPLEMENTED`  
  Regra/tipo ainda não implementado no serviço.

---

## 2.2 TC — LEGACY

- `TC_LEGACY_OK`  
  IP válido segundo regras legacy.

- `TC_LEGACY_REJECT_134`  
  Caso específico rejeitado (final `.134`).

- `TC_LEGACY_REJECT`  
  Qualquer IP fora das faixas aceitas que não seja o caso especial `.134`.

---

## 2.3 TC — SEGMENTADO

- `TC_SEGMENTADO_OK`  
  IP válido segundo regra segmentada.

- `TC_SEGMENTADO_REJECT_11`  
  Caso específico rejeitado (final `.11`).

- `TC_SEGMENTADO_REJECT`  
  Qualquer IP fora das faixas aceitas que não seja o caso especial `.11`.

---

## 2.4 Qualidade / Typo

- `TYPO_WARNING`  
  Indica provável erro de digitação (ex.: `.111` quando esperado `.11`).

⚠️ Importante:  
`TYPO_WARNING` é **WARN e não bloqueante** no MVP.

---

# 3. Regras MVP

## 3.1 Regra Global (Prefixo da Loja)

Antes de qualquer validação específica:

- Se o prefixo `/24` do IP não corresponde ao `base_ip` da loja:
  - `severity = ERROR`
  - `reason = PREFIX_MISMATCH`
  - `is_valid = False`

Essa regra é estrutural e sempre aplicada.

---

## 3.2 TC — LEGACY_FLAT

Aceita finais:

- `.11`
- `.13`
- `.14`
- `.15`

Rejeita explicitamente:

- `.134` → `TC_LEGACY_REJECT_134`

Outros finais fora da regra:

- `TC_LEGACY_REJECT`

---

## 3.3 TC — SEGMENTADO

Aceita:

- `.134` e superiores (conforme regra do serviço)

Rejeita explicitamente:

- `.11` → `TC_SEGMENTADO_REJECT_11`

Outros finais fora da regra:

- `TC_SEGMENTADO_REJECT`

---

## 3.4 Typo Warning

Caso detectado:

- `.111` quando esperado `.11`

Retorno:

- `severity = WARN`
- `reason = TYPO_WARNING`
- `is_valid = True`

⚠️ Não bloqueia no MVP.

---

# 4. Limitações do MVP

- Apenas o tipo `TC` é suportado.
- Não há integração automática com `TipoEquipamento` do cadastro.
- Não há bloqueio automático em telas de execução (depende do fluxo).

Evoluções futuras devem respeitar ADRs existentes.

---

# 5. Cobertura de Testes

Arquivo:

`web/redes/tests/test_validacao_ip.py`

Cenários cobertos:

- TC legacy OK
- TC legacy reject 134
- TC segmentado OK
- TC segmentado reject 11
- Prefix mismatch
- Typo warning

---

Última revisão: 2026-02-11  
Source of truth:
- web/redes/services/validacao.py  
- web/redes/tests/test_validacao_ip.py