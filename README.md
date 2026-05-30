# EXPANSÃO360

Plataforma para gestão de expansão, padronização e **operação de campo**,
com separação rigorosa entre **Cadastro Mestre (Registry)** e **Execução Operacional (Operation)**,
garantindo **rastreabilidade, histórico e governança de ponta a ponta**.

---

## 🚀 Release Atual

**v0.4.0 — PostgreSQL como banco padrão (Dev/CI)**

Veja detalhes em `CHANGELOG.md`.

Sprint atual: **Sprint 4 — UX Operacional & Views**

Status detalhado em `STATUS.md`.

---

## 🎯 Objetivo

Estruturar e padronizar a expansão de operações físicas,
assegurando que o planejamento (Registry) seja executado corretamente em campo (Operation),
com evidências, histórico auditável e regras explícitas.

O sistema evita:

* Perda de histórico
* Edições destrutivas de execução
* Inconsistência entre planejamento e operação
* Falta de governança em fluxos de retorno e exceção

---

## 🧱 Conceito Central

### Registry (Cadastro Mestre)

Define **o que existe** e **como deve ser padronizado**.

Exemplos:

* Lojas
* Projetos / Subprojetos
* Equipamentos
* Categorias e Tipos de Equipamento
* Kits

Características:

* Fonte da verdade
* Alterações impactam apenas execuções futuras
* Não registra execução

---

### Operation (Execução)

Registra **o que foi executado**, **quando**, **por quem** e **com quais evidências**.

Exemplos:

* Chamados
* Itens de Execução (snapshot)
* Evidências
* Fluxos direto e inverso

Características:

* Histórico imutável
* Rastreabilidade completa
* Não altera cadastro mestre

---

## 📌 Conceito-chave: Chamado

Unidade central da execução operacional.

* Representa evento real
* Possui ciclo de vida explícito
* Finalizado = imutável
* Correções geram novo Chamado

Estados principais:

1. `EM_ABERTURA` (setup)
2. `ABERTO` (entra na fila)
3. `EM_EXECUCAO` / `AGUARDANDO_*`
4. `FINALIZADO`

Chamados em `EM_ABERTURA` **não aparecem na fila operacional**.

---

## 🛡️ Gates Operacionais

Avanço de status protegido por regras:

* Liberação de NF exige itens rastreáveis bipados e contáveis confirmados
* Finalização exige NF (quando aplicável) + coleta + evidências mínimas

Regras implementadas no backend e cobertas por testes.

---

## 🖥️ Como Rodar o Projeto (Dev)

### Pré-requisitos

* Git
* Conda (Miniforge / Miniconda)
* Docker + Docker Compose (PostgreSQL local)
* Node (para testes JS)

---

## 🔧 Ambiente e Rebuild

O projeto utiliza:

* `environment.yml` → definição do ambiente Conda
* `pyproject.toml` → dependências Python
* `Makefile` → interface oficial de setup e rebuild (ver ADR-062)

> **Nota:** os comandos `make` abaixo assumem que o ambiente Conda se chama `expansao360`.

### Criar ambiente

```bash
make env-create
```

### Instalar dependências

```bash
make deps-install
```

### Rebuild limpo completo

```bash
make rebuild-clean
```

### Rodar checks

```bash
make check
```

---

## 🐘 Banco PostgreSQL (local via Docker)

### 1) Criar `.env`

Copie o exemplo e ajuste se necessário:

```bash
cp .env.example .env
```

Variáveis mínimas esperadas:

* `DB_ENGINE=postgres`
* `DB_HOST=localhost`
* `DB_PORT=5432`
* `DB_NAME=expansao360`
* `DB_USER=expansao360`
* `DB_PASSWORD=expansao360`

> O arquivo `.env` **não deve ser commitado**.

### 2) Subir o banco

Na raiz do projeto:

```bash
docker compose up -d
docker compose ps
```

Aguarde o serviço `db` ficar `healthy`.

### 3) Aplicar migrations

```bash
python web/manage.py migrate
```

---

### 4) Popular dados de dev

```bash
make seed-dev
```

> Cria dados mínimos para testar o fluxo completo.
> Idempotente — pode rodar múltiplas vezes.
> User criado: `dev` / senha: `dev123`


## ▶️ Rodar servidor

```bash
python web/manage.py runserver
```

---

## ♻️ Reset do banco (modo dev)

Remove volume e recria do zero:

```bash
docker compose down -v
docker compose up -d
python web/manage.py migrate
```

---

## 🧯 Troubleshooting (Postgres)

* **Conexão falhando logo após `up -d`**: aguarde `healthy` e rode novamente `migrate`.
* **Porta 5432 ocupada**: altere `DB_PORT` no `.env` e suba novamente.
* **Banco “sujo” ou migrations quebradas**: use o reset do banco (`down -v`).

---

## 🧪 Como Rodar Testes

### Python (pytest)

```bash
pytest -q
```

> A suíte deve rodar em PostgreSQL local.

### JavaScript (Jest)

```bash
npm install
npm run test:js
```

Testes JS ficam em:

```txt
web/cadastro/static/cadastro/js/__tests__/
```

---

## 🧩 Web (Django)

Apps principais:

* `cadastro` → Registry
* `execucao` → Operation
* `chamados` → Workflow/fluxo do Chamado (boundary)
* `iam` → Capabilities
* `redes` → Regras de validação de IP (MVP)

A Web atua como **adapter**, não como domínio.

---

## 📚 Documentação

* `ARCHITECTURE.md` → visão arquitetural
* `REQUIREMENTS.md` → requisitos funcionais e não funcionais
* `SECURITY.md` → diretrizes de segurança
* `GLOSSARIO.md` → terminologia oficial
* `STATUS.md` → visão executiva por sprint
* `CHANGELOG.md` → histórico de releases

Documentação operacional adicional em:

```txt
docs/
```

Decisões arquiteturais (ADRs) em:

```txt
DECISIONS/
```

---

## 📦 Snapshots de Dependências

Arquivos como `_env_dump.yml` e `_pip_dump.txt` são tratados como **artefatos gerados**, não como fonte de verdade.

A fonte oficial de dependências permanece:

* `pyproject.toml` → dependências Python
* `environment.yml` → base Conda (python + libs nativas)

Para gerar snapshots do ambiente atual:

```bash
make deps-snapshot
```

Snapshots podem ser:

* Versionados em `docs/deps/` para auditoria
  **ou**
* Ignorados via `.gitignore`, caso sejam usados apenas localmente

Eles **não devem** ser editados manualmente.

---

## 🧠 Princípios

* Histórico é sagrado
* Planejamento ≠ Execução
* Correções geram novos eventos
* Regras explícitas > comportamento implícito
* Evolução incremental e rastreável

---

**Última revisão:** 2026-02-13
**Fonte:** Código real em `web/` + `CHANGELOG.md` + `STATUS.md`
