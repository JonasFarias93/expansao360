# ADR-046 — Serviço de validação e classificação de IP (MVP)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Adotar um **serviço de validação/classificação de IP** como contrato público no app `redes`,
com duas funções principais:

- `classificar_ip(perfil, base_ip, ip) -> ClassificationResult`
- `validar_ip_para_tipo(perfil, base_ip, ip, tipo) -> ValidationResult`

Os resultados retornam **severity** e **reason** padronizados, com `suggestion` opcional.

## Contexto
Regras de IP variam por perfil de rede da loja e por tipo de equipamento.
Esse comportamento precisa ser:

- centralizado (evitar regra espalhada em views/forms)
- testável (unit tests determinísticos)
- extensível (novos tipos e perfis sem quebrar contrato)

## Consequências
- Existe um contrato público estável para o domínio de redes.
- O serviço retorna objetos de resultado (não exceções) para facilitar UX e auditoria:
  - `ValidationResult(is_valid, reason, severity, suggestion?)`
  - `ClassificationResult(probable_tipo, severity, reason, suggestion?)`
- A evolução do MVP (novos tipos além de `TC`) ocorre adicionando reasons/regras,
  sem mudar o contrato das funções.