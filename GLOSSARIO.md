# Glossário — EXPANSÃO360

Este documento define os **termos oficiais** utilizados no projeto EXPANSÃO360,
com o objetivo de manter consistência semântica entre:

* Domínio (core)
* Camada Web (Django)
* CLI (quando aplicável)
* Documentação
* Comunicação interna

> Este documento é a **fonte oficial de nomenclatura**.
> Em caso de dúvida terminológica, o glossário prevalece.

---

# 1. Source of Truth

* Código: `web/`
* Domínio Execução: `web/execucao/`
* Domínio Cadastro: `web/cadastro/`
* Domínio Redes: `web/redes/`
* ADRs: `DECISIONS/`

---

# 2. Camadas Conceituais

| Termo técnico | Termo oficial       | Descrição                                                      |
| ------------- | ------------------- | -------------------------------------------------------------- |
| registry      | Cadastro Mestre     | Camada que define **o que existe** e como deve ser padronizado |
| operation     | Execução / Operação | Camada que registra **o que ocorreu de fato**                  |
| workflow      | Fluxo de Execução   | Evolução de estados de um Chamado                              |
| core          | Domínio             | Regras de negócio puras, independentes de framework            |
| adapter       | Interface           | Camada de entrada/saída (Web, CLI, APIs futuras)               |

Princípio estrutural:

* Registry nunca depende de Operation.
* Operation referencia Registry, nunca o contrário.

---

# 3. Entidades de Negócio

## 3.1 Cadastro (Registry)

| Termo técnico  | Termo oficial       | Descrição                           |
| -------------- | ------------------- | ----------------------------------- |
| location       | Loja                | Unidade física onde ocorre execução |
| project        | Projeto             | Contexto organizacional             |
| subproject     | Subprojeto          | Subdivisão operacional              |
| kit            | Kit                 | Conjunto padronizado de itens       |
| kit item       | Item de Kit         | Item pertencente ao cadastro mestre |
| equipment      | Equipamento         | Entidade física cadastrada          |
| category       | Categoria           | Agrupador lógico de tipos           |
| equipment type | Tipo de Equipamento | Classificação do equipamento        |

---

## 3.2 Execução (Operation)

| Termo técnico  | Termo oficial    | Descrição                               |
| -------------- | ---------------- | --------------------------------------- |
| card           | Chamado          | Unidade central de execução operacional |
| execution item | Item de Execução | Snapshot operacional derivado do Kit    |
| evidence       | Evidência        | Documento que comprova execução         |
| mount          | Instalação       | Ato físico registrado por um Chamado    |

Princípio:

* Chamado é sempre um evento operacional imutável.

---

# 4. Chamado (Conceito Central)

| Termo              | Definição                                     |
| ------------------ | --------------------------------------------- |
| Chamado            | Evento operacional que registra execução real |
| Chamado de Envio   | Fluxo Matriz → Loja                           |
| Chamado de Retorno | Fluxo Loja → Matriz                           |
| Chamado de Origem  | Chamado que originou um retorno               |
| Item de Chamado    | Item pertencente exclusivamente a um Chamado  |
| Evidência          | Documento comprobatório (NF, carta, exceção)  |

Princípios:

* Chamados finalizados são imutáveis.
* Correções geram novos Chamados.
* Histórico não é editado.

---

# 5. Equipamentos e Inventário

| Termo        | Definição                                             |
| ------------ | ----------------------------------------------------- |
| Rastreável   | Equipamento que exige Ativo e Número de Série         |
| Contável     | Equipamento que exige apenas confirmação              |
| tem_ativo    | Flag que indica rastreabilidade                       |
| configurável | Item cuja configuração técnica é decidida na execução |

---

# 6. Identificadores Técnicos

| Termo técnico     | Termo oficial     | Observação                       |
| ----------------- | ----------------- | -------------------------------- |
| asset tag         | Ativo             | Identificador patrimonial        |
| serial            | Número de Série   | Identificador físico único       |
| IP                | IP                | Endereço de rede                 |
| ticket externo    | Chamado Externo   | Identificador de sistema externo |
| NF                | Nota Fiscal       | Documento fiscal de saída        |
| Carta de Conteúdo | Carta de Conteúdo | Evidência quando não há NF       |

---

# 7. Status e Estados

## 7.1 Status de Chamado

* **EM_ABERTURA** — Planejamento técnico
* **ABERTO** — Pronto para execução (fila)
* **EM_EXECUCAO** — Execução ativa
* **AGUARDANDO_*** — Estados intermediários (NF, coleta, exceções)
* **FINALIZADO** — Estado terminal

## 7.2 Status de Configuração (Itens)

* **Aguardando**
* **Em configuração**
* **Configurado**

## 7.3 Status de Retorno

* **Retornado**
* **Não retornado**

Fonte:

* `web/execucao/models.py`

---

# 8. Princípios Terminológicos

* Chamado nunca significa "card visual".
* Registry não registra execução.
* Operation não altera cadastro mestre.
* Termos visuais não substituem termos de domínio.
* Sinônimos técnicos antigos devem ser evitados em código novo.

---

# 9. Regra de Governança

Se um termo gerar dúvida:

1. Ele deve ser definido aqui antes de virar código.
2. Alterações terminológicas relevantes exigem atualização deste documento.
3. Mudanças estruturais podem exigir ADR.

---

Última revisão: 2026-02-11
Fonte: Código real em `web/` + estados definidos em `web/execucao/models.py`
