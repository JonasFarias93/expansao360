# DECISIONS — EXPANSÃO360 (Índice)

Este diretório registra decisões técnicas e arquiteturais relevantes do projeto,
com o objetivo de evitar ambiguidades, manter rastreabilidade
e facilitar onboarding.

Cada ADR representa uma decisão formal aceita ou proposta
que impacta arquitetura, domínio, UI, processo ou governança.

---

## 📐 Formato padrão de cada ADR

- **Data** (YYYY-MM-DD)
- **Status** (Proposto | Aceito | Deprecado)
- **Decisão**
- **Contexto**
- **Consequências**

---

# 📚 Índice por Domínio

---

## 🏗 Architecture

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-001 | Separação conceitual: Registry x Operation | 2026-01-20 | Aceito |
| ADR-004 | Repositório stack-agnostic (sem framework definido) | 2026-01-20 | Deprecado |
| ADR-005 | Stack web definida: Django | 2026-01-21 | Aceito |
| ADR-020 | Web atua como Adapter (Camada de Entrega) | 2026-02-04 | Aceito |
| ADR-046 | Reorganização do diretório DECISIONS (índice + domínios) | 2026-02-11 | Aceito |

---

## 🧠 Domain

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-006 | Nomenclatura em PT-BR no domínio | 2026-01-21 | Aceito |
| ADR-007 | Entidade operacional “Chamado” substitui “Card” | 2026-01-21 | Aceito |
| ADR-008 | Configuração (IP) é decisão do Chamado | 2026-02-03 | Aceito |
| ADR-009 | Gate de NF e critérios de fechamento do Chamado | 2026-02-03 | Aceito |
| ADR-010 | Ciclo de vida explícito do Chamado | 2026-02-04 | Aceito |
| ADR-011 | Status EM_ABERTURA | 2026-02-05 | Aceito |
| ADR-033 | Padronização de códigos (internos vs externos) | 2026-02-03 | Proposto |
| ADR-058 | Separação do Domínio Chamado do App Execucao | 2026-02-11 | Aceito |

---

## ⚙️ Execução

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-012 | Separação Abertura vs Fila Operacional | 2026-02-04 | Aceito |
| ADR-013 | Setup e Execução em templates separados | 2026-02-05 | Aceito |
| ADR-041 | Sessão exclusiva de execução (ExecutionSession) | 2026-02-08 | Aceito |
| ADR-042 | Ação “Abrir” inicia/reentra sessão | 2026-02-08 | Aceito |
| ADR-043 | Validação e normalização de Contabilidade/NF | 2026-02-09 | Aceito |
| ADR-044 | Recalcular status automaticamente no Salvar | 2026-02-09 | Aceito |
| ADR-045 | Introdução do status EM_CONFIGURACAO | 2026-02-10 | Aceito |

---

## 🎨 UI

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-015 | Padronização de Layout e Componentes | 2026-02-05 | Aceito |
| ADR-016 | Preview inline na Fila (accordion) | 2026-02-05 | Aceito |
| ADR-038 | Cor do Projeto na Fila Operacional | 2026-02-05 | Aceito |
| ADR-039 | Modularização de templatetags por tema | 2026-02-06 | Aceito |
| ADR-040 | Cards-resumo interativos na Fila | 2026-02-06 | Aceito |

---

## 🔐 IAM / Autorização

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-021 | Adoção de Capability-Based Access Control | 2026-02-04 | Aceito |
| ADR-022 | Padronização de CBVs + CapabilityRequiredMixin | 2026-01-24 | Aceito |

---

## 🧪 Testing

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-030 | Padronização da estrutura de testes por camadas | 2026-02-02 | Aceito |
| ADR-031 | Adoção de testes JavaScript com Jest | 2026-02-04 | Aceito |

---

## 🗂 Registry (Cadastro Mestre)

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-023 | Introdução de Subprojetos no Registry | 2026-01-25 | Aceito |
| ADR-024 | Mapeamento operacional: Filial → Java | 2026-02-02 | Aceito |
| ADR-025 | Padronização de Logomarca | 2026-02-02 | Aceito |
| ADR-026 | Refinamento do Cadastro de Equipamentos | 2026-02-02 | Aceito |
| ADR-027 | Código de Equipamento automático | 2026-02-03 | Aceito |
| ADR-028 | TipoEquipamento como cadastro mestre | 2026-02-03 | Aceito |
| ADR-029 | InstalacaoItem referencia TipoEquipamento via FK | 2026-02-03 | Aceito |
| ADR-032 | Tipos governados por Categoria | 2026-02-04 | Aceito |
| ADR-034 | Cadastro mestre de Kit e KitItem | 2026-02-03 | Aceito |

---

## 🌐 Redes

| ID | Título | Data | Status |
|----|--------|------|--------|
| ADR-046 | Serviço de validação e classificação de IP (MVP) | 2026-02-04 | Aceito |
| ADR-047 | Reasons padronizados para validação/classificação de IP | 2026-02-04 | Aceito |
| ADR-048 | Regra global: prefixo /24 deve bater com base_ip | 2026-02-04 | Aceito |
| ADR-049 | Regras MVP TC por perfil (LEGACY vs SEGMENTADO) | 2026-02-04 | Aceito |
| ADR-050 | Typo warning não bloqueante | 2026-02-04 | Aceito |
| ADR-051 | Perfilrede tipos e Governanca.md | 2026-02-04 | Aceito |
| ADR-052 | Regraredeequipamento por perfil e unicidade.md | 2026-02-04 | Aceito |
| ADR-053 | Ippolicy como estrategia de atribuicao-ip.md | 2026-02-04 | Aceito |
| ADR-054 | Iindice instancia equipamento na execucao.md | 2026-02-04 | Aceito |
| ADR-055 | Integracao tipoequipamento com regrarreequipamento.md | 2026-02-04 | Proposto |
| ADR-056 | Evolucao enforcement validacao-ip-bloqueante.md | 2026-02-04 | Proposto |
| ADR-057 | Grupo de Rede como contrato estruturado do domínio Redes | 2026-02-04 | Aceito |
---

# 📌 Observações

- ADRs são imutáveis após aceitação.
- Mudanças estruturais devem gerar nova ADR.
- Decisões pendentes devem permanecer com status **Proposto**.
- Deprecações devem referenciar a ADR substituta.