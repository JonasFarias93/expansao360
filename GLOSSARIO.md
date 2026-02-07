# Glossário — EXPANSÃO360

Este documento define os **termos oficiais** utilizados no projeto **EXPANSÃO360**,
com o objetivo de manter **consistência semântica** entre:

* domínio (core)
* camada Web (Django)
* CLI
* documentação
* comunicação do time

Sempre que surgir dúvida de nomenclatura, **este documento é a fonte da verdade**.

---

## Camadas Conceituais

| Termo técnico | Termo adotado       | Descrição                                                                       |
| ------------- | ------------------- | ------------------------------------------------------------------------------- |
| registry      | Cadastro Mestre     | Camada responsável por definir **o que existe** e **como deve ser padronizado** |
| operation     | Execução / Operação | Camada responsável por registrar **o que foi executado de fato**                |
| workflow      | Execução            | Fluxo operacional de um Chamado (status, etapas e histórico)                    |
| core          | Domínio             | Regras de negócio puras, independentes de framework                             |
| adapter       | Interface           | Camada de entrada/saída (Web, CLI, APIs futuras)                                |

---

## Entidades de Negócio (Domínio)

| Termo técnico / legado | Termo oficial    | Descrição                                     |
| ---------------------- | ---------------- | --------------------------------------------- |
| location               | Loja             | Unidade física onde ocorre a execução         |
| project                | Projeto          | Contexto organizacional da execução           |
| subproject             | Subprojeto       | Subdivisão operacional de um Projeto          |
| kit                    | Kit              | Conjunto padronizado de itens de planejamento |
| kit item               | Item de Kit      | Item pertencente ao cadastro mestre de um Kit |
| card                   | Chamado          | **Unidade central de execução operacional**   |
| mount                  | Instalação       | Ato de executar fisicamente um Chamado        |
| execution item         | Item de Execução | Snapshot operacional derivado do Kit          |
| evidence               | Evidência        | Documento/anexo que comprova a execução       |

---

## Chamado (conceito central)

| Termo              | Definição                                                  |
| ------------------ | ---------------------------------------------------------- |
| Chamado            | Evento operacional imutável que registra uma execução real |
| Chamado de envio   | Fluxo operacional Matriz → Loja                            |
| Chamado de retorno | Fluxo operacional Loja → Matriz                            |
| Chamado de origem  | Chamado inicial que gerou um retorno                       |
| Item de Chamado    | Item pertencente exclusivamente a um Chamado               |
| Evidência          | Comprovação documental da execução (NF, carta, exceção)    |

---

## Equipamentos e Inventário

| Termo               | Definição                                             |
| ------------------- | ----------------------------------------------------- |
| Equipamento         | Item cadastrado no Registry                           |
| Tipo de Equipamento | Classificação do Equipamento dentro de uma Categoria  |
| Categoria           | Agrupador lógico de Tipos de Equipamento              |
| Rastreável          | Equipamento que exige Ativo e Número de Série         |
| Contável            | Equipamento sem ativo/série, apenas confirmação       |
| tem_ativo           | Flag que define se o equipamento é rastreável         |
| configurável        | Item cuja configuração técnica é decidida na execução |

---

## Identificadores e Dados Técnicos

| Termo técnico     | Termo adotado     | Observação                             |
| ----------------- | ----------------- | -------------------------------------- |
| asset tag         | Ativo             | Identificador patrimonial              |
| serial            | Número de Série   | Identificador físico único             |
| IP                | IP                | Endereço de rede                       |
| ticket externo    | Chamado Externo   | Identificador vindo de sistema externo |
| NF                | Nota Fiscal       | Documento fiscal de saída              |
| Carta de Conteúdo | Carta de Conteúdo | Evidência utilizada quando não há NF   |

---

## Status e Estados

### Status de Chamado

* **EM_ABERTURA** — Planejamento e setup técnico
* **ABERTO** — Pronto para execução (fila operacional)
* **EM_EXECUCAO** — Em execução em campo
* **AGUARDANDO_*** — Estados intermediários (NF, coleta, exceções)
* **FINALIZADO** — Estado terminal

### Status de Configuração (itens)

* **Aguardando** — Ainda não configurado
* **Em configuração** — Configuração em andamento
* **Configurado** — Configuração concluída

### Status de Retorno

* **Retornado** — Item retornado com sucesso
* **Não retornado** — Exceção registrada

---

## Princípios Terminológicos

* **Chamado** é sempre um evento operacional (nunca um card visual).
* **Registry nunca registra execução**.
* **Operation nunca altera cadastro mestre**.
* Termos visuais (UI) não substituem termos de domínio.
* Sinônimos técnicos antigos devem ser evitados em código novo.

---

## Regra de Ouro

> Se um termo gera dúvida, **ele deve ser adicionado aqui antes de virar código**.
