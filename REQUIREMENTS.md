# REQUIREMENTS — EXPANSÃO360

Este documento descreve os requisitos **funcionais**, **não funcionais** e **restrições técnicas** do EXPANSÃO360,
alinhados com o comportamento real do sistema (as-is).

Fontes de verdade:

* Código em `web/`
* Testes automatizados (`tests/` e `web/*/tests/`)
* ADRs em `DECISIONS/`
* Dependências Python definidas em `pyproject.toml` (ADR-062)
* Base do ambiente Conda (python/libs nativas) em `environment.yml` (ADR-062)

> Regra: todo requisito aqui descrito deve ser verificável por teste automatizado,
> inspeção objetiva do código ou validação operacional reproduzível.

---

# 1. Escopo do Produto

## 1.1 Objetivo

Padronizar e governar operações físicas de expansão,
separando planejamento (Registry) de execução real (Operation),
com histórico imutável e rastreabilidade explícita.

## 1.2 Princípio Estrutural

O sistema separa rigorosamente:

* **Registry (Cadastro Mestre)** → define o que existe e como deve ser.
* **Operation (Execução)** → registra o que foi executado, quando, por quem e com quais evidências.

---

# 2. Requisitos Funcionais

## RF-01 — Cadastro Mestre (Registry)

O sistema deve permitir manter entidades estruturais via camada Web (Django):

* Lojas
* Projetos
* Subprojetos
* Categorias
* Tipos de Equipamento
* Equipamentos
* Kits e Itens de Kit

Critério de aceitação:

* CRUD disponível
* Alterações impactam apenas execuções futuras

Fonte:

* `web/cadastro/`

---

## RF-02 — Snapshot Operacional ao criar Chamado

Ao criar um Chamado, o sistema deve gerar automaticamente os Itens de Execução
com base no Kit selecionado.

Critério de aceitação:

* Alterações futuras no Kit não alteram Chamados já criados.

Fonte:

* `web/execucao/models.py`
* `web/execucao/tests/`

---

## RF-03 — Separação entre Setup e Execução

O Chamado deve possuir estágio explícito de planejamento (`EM_ABERTURA`)
distinto da execução.

Regras:

* Chamado nasce em `EM_ABERTURA`
* Após salvar setup → promovido para `ABERTO`
* Apenas Chamados `ABERTO` em diante aparecem na fila

Fonte:

* `web/execucao/views.py`

---

## RF-04 — Execução em Fila Operacional

O sistema deve permitir execução de Chamados por meio de fila operacional.

Critério de aceitação:

* Chamados `ABERTO+` aparecem na fila
* Templates não contêm regra de negócio

Fonte:

* `web/execucao/templates/`

---

## RF-05 — Evidências vinculadas ao Chamado

O sistema deve permitir anexar evidências a Chamados.

Exemplos:

* Nota Fiscal
* Carta de Conteúdo
* Documentos de exceção

Critério de aceitação:

* Evidência é entidade própria
* Vinculada a um Chamado

Fonte:

* `web/execucao/models.py`

---

## RF-06 — Gates Operacionais

Transições de estado devem ser protegidas por validações objetivas.

Exemplos:

* Liberação de NF exige itens válidos
* Finalização exige pré-condições
* Edição exige sessão ativa

Critério de aceitação:

* Tentativa inválida é bloqueada no backend

Fonte:

* `web/execucao/views.py`
* `web/execucao/tests/`

---

## RF-07 — Fluxo Direto e Inverso

O sistema deve suportar:

* ENVIO (Matriz → Loja)
* RETORNO (Loja → Matriz)

Critério de aceitação:

* Retorno gera novo Chamado
* Histórico não é apagado

Fonte:

* `web/execucao/models.py`

---

## RF-08 — Imutabilidade Operacional

Chamados finalizados não devem ser alterados destrutivamente.

Critério de aceitação:

* Correções geram novo Chamado
* Finalizado permanece histórico

---

## RF-09 — Chamado Externo

O sistema deve permitir registrar identificador externo.

Critério de aceitação:

* `ticket_externo_id` único quando preenchido
* UI exibe formato padronizado

Fonte:

* `web/execucao/models.py`

---

## RF-10 — Autorização por Capabilities

A camada Web deve aplicar autorização baseada em capabilities.

Critério de aceitação:

* Enforcement no backend
* Templates apenas refletem permissões

Fonte:

* `web/iam/`

---

# 3. Requisitos Não Funcionais

## RNF-01 — Separação Arquitetural

O sistema deve manter:

* Domínio independente de Django
* Web como adapter
* Regras fora de templates

Verificação:

* Inspeção arquitetural
* Testes de domínio

---

## RNF-02 — Qualidade de Código (Python)

O projeto deve usar:

* ruff
* black
* pre-commit

Verificação:

* Hooks ativos
* Execução local/CI

---

## RNF-03 — Testes Automatizados (Python)

O projeto deve usar:

* pytest
* pytest-django
* pytest-cov (quando configurado)

Verificação:

* Suíte executável via comando único (`make test-py`)

---

## RNF-04 — Testes JS

O projeto deve testar JavaScript crítico com:

* Jest
* jsdom

Verificação:

* Testes presentes em `web/**/__tests__/`

---

## RNF-05 — Auditoria de Dependências Python

O projeto deve possuir auditoria automatizada para detectar:

* Dependências declaradas e não utilizadas
* Imports utilizados sem dependência declarada

Ferramenta adotada:

* `deptry`

Verificação:

* Execução via `make deps-check`
* Falhas devem ser corrigidas antes de merge

---

# 4. Restrições Técnicas

## RT-01 — Runtime

* Python 3.11
* Ambiente gerenciado por Conda (`environment.yml`)

## RT-02 — Framework Web

* Django

## RT-03 — Frontend leve

* Sem build obrigatório
* Tailwind via CDN

## RT-04 — Tooling JS

* Node/npm apenas para testes JS
* Não faz parte do runtime de produção

---

# 5. Baseline de Dependências

Dependências principais (runtime Python):

* Django
* python-dotenv

Dependências de teste (extra `[test]` no `pyproject.toml`):

* pytest
* pytest-django
* pytest-cov
* psycopg[binary]

Ferramentas de desenvolvimento (extra `[dev]` no `pyproject.toml`):

* ruff
* black
* pre-commit
* deptry

JS (dev):

* Jest
* jsdom

Fonte definitiva:

* Python: `pyproject.toml`
* Base Conda: `environment.yml`
* JS: `package.json` / `package-lock.json`

Snapshots (artefatos gerados, não fonte de verdade):

* `docs/deps/environment.snapshot.yml`
* `docs/deps/pip-freeze.snapshot.txt`

---

# 6. Fora de Escopo Atual

* APIs públicas
* Integrações corporativas
* Multitenancy
* Infra hardening avançado
* Mobile/offline-first

---

# 7. Governança

Se um requisito mudar:

* Atualizar este documento no mesmo PR
* Criar ou atualizar ADR quando necessário

---

**Última revisão:** 2026-02-13
**Fonte:** Código real em `web/` + testes automatizados + `pyproject.toml` + `environment.yml`
