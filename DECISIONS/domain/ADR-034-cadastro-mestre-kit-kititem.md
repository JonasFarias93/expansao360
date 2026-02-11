# ADR-034 — Cadastro Mestre de Kit e KitItem (Registry)

**Data:** 2026-02-03  
**Status:** Aceito

## Decisão
Adicionar entidades de cadastro mestre no Registry:

- **Kit**: conjunto padronizado utilizado em fluxos operacionais.
- **KitItem**: itens que compõem um Kit, com quantidade e ordenação.

## Contexto
O fluxo de Chamados depende de kits padronizados,
que representam conjuntos estáveis de equipamentos utilizados em operação.

Como se trata de informação relativamente estável e reutilizável,
essas entidades pertencem ao **Registry (Cadastro Mestre)**,
não à camada de execução.

## Consequências
- A camada de Operation poderá referenciar `Kit`
  sem criar dependência inversa com o Registry.
- Integridade de `KitItem` é validada
  (quantidade mínima, ordenação consistente).
- CRUD exposto via Django (camada de entrega),
  mantendo regras de negócio fora das views.
- Base estruturada para geração de snapshot operacional no Chamado.