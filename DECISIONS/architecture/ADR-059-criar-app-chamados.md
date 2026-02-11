# ADR-059 — Criar app Django dedicado para o domínio Chamados

## Data
2026-02-11

## Status
Aceito

## Decisão
Criar o app Django `chamados` como base estrutural para isolar e evoluir o domínio Chamado,
reduzindo acoplamento com o app `execucao` e preparando a migração incremental.

## Contexto
O domínio Chamado possui regras próprias (ciclo de vida, gates, validações e ações operacionais).
Para sustentar o split planejado (ver ADR-058), é necessário materializar um boundary físico
no código, permitindo migração progressiva de modelos, serviços, views e URLs.

## Consequências
- Estrutura pronta para migração incremental sem interrupção do fluxo atual
- Melhor organização e ownership do domínio
- Exige disciplina para evitar import cycles e duplicação durante a transição