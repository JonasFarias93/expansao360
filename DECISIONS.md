# DECISIONS — EXPANSÃO360

Este documento registra **decisões técnicas e arquiteturais** do projeto **Expansão360**, com foco em **governança, rastreabilidade, imutabilidade operacional** e **facilidade de onboarding**.

> Documento **revisado, consolidado e sem duplicações**. Pronto para **copiar e colar no Canva**.

---

## 📐 Formato padrão de cada decisão

* **Data** (YYYY-MM-DD)
* **Decisão**
* **Contexto**
* **Consequências**
* **Status** (Proposto | Aceito | Deprecado)

---

# 🧠 Decisões Arquiteturais e de Domínio

## 2026-01-20 — Separação conceitual: Registry × Operation

**Decisão**
O sistema é modelado em duas camadas conceituais:

* **Registry (Cadastro Mestre):** define *o que existe* e *como deve ser*
* **Operation (Execução):** registra *o que foi executado*, com histórico e rastreabilidade

**Contexto**
Garantir governança sem poluir o cadastro com eventos operacionais.

**Consequências**

* Operation referencia Registry
* Registry não depende de Operation
* Base sólida para auditoria

**Status:** Aceito

---

## 2026-01-20 — Estratégia de trabalho: microtarefas + versionamento disciplinado

**Decisão**
Desenvolvimento orientado a microtarefas com commits pequenos e frequentes.

**Consequências**

* Cada microtarefa gera commit
* Push frequente
* Branches com prefixos semânticos (`feat/`, `fix/`, `docs/`)

**Status:** Aceito

---

## 2026-01-20 — Branches base: `main` / `develop`

**Decisão**

* `main`: releases estáveis
* `develop`: integração contínua

**Consequências**

* `main` recebe apenas código validado
* Mudanças entram via branch intermediária

**Status:** Aceito

---

## 2026-01-20 — Repositório stack-agnostic (fase inicial)

**Decisão**
Evitar acoplamento prematuro a frameworks.

**Consequências**

* `.gitignore` genérico
* Core independente

**Status:** Aceito

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**
A camada Web será implementada em **Django**, atuando como adapter.

**Consequências**

* Core isolado
* Django sem regras de negócio

**Status:** Aceito

---

## 2026-01-21 — Nomenclatura em PT-BR no domínio

**Decisão**
O domínio utiliza **português (PT-BR)**.

**Consequências**

* Código mais próximo do negócio
* Glossário mantido

**Status:** Aceito

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**
O termo **Chamado** substitui “Card”.

**Consequências**

* Clareza semântica
* Alinhamento com operação real

**Status:** Aceito

---

# 🔐 Segurança, Acesso e Execução

## 2026-01-24 — Capability-Based Access Control (Web)

**Decisão**
Adotar **Capability-Based Access Control** na camada Web.

**Consequências**

* Core permission-agnostic
* Backend valida
* Templates apenas refletem

**Status:** Aceito

---

## 2026-02-05 — Status EM_ABERTURA no ciclo de vida do Chamado

**Decisão**
Separar explicitamente:

* **EM_ABERTURA** → setup
* **ABERTO+** → execução

**Regras**

1. POST inicial cria `EM_ABERTURA`
2. Salvar setup promove para `ABERTO`
3. Fila lista apenas `ABERTO+`

**Consequências**

* Elimina estados ambíguos
* Simplifica UI e testes

**Status:** Aceito

---

# 🧩 Registry e Governança de Dados

## 2026-02-03 — Tipos de Equipamento como cadastro mestre

**Decisão**
Criar `TipoEquipamento` como entidade de Registry.

**Consequências**

* Elimina texto livre
* Garante integridade histórica

**Status:** Aceito

---

## 2026-02-04 — Tipos de Equipamento só existem dentro de Categoria

**Decisão**
`TipoEquipamento` só pode ser criado via **Categoria**.

**Consequências**

* Evita selects vazios
* Registry consistente

**Status:** Aceito

---

# 🌐 Domínio de Redes

## 2026-02-07 — Criação do app `rede`

**Decisão**
Criar o app `rede` para governança e validação de regras de rede.

**Escopo inicial**

* Validação de IP
* Perfis LEGACY / SEGMENTADO
* Regras versionadas

**Status:** Proposto

---

## 2026-02-07 — Grupos de Rede como contrato completo

**Decisão**
Grupos de Rede definem:

* Política de IP
* Máscara (CIDR)
* Gateway
* Hostname pattern

**Consequências**

* Domínio vira documentação viva
* Base para automação futura

**Status:** Aceito

---

## Grupo Oficial — RETAGUARDA_LOJA

### Perfil LEGACY_FLAT

* CIDR: 24
* Gateway: .222

### Perfil RD_SEGMENTADO

* CIDR: 27
* Gateway: .158

Itens:

* Banco12
* Micro Gerência
* Micro Farma
* Portal do Saber (RH)

> Contrato completo e fechado.

---

# 📊 Testes

## 2026-02-04 — Testes de JavaScript com Jest

**Decisão**
Adotar Jest + jsdom para testar JS puro.

**Consequências**

* Node como dependência dev
* Bugs de frontend cobertos

**Status:** Aceito

---

# 📌 Decisões Pendentes

1. Padronização de códigos internos vs externos — *Proposto*
2. Consolidação de UX na edição de Kit — *Em avaliação*

---

📘 **Fim do documento**

> Este arquivo está **limpo, consolidado e pronto para Canva**.
