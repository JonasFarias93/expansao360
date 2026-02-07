# REQUIREMENTS — EXPANSÃO360

Este documento descreve requisitos **funcionais**, **não funcionais** e **restrições** do EXPANSÃO360,
alinhados com:

* `README.md`
* `ARCHITECTURE.md`
* `DECISIONS.md`
* Dependências reais registradas em `environment.yml` e no `pip` instalado

> Regra: requisitos aqui descritos devem ser **testáveis** (por teste automatizado, inspeção objetiva ou validação operacional).

---

## 1) Escopo do Produto

### 1.1 Objetivo

Padronizar e governar a expansão de operações físicas, garantindo que o planejamento (Registry)
seja executado em campo (Operation) com **histórico imutável**, **rastreabilidade** e **evidências**.

### 1.2 Conceito central

O sistema separa rigorosamente:

* **Registry (Cadastro Mestre)**: define o que existe e como deve ser
* **Operation (Execução)**: registra o que foi executado, quando, por quem e com quais evidências

---

## 2) Requisitos Funcionais

### RF-01 — Cadastro mestre de entidades (Registry)

O sistema deve permitir manter cadastros mestres governados para:

* Lojas
* Projetos e Subprojetos
* Categorias e Tipos de Equipamento
* Equipamentos
* Kits e Itens de Kit

**Critério de aceitação**: CRUD disponível via camada Web (Django) e/ou Admin; alterações afetam apenas execuções futuras.

---

### RF-02 — Abertura de Chamado a partir de Kit (snapshot operacional)

Ao criar um Chamado, o sistema deve gerar automaticamente os **Itens de Execução** a partir do Kit,
formando um **snapshot operacional** imutável.

**Critério de aceitação**: mudanças posteriores no Kit não alteram Itens de Execução de Chamados já criados.

---

### RF-03 — Separação explícita entre Setup e Execução

O sistema deve suportar um estágio de **setup/planejamento** do Chamado distinto da **execução operacional**.

Regras:

* Chamado nasce em `EM_ABERTURA` após a criação
* Ao salvar o setup, o Chamado é promovido explicitamente para `ABERTO`
* A fila operacional lista apenas Chamados `ABERTO` em diante

**Critério de aceitação**: Chamados em `EM_ABERTURA` não aparecem na fila operacional.

---

### RF-04 — Execução do Chamado em fila operacional

O sistema deve permitir executar Chamados em fila, registrando o andamento por status e por item.

**Critério de aceitação**: UI exibe fila operacional com chamadas para execução; templates não implementam regras de negócio.

---

### RF-05 — Evidências vinculadas ao Chamado

O sistema deve permitir registrar evidências associadas a Chamados, como:

* NF
* Carta de Conteúdo
* Documentos de exceção

**Critério de aceitação**: evidências são entidades próprias e consultáveis no contexto do Chamado.

---

### RF-06 — Gates operacionais (NF / coleta / finalização)

O sistema deve restringir transições de estado por regras explícitas:

* Liberação de NF apenas quando:

  * itens rastreáveis estiverem bipados
  * itens contáveis estiverem confirmados

* Finalização exige:

  * NF registrada (quando aplicável)
  * confirmação de coleta (quando aplicável)
  * evidências mínimas conforme o fluxo

**Critério de aceitação**: tentativa de avanço inválido é bloqueada por validação objetiva.

---

### RF-07 — Fluxo direto e fluxo inverso

O sistema deve suportar:

* Envio (Matriz → Loja)
* Retorno (Loja → Matriz)

**Critério de aceitação**: fluxos são rastreáveis e não apagam histórico; retorno/correção gera novo Chamado.

---

### RF-08 — Imutabilidade operacional

O sistema deve preservar histórico operacional:

* Chamados finalizados não são editados destrutivamente
* Correções e retornos geram **novo Chamado**

**Critério de aceitação**: operações de correção não alteram registros de eventos já concluídos.

---

### RF-09 — Chamado externo padronizado

O sistema deve suportar identificadores externos por:

* `ticket_externo_sistema`
* `ticket_externo_id`

