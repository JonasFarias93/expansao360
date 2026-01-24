# EXPANSÃO360

Plataforma para gestão de expansão, padronização e **operação de campo**,
com separação rigorosa entre **cadastro mestre (Registry)** e **execução operacional (Operation)**,
garantindo rastreabilidade, auditoria e governança de ponta a ponta.

---

## Visão Geral

O EXPANSÃO360 foi concebido para resolver um problema recorrente em operações físicas:
a desconexão entre **planejamento**, **execução** e **registro histórico**.

O sistema garante que:
- o que foi definido no planejamento exista como **fonte da verdade**
- o que aconteceu em campo seja registrado como **evento operacional imutável**
- toda execução tenha **rastreabilidade, evidências e governança**

---

## Status do Projeto

🚀 **Sprint 3 — Fluxo Inverso e Evolução Operacional (em andamento)**

### Sprint 2 — Cadastro e Execução Base  
Status: ✅ **Concluída**

O projeto já possui uma base sólida com:

- Arquitetura em camadas (Domain / Application / Infrastructure)
- Core de domínio independente de framework
- Casos de uso cobertos por testes (TDD)
- CLI funcional para Registry e Operation
- Camada Web (Django) estável
- Execução operacional via **Chamados**
- Evidências (anexos) por Chamado
- Governança de finalização
- IAM mínimo baseado em **capabilities**
- Testes automatizados + pre-commit hooks
- Documentação viva (ADR, Architecture, Status)

---

## Conceito Central

O sistema é baseado em duas camadas conceituais bem definidas:

### Registry (Cadastro Mestre)
Define **o que existe** e **como deve ser padronizado**.

Exemplos:
- Lojas
- Projetos / Subprojetos
- Equipamentos
- Kits de instalação

Características:
- Dados estáveis
- Governança forte
- Fonte da verdade do planejamento

---

### Operation (Execução de Campo)
Registra **o que foi executado na prática**.

Exemplos:
- Chamados
- Itens de execução
- Status operacionais
- Evidências (NF, carta de conteúdo, exceções)

Características:
- Histórico imutável
- Alto valor para auditoria e contabilidade
- Nenhuma edição destrutiva após finalização

---

## Arquitetura

O EXPANSÃO360 segue uma arquitetura em camadas:

- **Domain**  
  Regras de negócio puras (framework-agnostic)

- **Application**  
  Casos de uso e orquestração

- **Infrastructure**  
  Persistência, storage, integrações

- **Adapters (CLI / Web)**  
  Interfaces de entrada, UI e persistência

📄 Detalhes completos em [`ARCHITECTURE.md`](ARCHITECTURE.md)  
📄 Decisões arquiteturais em [`DECISIONS.md`](DECISIONS.md)

---

## Funcionalidades Atuais

### Execução Operacional (Chamados)
- Protocolo automático (`EX360-YYYYMMDD-XXXXXX`)
- Status controlado (ABERTO → EM_EXECUCAO → FINALIZADO)
- Itens gerados automaticamente a partir de Kits
- Equipamentos:
  - rastreáveis (ativo + série obrigatórios)
  - contáveis (confirmação simples)
- Configuração técnica por item
- Progresso calculado dinamicamente
- Finalização com validações de domínio

---

### Evidências
- Upload de arquivos por Chamado
- Tipos:
  - NF
  - Carta de Conteúdo
  - Exceção
- Listagem, download e remoção controlada
- Governança registrada via ADR

---

### IAM (mínimo)
- Controle por **capabilities**
- Enforcement no backend (Django views)
- UI condicionada por permissão
- Domínio permanece permission-agnostic

---

## Como rodar o projeto localmente

### Pré-requisitos
- Git
- Conda (Miniforge / Miniconda)
- GNU Make

---

### Setup do ambiente

```bash
# criar o ambiente
conda env create -f environment.yml

# ativar
conda activate expansao360


CLI

A CLI permite operar o sistema sem Web/API, útil para testes e apresentação do core.

Ajuda

# limpar estado local
rm -f .expansao360-state.json

# cadastrar Location
python -m expansao360 location add LOC-001 "Loja A"

# registrar operação
python -m expansao360 mount register LOC-001 jonas

# listar
python -m expansao360 location list
python -m expansao360 mount list


Web (Django)

A camada Web fornece:

Cadastro administrativo (Registry)

Execução operacional via Chamados

Evidências e histórico

IAM mínimo

Admin Django

Comandos principais

# aplicar migrations
python web/manage.py migrate

# rodar servidor
python web/manage.py runserver

# rodar testes
python web/manage.py test


Próximos Passos (Sprint 3)

Fluxo inverso (Loja → Matriz)

Chamados de retorno vinculados

Regras específicas de finalização

Evolução do IAM

Robustez, UX e relatórios

Princípios do Projeto

Nenhuma regra crítica sem ADR

Nenhuma regra de negócio no adapter

Histórico nunca é apagado

Domínio sempre testado

Mudanças pequenas e rastreáveis



---

### 💡 Observação importante
Esse README agora:
- **explica o “porquê”**, não só o “como”
- serve para **onboarding técnico**
- reflete corretamente o estágio do projeto
- não promete nada que não exista

Se quiser, no próximo passo podemos:
- revisar se o README está “bom para GitHub público”
- ou extrair uma versão mais curta (pitch / overview)

Mas por agora: **update 100% justificado e maduro** 👏
