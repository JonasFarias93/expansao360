# ADR-038 — Cor do Projeto para Identidade Visual na Fila Operacional

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
Adicionar ao cadastro de `Projeto` um campo `cor_slug`
(baseado em paleta fechada).

A fila operacional utiliza essa cor
para renderizar uma faixa visual no card do chamado.

## Contexto
Mapear cor por código diretamente no frontend:

- Não escala.
- Deixa projetos novos sem cor.
- Compromete consistência visual.

A cor precisa ser governada pelo próprio cadastro de Projeto.

## Consequências
- Migration no app `cadastro`.
- Form de Projeto expõe seleção de cor (paleta limitada).
- `execucao` apenas consome `projeto.cor_slug` para renderização.
- Centraliza identidade visual no domínio.