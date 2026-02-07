# STATUS — EXPANSÃO360

Este documento apresenta uma **visão executiva e técnica** do andamento do projeto,
organizada por **sprints** e **releases**, servindo como referência rápida para alinhamento,
onboarding e acompanhamento de evolução.

---

## Sprint Atual

**Sprint 4 — UX Operacional & Views**
📌 **Status:** 🟡 Em andamento
🏷 **Releases associados:** v0.3.1 → v0.3.5

### 🎯 Objetivo da Sprint

Evoluir a **experiência operacional** do sistema,
refinando UI, views e feedbacks visuais,
**sem alterações no core de domínio**.

Esta sprint foca exclusivamente em:

* clareza operacional
* redução de atrito na execução
* comunicação visual de status, prioridade e permissões
* consolidação de contratos de templates

---

### ✅ Entregas realizadas na Sprint 4

#### Registry (Cadastro Mestre)

* Importação **idempotente** de Lojas via CSV e XLSX (v0.3.1)
* Mapeamento operacional:

  * Filial → Java
  * Nome Filial → Nome loja
* Normalização automática de campos críticos:

  * UF em maiúsculo
  * Logomarca padronizada (uppercase / dropdown)
* UX aprimorada no cadastro e listagem de Lojas

#### Execução Operacional

* Separação explícita entre:

  * **Setup do Chamado** (`EM_ABERTURA`)
  * **Execução operacional** (`ABERTO` em diante)
* Reativação do bloco de **Evidências** na tela de execução
* Consolidação do fluxo de execução em fila operacional

#### UI / UX

* Projetos com **cor definida no cadastro**
* Fila operacional com **identificação visual por projeto**
* Header da fila com **cards-resumo interativos**
* Preview inline de detalhes do Chamado na fila
* Novo componente `_card_operacional_chamado_full.html`

#### Arquitetura

* Introdução de **templatetags de UI** (`execucao_ui`)
* Separação de responsabilidades em templates
* Refatoração incremental **sem quebra de compatibilidade**

#### Qualidade

* Testes automatizados adicionados para:

  * Views de execução
  * Template tags de UI
* Stack de qualidade ativa:

  * Ruff
  * Black
  * Pre-commit
* Integração de testes JS (Jest + jsdom) mantida

---

### 🔜 Pendências conhecidas da Sprint 4

* Refinar métricas visuais da fila (densidade e leitura rápida)
* Ajustar microcopy e feedbacks de erro na execução
* Avaliar próximos passos de UX para filtros avançados

---

## Sprint Anterior

**Sprint 3 — Fluxo Inverso e Evolução Operacional**
📌 **Status:** ✅ Concluída
🏷 **Release:** v0.3.0

### 🎯 Objetivo da Sprint

Consolidar o **core operacional** do EXPANSÃO360,
incluindo fluxo inverso, evidências, regras de exceção
e IAM mínimo por capability.

### ✅ Entregas

* Chamado com suporte a:

  * fluxo direto (Matriz → Loja)
  * fluxo inverso (Loja → Matriz)
* Regras completas de finalização e retorno
* Modelo de itens operacionais com rastreabilidade
* Evidências associadas à execução (anexos)
* IAM mínimo baseado em capabilities
* Views Web funcionais para execução operacional
* Testes automatizados cobrindo regras críticas

Encerramento formal do release **v0.3.0**.

---

## Sprint 2

**Sprint 2 — Cadastro e Execução Base (Web + CLI)**
📌 **Status:** ✅ Concluída

### 🎯 Objetivo da Sprint

Consolidar o **Cadastro Mestre (Registry)** e a
**Execução Base (Operation)**,
com testes automatizados e separação clara entre core, CLI e Web.

### ✅ Principais Entregas

* Core de domínio independente de framework
* CLI funcional para Registry e Operation
* Camada Web (Django) para:

  * Cadastro administrativo
  * Execução operacional
* Entidade Chamado com workflow e validações
* UI Web inicial para:

  * histórico
  * detalhe
  * edição de Chamados

---

## Observações Arquiteturais

* O core permanece **independente de framework**.
* Django atua exclusivamente como **camada de entrega (adapter)**.
* Nenhuma regra de negócio foi adicionada durante a Sprint 4.
* Evoluções estruturais exigem **ADR explícita** registrada em `DECISIONS.md`.

---

## Leitura complementar

* `README.md` — visão geral e onboarding
* `ARCHITECTURE.md` — contratos arquiteturais
* `DECISIONS.md` — histórico de decisões técnicas
* `CHANGELOG.md` — histórico de releases
