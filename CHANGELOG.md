# Changelog — EXPANSÃO360

Todas as mudanças relevantes do projeto são documentadas neste arquivo.
O versionamento segue o padrão **SemVer**.

---

## [v0.6.0] — 2026-05-31

### Sprint Operacional — Correções, Novos Apps e UX

Esta release consolida um ciclo completo de melhorias incrementais sobre a base v0.5.0,
com foco em correção de bugs críticos de rastreabilidade, novos apps de domínio
e melhorias de experiência operacional.

---

### 🐛 Bug Fixes

#### Fila Operacional
* Corrigido bug onde chamados desapareciam da fila após configuração de itens
* `EM_CONFIGURACAO` removido do `recalcular_status` — configuração é estado de item, não de chamado
* Testes de regressão adicionados para garantir que chamados permanecem na fila durante todo o ciclo

#### Snapshot Operacional
* Corrigida propagação de `requer_configuracao` → `deve_configurar` no snapshot do chamado
* Itens configuráveis do Kit agora chegam corretamente na fila operacional com `deve_configurar=True`

#### Evidências
* Corrigido erro 403 (CSRF) ao enviar evidências no chamado
* Adicionado `ensure_csrf_cookie` na `ChamadoExecucaoView`
* Removido `only` do include que bloqueava o token CSRF

#### Template
* Corrigido `ev.nome_arquivo` inexistente — substituído por `ev.descricao`

---

### ✨ Features

#### seed_dev — Dados de Desenvolvimento
* Novo management command `python web/manage.py seed_dev`
* Popula dados mínimos para testar o fluxo completo (loja, projeto, kit, equipamento, usuário)
* Idempotente — pode rodar múltiplas vezes sem duplicar dados
* Suporte a `--reset` para limpar e recriar tudo
* Usuário `dev` criado com capabilities básicas
* Disponível via `make seed-dev` e `make seed-dev-reset`

#### Cancelamento de Chamado
* Novo status `CANCELADO` no ciclo de vida do chamado
* Campos auditáveis: `cancelado_em`, `cancelado_por`, `motivo_cancelamento`
* Botão de cancelar na tela de execução (protegido por `data-skip-readonly`)
* Motivo obrigatório — não é possível cancelar sem justificativa
* Capability `execucao.chamado.cancelar` protege a ação
* Service `cancelar_chamado` com regras explícitas e 7 testes

#### UX Operacional
* Botão "Editar IP" protegido por `can_edit` (requer sessão ativa)
* Botão "Salvar IP" adicionado no modo edição — sem precisar salvar todos os itens
* Removidos botões de status de configuração (`Aguardando`, `Em execução`, `Configurado`)
* Mantido apenas o botão "Marcar configurado"
* Resumo de equipamentos na sidebar do chamado (agrupado por nome)
* TAB behavior para leitura de código de barras — após série, vai direto para o próximo ativo

---

### 🏗️ Novos Apps

#### `historico/` — Memória Auditável
* `HistoricoExecucao` — snapshot imutável consolidado de cada chamado finalizado/cancelado
* `HistoricoAtivoTimeline` — linha do tempo de ativos rastreáveis
* Signal automático: ao finalizar ou cancelar chamado, projeção é gerada
* Service `gerar_historico_execucao` idempotente
* Views: detalhe do chamado, histórico da loja, timeline do ativo
* Página de busca centralizada com filtros por protocolo, loja e ativo
* Link "Histórico & Auditoria" no menu lateral
* 6 testes cobrindo projeção, idempotência e timeline

#### `users/` — Identidade Operacional
* `UserProfile` — contexto operacional do usuário (perfil, status, equipe, supervisor)
* Status operacional: `ATIVO`, `AFASTADO`, `BLOQUEADO`, `DESLIGADO`
* Perfis: `TECNICO`, `COORDENADOR`, `LOGISTICA`, `AUDITOR`, `ADMINISTRADOR`
* `OperationalAuthBackend` — bloqueia login de usuários inativos
* UI completa: lista, detalhe, criação, edição de perfil
* Gerenciamento de capabilities por usuário via interface web
* Link "Usuários" no menu lateral
* `iam/mixins.py` atualizado com bypass para superuser
* 9 testes cobrindo profile e autenticação operacional

---

### 🔄 Changed

* `views.py` de chamados reorganizado por seção lógica (abertura → fila → execução → workflow → itens → configuração → finalização → cancelamento → evidências)
* `iam/mixins.py` — superuser bypassa verificação de capability
* `seed_dev` — equipamento criado com `configuravel=True`
* `seed_dev --reset` — ordem correta de deleção respeitando FKs protegidas

---

### 🧪 Quality

* 189 testes passando (era 160 na v0.5.0)
* TDD respeitado em todas as features críticas
* Nenhuma regressão conhecida

---

## [v0.5.0] — 2026-02-14

### Consolidação Arquitetural

* Split definitivo de domínios: `chamados`, `execucao`, `redes`, `iam`
* State Manager centralizado com contrato `data-*`
* Fluxo Salvar → Encerrar Sessão consistente
* Suíte de testes padronizada e organizada por domínio
* 160 testes passando

---

## [v0.4.1] — 2026-02-14

### Changed

* Reset estrutural de migrations após split definitivo
* Remoção de duplicidade de templatetags
* Alinhamento de admin ao boundary de domínio

### Internal

* Boundary final: chamados = domínio / execucao = sessão/fila
* pytest 160 passed / 1 skipped
* manage.py check limpo

---

## [v0.4.0] — 2026-02-13

### PostgreSQL como banco padrão

* PostgreSQL definido como banco oficial
* Configuração via variáveis de ambiente
* docker-compose com healthcheck
* CI ajustado para Postgres obrigatório
* Novo target `make compose-smoke`

---

## [v0.3.6] — 2026-02-08

### Lookup de Loja por Código (Java)

* Endpoint de lookup assíncrono de loja
* Novo input "Loja (Java)" no Abrir Chamado
* Validação server-side + proteção contra ID inválido
* Testes: 200, 404, 400

---

## [v0.3.5] — 2026-02-07

### Execução operacional mais clara

* Separação explícita entre setup e execução
* Reativação de evidências
* Projetos com cor definida
* Cards-resumo na fila operacional
* Introdução de templatetags (`execucao_ui`)

---

## [v0.3.3] — 2026-02-04

### Consolidação funcional (Cadastro + Execução + IAM)

* Registry, Operation e IAM estabilizados
* UI normalizada
* Cobertura de testes ampliada

---

## [v0.3.2] — 2026-02-03

### Tipos de Equipamento por Categoria

* `TipoEquipamento` vinculado à `Categoria`
* Ativar/inativar tipos sem apagar histórico
* `ItemKit.tipo` migra de texto livre para FK

---

## [v0.3.1] — 2026-02-02

### Importação de Lojas (CSV/XLSX)

* Import idempotente
* Normalização automática (UF, logomarca)
* UX aprimorada na listagem

---

## [v0.3.0] — 2026-01-30

### Fluxo Inverso e Consolidação Operacional

* Suporte a fluxo direto e inverso
* Regras completas de finalização
* Evidências associadas
* IAM mínimo por capability

---

## [v0.2.0] — 2026-01-22

### Web v1 (Registry + Chamado)

* Core independente de framework
* CLI funcional
* Cadastro via Web
* Chamado com protocolo automático
* Snapshot operacional de itens
* Workflow básico

---

Última revisão: 2026-05-31
Fonte: Tags Git + código versionado