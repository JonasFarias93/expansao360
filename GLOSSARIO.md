# Glossário — EXPANSÃO360

Este documento define os **termos oficiais** utilizados no projeto EXPANSÃO360,
com o objetivo de manter **consistência semântica** entre:

- domínio (core)
- camada Web (Django)
- CLI
- documentação
- comunicação do time

Sempre que surgir dúvida de nomenclatura, **este documento é a fonte da verdade**.

---

## Camadas Conceituais

| Termo técnico | Termo adotado | Descrição |
|---------------|---------------|-----------|
| registry | Cadastro Mestre | Camada responsável por definir **o que existe** e **como deve ser** |
| operation | Execução / Operação | Camada responsável por registrar **o que foi executado** |
| workflow | Execução | Fluxo operacional de um Chamado (status, etapas, histórico) |
| core | Domínio | Regras de negócio puras, independentes de framework |
| adapter | Interface | Camada de entrada/saída (Web, CLI, API futura) |

---

## Entidades de Negócio (Domínio)

| Termo antigo / técnico | Termo oficial | Observação |
|------------------------|---------------|------------|
| location | Loja | Unidade física onde ocorre a execução |
| project | Projeto | Contexto organizacional da execução |
| subproject | Subprojeto | Subdivisão operacional de um Projeto |
| kit | Kit | Conjunto padronizado de itens |
| item | Item | Unidade individual dentro de um Kit ou Chamado |
| card | Chamado | **Unidade central de execução operacional** |
| mount | Instalação | Ato de executar fisicamente um Chamado |
| execution item | Item de Execução | Snapshot operacional derivado do Kit |

---

## Chamado (conceito central)

| Termo | Definição |
|------|----------|
| Chamado | Evento operacional imutável que registra uma execução |
| Chamado de envio | Fluxo Matriz → Loja |
| Chamado de retorno | Fluxo Loja → Matriz |
| Chamado de origem | Chamado inicial que gerou um retorno |
| Item de Chamado | Item pertencente exclusivamente a um Chamado |
| Evidência | Documento/anexo que comprova a execução |

---

## Equipamentos e Inventário

| Termo | Definição |
|------|----------|
| Equipamento | Item cadastrado no Registry |
| Rastreável | Equipamento que exige Ativo e Número de Série |
| Contável | Equipamento sem ativo/série, apenas confirmação |
| tem_ativo | Flag que define se o equipamento é rastreável |
| configurável | Equipamento que exige configuração técnica |

---

## Identificadores e Dados Técnicos

| Termo técnico | Termo adotado | Observação |
|---------------|---------------|------------|
| asset tag | Ativo | Identificador patrimonial |
| serial | Número de Série | Identificador físico |
| IP | IP | Endereço de rede |
| protocolo | Protocolo | Identificador único do Chamado |
| NF | Nota Fiscal | Documento fiscal |
| Carta de Conteúdo | Carta de Conteúdo | Evidência sem NF |

---

## Status e Estados

### Status de Chamado
- Aberto
- Em execução
- Finalizado

### Status de Configuração
- Aguardando
- Em configuração
- Configurado

### Status de Retorno
- Retornado
- Não retornado (exceção)

---

## Princípios Terminológicos

- **Chamado** é sempre um evento operacional (nunca um formulário ou card visual).
- **Registry nunca registra execução**.
- **Operation nunca altera cadastro mestre**.
- Termos visuais (UI) não substituem termos de domínio.
- Sinônimos técnicos antigos devem ser evitados em código novo.

---

## Regra de Ouro

> Se um termo gera dúvida, **ele deve ser adicionado aqui antes de virar código**.
