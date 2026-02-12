# ADR-060 — Boundary final: `chamados` (workflow) vs `execucao` (sessão)

- **Data:** 2026-02-12
- **Status:** Aceito

## Decisão

Consolidar o split do domínio/fluxo de **Chamado** em um app dedicado (`chamados`), mantendo o app
`execucao` focado exclusivamente em **sessão/lock operacional** (ExecutionSession) e endpoints de sessão.

Durante a transição, manter compatibilidade com banco/migrations existentes usando:

- `Meta.app_label = "execucao"` nos models movidos fisicamente para `chamados/models.py`
- wrappers explícitos (sem `import *`) quando necessário para compatibilidade de imports
  (`execucao/forms.py`, `execucao/api_views.py`, `execucao/services/*`)

## Contexto

O app `execucao` acumulou responsabilidades de domínio, workflow, forms, endpoints e UI, além da
sessão exclusiva de execução. Isso aumentou acoplamento e risco de regressões, dificultando a evolução
do produto e o próximo passo planejado (migração/uso de Postgres com split real de tabelas/apps).

Já existiam decisões estabelecendo o domínio Chamado e a criação do app `chamados`:
- ADR-058 (Domain): Separação do Domínio Chamado do App Execucao
- ADR-059 (Architecture): Criar app Django dedicado para o domínio Chamados

Este ADR registra a **consolidação prática** do boundary final e o mecanismo de compatibilidade adotado.

## Consequências

### Positivas

- Boundary claro e coerente para evolução:
  - `chamados`: domínio + workflow + forms + endpoints + views do Chamado
  - `execucao`: sessão/lock + endpoints de abrir/tomar sessão
- Redução de acoplamento e melhora de manutenibilidade/testabilidade
- Base pronta para a próxima fase (Postgres) com menor risco operacional

### Negativas / Trade-offs

- Fase temporária com “mundo físico” diferente do “mundo lógico” (models em `chamados/` mas com
  `app_label="execucao"`), exigindo disciplina de imports e compat layers
- Parte da limpeza final (remover compat layers e alinhar app_label/tabelas) fica para a fase Postgres

### Boundary final (contrato)

#### `chamados/`
- Models: `Chamado`, `InstalacaoItem`, `ItemConfiguracaoLog`, `EvidenciaChamado` (+ enums/constantes)
- Services: workflow do chamado (`finalizacao`, `chamado_status`)
- Forms: forms do Chamado
- API: endpoints de lookup relacionados ao Chamado
- Views: workflow do Chamado (fila, histórico, setup, salvar, finalizar, evidências)

#### `execucao/`
- Models: `ExecutionSession`, `ExecutionSessionLog`
- Services: regras de sessão/lock (session workflow)
- Views: apenas `chamado_abrir` e `chamado_take_session`

### Próximo passo

Criar ADR específica e executar a migração Postgres para refletir o novo boundary no banco
(app_label/tabelas/FKs/ContentTypes), removendo gradualmente os wrappers de compatibilidade.