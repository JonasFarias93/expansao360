# ADR-052 — RegraRedeEquipamento por perfil (unicidade perfil + codigo)

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Modelar regras de rede por tipo de equipamento como entidade `RegraRedeEquipamento`,
relacionada a um `PerfilRede` (FK `PROTECT`), com unicidade garantida por:

- `perfil_rede` + `codigo`

## Contexto
As regras de IP variam conforme:

- tipo de equipamento (`codigo`: ex.: `PDV`, `TC`, `CONSULTA_PRECO`)
- perfil de rede (LEGACY_FLAT / SEGMENTADO)

É necessário permitir múltiplas regras para o mesmo `codigo` em perfis diferentes,
mas impedir duplicidade dentro do mesmo perfil.

## Consequências
- Unicidade via constraint: `uniq_regra_rede_equipamento_por_perfil_codigo`.
- `on_delete=PROTECT` preserva histórico e evita apagar perfil com regra vinculada.
- Permite extensões futuras sem mudar contrato do serviço:
  - novos tipos
  - novos perfis
  - novas políticas de IP