# ADR-048 — Regra global: IP deve pertencer ao prefixo da loja (base_ip)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Antes de aplicar qualquer regra por tipo/perfil, validar regra global:

- Se o prefixo **/24** do `ip` não bate com o `base_ip` da loja:
  - retornar `ERROR / PREFIX_MISMATCH`

## Contexto
Mesmo que um IP “pareça válido” para um tipo, ele não pode ser aceito se:

- não pertence à rede da loja
- foi digitado/copied do lugar errado
- está apontando para outro ambiente

A validação do pertencimento ao prefixo deve ser a primeira barreira.

## Consequências
- A validação falha cedo e de forma determinística.
- Evita falsos positivos na classificação por tipo.
- Reduz risco operacional (IP fora da loja).
- Mantém consistência do serviço: regra global sempre precede regras específicas.