**Critério de aceitação**:

* UI exibe "Chamado Externo" como `<sistema>: <id>`
* `ticket_externo_id` é único globalmente quando preenchido

---

### RF-10 — Autorização por capabilities (camada Web)

A camada Web deve aplicar autorização baseada em **capabilities** para ações sensíveis.

**Critério de aceitação**: enforcement no backend; templates apenas refletem permissões.

---

## 3) Requisitos Não Funcionais

### RNF-01 — Separação de camadas (arquitetura)

O sistema deve manter:

* Domínio independente de framework
* Web/CLI como adapters
* Regras de negócio fora de views/templates

**Verificação**: inspeção arquitetural + cobertura de testes de domínio/usecases.

---

### RNF-02 — Qualidade e estilo de código (Python)

O projeto deve manter padronização automática com:

* `ruff`
* `black`
* `pre-commit`

**Verificação**: execução em CI/local; hooks impedem drift.

---

### RNF-03 — Testes automatizados (Python)

O projeto deve possuir testes automatizados usando:

* `pytest`
* `pytest-cov`
* `pytest-django`

**Verificação**: execução de suíte de testes e relatório de cobertura.

---

### RNF-04 — Testes automatizados (JavaScript)

O projeto deve testar JavaScript puro crítico (ex.: formsets dinâmicos) com:

* Jest + jsdom (via Node)

**Verificação**: suíte de testes JS executável por comando único.

---

### RNF-05 — Observabilidade mínima de execução (dev)

O projeto deve oferecer feedback rápido em desenvolvimento:

* `pytest-watch`/`ptw` para ciclo rápido de testes

**Verificação**: comando de watch funcional no ambiente local.

---

### RNF-06 — Evolução segura e rastreabilidade de mudanças

Mudanças devem ser entregues em microtarefas e commits pequenos, com rastreabilidade.

**Verificação**: histórico de commits e branches descritivas (`feat/`, `fix/`, `docs/`).

---

## 4) Restrições Técnicas

### RT-01 — Plataforma / Runtime

* Python **3.11**
* Ambiente gerenciado por **Conda** (`environment.yml`)

---

### RT-02 — Framework web

* Django é o framework adotado para a camada Web

---

### RT-03 — Sem build frontend obrigatório

* Tailwind via CDN (setup leve)

---

### RT-04 — Stack de testes JS

* Dependência de desenvolvimento: Node/npm (para Jest/jsdom)

---

## 5) Dependências reais do projeto (baseline)

> A lista abaixo é **informativa** e serve para evitar documentação desatualizada. Não substitui o `environment.yml`.

### 5.1 Python (Conda / Base)

* python=3.11
* pytest
* ruff
* black
* pre-commit

### 5.2 Python (pip)

* django
* pytest-cov
* pytest-django
* pytest-watch / ptw
* typer, rich (CLI)

### 5.3 Utilitários observados no ambiente

* factory_boy, Faker (testes/fábricas)
* requests (HTTP)
* pillow (imagens)
* openpyxl (Excel)
* PyYAML (configs)
* docker (automação/integração de dev)
* nodeenv, virtualenv (suporte a tooling)

> Nota: dependências listadas como “observadas” devem ser confirmadas quanto ao uso efetivo no repositório.

---

## 6) Fora de Escopo (por enquanto)

* APIs públicas
* Integrações corporativas profundas
* Hardening de infraestrutura
* Multitenancy
* Mobile / offline-first

---

## 7) Microtarefas recomendadas para fechar a lacuna de doc vs ambiente

1. **[DOC] Atualizar `environment.yml` (pip indentação e consistência)**
2. **[DOC] Criar/atualizar seção "Dependências" no README (curta)**
3. **[DOC] Criar `docs/dependencies.md` (opcional) com racional de cada pacote "extra"**
4. **[DOC] Revisar se Jest/jsdom estão registrados (package.json / instruções)**

### Commits sugeridos

* `docs(requirements): registrar requisitos e baseline de dependencias reais`
* `docs(deps): documentar dependencias instaladas e racional`
