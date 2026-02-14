# ADR-005 — Stack web definida: Django

**Data:** 2026-01-21  
**Status:** Aceito

## Decisão
A camada web do EXPANSÃO360 será implementada utilizando Django.

## Contexto
Após a estabilização do core e da CLI, foi necessário definir um framework web
para fornecer interface de usuário, autenticação, persistência e administração.
Django foi escolhido pela maturidade, ecossistema, ORM integrado e velocidade
de entrega para CRUDs e RBAC.

## Consequências
- O core permanece independente de framework.
- Django atua apenas como camada de entrega (web/adapters).
- Models Django não contêm regras de negócio.