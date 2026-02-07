# Changelog — EXPANSÃO360

Todas as mudanças relevantes do projeto são documentadas neste arquivo.
O versionamento segue o padrão **SemVer**.

---

## [v0.3.5] — 2026-02-07

### Execução operacional mais clara

Este release consolida a **separação explícita entre setup e execução operacional**,
fecha lacunas de UX na fila e reforça contratos arquiteturais, sem quebra de compatibilidade.

### ✨ Execução

* Reativação do bloco de **Evidências** na tela de execução
* Separação clara entre **setup** e **execução operacional**
* Novo componente `_card_operacional_chamado_full.html`

### 🎨 UI / UX

* Projetos passam a possuir **cor definida no cadastro**
* Fila operacional com **identificação visual por projeto**
* Header e cards da fila mais informativos

### 🛠️ Arquitetura

* Introdução de **templatetags de UI** (`execucao_ui`)
* Contratos de templates respeitados
* Refatoração incremental sem quebra de compatibilidade

### 🧪 Qualidade

* Testes adicionados para:

  * Views de execução
  * Template tags de UI
* Ruff / Black / Pre-commit ativos

### 🔖 Notas

Esta versão consolida a transição do fluxo de execução e prepara o terreno
para evolução visual e operacional da fila.

---

## [v0.3.3] — 2026-02-04

### Fechamento da fase funcional (Cadastro + Execução + IAM)

Este release consolida a **fase funcional** do EXPANSÃO360, com Registry, Execução e IAM
estabilizados e cobertura de testes ampliada.

### ✨ Destaques

* Consolidação de **Registry (Cadastro)**, **Operation (Execução)** e **IAM**
* UI normalizada e cobertura de testes ampliada

### 🔄 Registry (Cadastro)

* Ajustes em models, forms, views e telas
* Correções e melhorias em formsets (kits e tipos)
* Migração incluída

### 🔄 Execução

* Consolidação de fluxos e regras operacionais
* Validações para fechamento de Chamados

### 🎨 UI

* Remoção de JS inline
* Normalização de templates base e sidebar

### 🧪 Testes

* Novos testes para AJAX e formsets
* Configuração do pytest consolidada

### 🧰 Front tooling

* Dependências e lockfile adicionados
* Alias `npm test` → `npm run test:js`

### 🔖 Notas

* Migração incluída: revisar e aplicar com cuidado em ambientes com dados

---

## [v0.3.2] — 2026-02-03

### Registry: Tipos de Equipamento por Categoria + UI

Este release consolida a padronização de **Tipos de Equipamento** como cadastro mestre
ligado à **Categoria**, eliminando texto livre e melhorando consistência histórica.

### ✨ Principais entregas

* `TipoEquipamento` vinculado à `Categoria` (1:N)
* Suporte a ativar/inativar tipos sem apagar histórico
* `ItemKit.tipo` migra de texto livre para FK (`PROTECT`)

### 🎨 UI de Categoria

* Edição de Categoria com Tipos inline (formset)
* Ajuda visual explicando estados (ativo/remover)

### 🛠️ Admin

* Ajustes no Django Admin para refletir os novos relacionamentos

### 🧪 Testes

* Cobertura de unicidade e comportamento de `TipoEquipamento`
* Ajustes por conta da migração de schema

### 🔖 Notas técnicas

* Migração adicionada (atenção em ambientes com dados existentes)
* Tipos antigos em texto precisam ser convertidos

### 📌 Por que isso importa

* Reduz inconsistência (ex.: "lcd", "LCD ", "Monitor LCD")
* Destrava filtros e relatórios confiáveis
* Mantém o Registry governado: Categoria → Equipamento → Tipo

---

## [v0.3.1] — 2026-02-02

### Importação de Lojas (CSV/XLSX) + UX do Cadastro

Este release evolui o **Cadastro Mestre (Registry)** com foco em realidade operacional
por meio de importação idempotente e refinamento de UI.

### ✨ Destaques

* Importação idempotente de Lojas via **CSV e XLSX**
* Mapeamento operacional:

  * Filial → Java
  * Nome Filial → Nome loja
* Normalização automática:

  * UF em maiúsculo
  * Logomarca padronizada (uppercase / dropdown)

### 🎨 UI

* Cadastro de Loja expandido (endereço e dados reais)
* Listagem de lojas aprimorada (colunas e ordenação)

### 🧪 Qualidade

* Testes cobrindo:

  * normalização de dados
  * idempotência do import
  * regras de padronização

### 🧾 Notas operacionais

```bash
python web/manage.py import_lojas web/data/imports/lojas/lojas_bases.csv
```

* Arquivos de import permanecem fora do versionamento

---

## [v0.2.0] — 2026-01-22

### Web v1 (Registry + Chamado)

Primeira versão utilizável end-to-end do EXPANSÃO360.

### ✨ Core + CLI

* Core de domínio independente de framework
* Casos de uso com TDD
* CLI funcional para Registry e Operation

### 🗂️ Web — Cadastro (Registry)

* Categoria, Equipamento, Loja, Projeto/Subprojeto
* Kit / ItemKit
* Admin configurado e migrations aplicadas

### 🧾 Web — Execução (Chamado)

* Entidade Chamado com protocolo automático
* Workflow de status
* Geração automática de itens de execução (snapshot)
* Validações de finalização

### 🎨 UI / Layout

* Layout base e estrutura de templates
* Tailwind via CDN
* Histórico e detalhe de Chamados

### 🔖 Observações

* Core permanece desacoplado de framework
* Django atua apenas como camada de entrega
* Decisões arquiteturais registradas via ADRs
