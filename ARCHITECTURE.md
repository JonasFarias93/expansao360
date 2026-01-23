# ARCHITECTURE — EXPANSÃO360

## Visão Geral

O **EXPANSÃO360** é um sistema orientado à **execução operacional e governança de expansão de campo**.
O princípio central da arquitetura é a **separação explícita entre planejamento e execução**, garantindo:

- rastreabilidade histórica
- auditoria confiável
- imutabilidade operacional
- evolução segura do sistema

A arquitetura distingue claramente **o que é definido** do **que é executado**.

---

## Separação Conceitual Fundamental

### Registry × Operation

| Camada | Papel |
|------|------|
| **Registry (Cadastro Mestre)** | Define padrões, estruturas e regras |
| **Operation (Execução de Campo)** | Registra eventos reais, evidências e resultados |

Essa separação é **regra estrutural**, não convenção informal.

---

## Camadas Conceituais

### 1) Registry (Cadastro Mestre)

Responsável por manter as **entidades fonte da verdade** do planejamento e padronização.

#### Exemplos
- Lojas
- Projetos / Subprojetos
- Equipamentos
- Kits
- ItemKit (equipamento + tipo + quantidade + regra de configuração)

#### Características
- Dados relativamente estáveis
- Alterações controladas (governança)
- Versionamento implícito via snapshot na execução
- Não conhece a execução

---

### 2) Operation (Execução de Campo)

Responsável por registrar **eventos operacionais reais**, com histórico completo.

#### Exemplos
- Chamados
- Itens de execução
- Status de execução
- Configuração técnica por item
- Evidências (anexos)
- Fluxos de retorno (Loja → Matriz)

#### Características
- Alto volume transacional
- Histórico imutável após finalização
- Snapshot do estado do Registry no momento da execução
- Base para auditoria, contabilidade e rastreabilidade

---

## Modelo Arquitetural (Visão Lógica)

┌───────────────────────────┐
│ Interfaces │
│ (Web / CLI / API futura) │
└─────────────┬─────────────┘
│
┌─────────────▼─────────────┐
│ Application │
│ (Casos de Uso) │
└─────────────┬─────────────┘
│
┌─────────────▼─────────────┐
│ Domain │
│ (Regras de Negócio Puras) │
└─────────────┬─────────────┘
│
┌─────────────▼─────────────┐
│ Infrastructure │
│ (DB, Storage, Integrações)│
└───────────────────────────┘



---

## Camadas Técnicas

### Domain
- Entidades
- Value Objects
- Regras de negócio
- Políticas e validações
- Independente de framework

### Application
- Casos de uso
- Orquestração de regras
- Coordenação entre entidades
- Nenhuma dependência de UI ou persistência

### Infrastructure
- Banco de dados
- Storage de arquivos
- Integrações externas
- Implementações técnicas

### Interfaces (Adapters)
- Web (Django)
- CLI
- API futura

Adapters **não contêm regra de negócio**.

---

## Implementação Atual

### Core
- Independente de Django
- Testado via TDD
- Modela:
  - Chamado
  - Itens de execução
  - Regras de finalização
  - Snapshot operacional

---

### Web (Django)

A camada Web atua como **adapter**, responsável por:

- entrada de dados
- persistência
- apresentação (UI)
- orquestração de casos de uso

#### Apps

| App | Responsabilidade |
|---|---|
| `cadastro` | Registry |
| `execucao` | Operation |
| `iam` | Identidade e permissões (mínimo, em evolução) |

#### Diretrizes
- Models Django **não** concentram regras de negócio
- Views apenas orquestram
- Regras críticas ficam no domínio
- UI reflete permissões e estados, não decide regras

---

## Execução Operacional (Operation)

### Chamado
- Unidade operacional imutável
- Possui:
  - protocolo único
  - status (ABERTO / EM_EXECUCAO / FINALIZADO)
  - referências externas
  - evidências
- Após finalização:
  - não pode ser alterado
  - correções exigem novo Chamado

---

### Itens de Execução
- Gerados a partir do Kit
- Armazenam snapshot de:
  - equipamento
  - tipo
  - quantidade
  - `tem_ativo`
  - `requer_configuracao`

Alterações no Registry **não afetam execuções passadas**.

---

### Configuração Técnica por Item
- Estado individual:
  - AGUARDANDO
  - EM_CONFIGURACAO
  - CONFIGURADO
- Finalização do Chamado exige:
  - todos os itens configuráveis concluídos
- Governança formalizada via ADR

---

### Evidências
- Entidade própria
- Vínculo direto com Chamado
- Tipos:
  - NF
  - Carta de Conteúdo
  - Exceção
- Base para auditoria e contabilidade

---

## Fluxo Inverso (Loja → Matriz)

- Chamados finalizados são imutáveis
- Retornos geram **novo Chamado**
- Novo Chamado referencia o original
- Finalização exige decisão explícita:
  - retorno confirmado
  - não retornado (exceção)

---

## IAM (Identidade e Acesso)

### Estratégia
- IAM mínimo
- Baseado em **capacidades**, não perfis
- Evolutivo para RBAC completo

### Princípios
- Domínio define regras
- UI apenas habilita/desabilita ações
- Segurança não é implícita

---

## UI e Frontend

### Estratégia Atual
- Tailwind via CDN (MVP)
- Templates Django:
  - `base.html`
  - `partials/`
  - `components/`

### Evolução Planejada
- Separação formal de static files:
  - CSS
  - JS
- Preparação para build pipeline futuro
- UI desacoplada da regra de negócio

---

## Princípios Arquiteturais

- Imutabilidade operacional
- Snapshot em execução
- Separação Registry × Operation
- Decisões explícitas (ADR)
- Governança antes de conveniência
- Evolução sem retrabalho estrutural

---

## Fora de Escopo (por enquanto)
- API pública
- Mobile
- RBAC avançado
- Eventos assíncronos
- Versionamento explícito de configuração

Esses pontos já estão **preparados arquiteturalmente**, mas não implementados.

---

## Documentos Relacionados
- `DECISIONS.md` — decisões arquiteturais (ADR)
- `STATUS.md` — progresso e planejamento
- `REQUIREMENTS.md` — requisitos funcionais e não funcionais
