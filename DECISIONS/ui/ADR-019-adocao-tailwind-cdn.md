# ADR-019 — Adoção de Tailwind via CDN e Estrutura Base de Templates

**Data:** 2026-02-03  
**Status:** Aceito

## Decisão
Adotar Tailwind CSS via CDN como base de estilização do projeto,
utilizando uma estrutura organizada de templates:

- `base`
- `partials`
- `components`

Sem introduzir pipeline de build frontend neste estágio.

## Contexto
Era necessário padronizar a UI desde o início do projeto,
sem introduzir complexidade adicional de build (Node, bundlers,
compilação de assets).

Optou-se por usar Tailwind via CDN para:

- Agilidade inicial
- Redução de setup
- Consistência visual

## Consequências
- UI padronizada desde as primeiras telas.
- Estrutura clara de templates (base + componentes).
- Evita HTML duplicado e decisões visuais ad-hoc.
- Não há etapa de build frontend neste momento.
- Dependência futura de possível migração para build local
  caso o projeto cresça em complexidade visual.