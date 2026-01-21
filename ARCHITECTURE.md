# Arquitetura — EXPANSÃO360

## Visão Geral

O EXPANSÃO360 é um sistema orientado a processos de expansão e operação de campo.
O princípio central é separar claramente:

- **Cadastro administrativo (mestre / estático)**: define o que existe e como deve ser.
- **Operação de campo (transacional / execução)**: registra o que foi executado, com rastreabilidade e histórico.

Essa separação reduz ambiguidade, melhora governança e permite evolução do sistema com segurança.

## Camadas Conceituais

### 1) Registry (Cadastro Mestre)
Responsável por manter entidades "fonte da verdade" do planejamento e padronização.

Exemplos típicos:
- Lojas / locais
- Projetos / iniciativas
- Padrões, layouts, checklists e regras
- Materiais e componentes aprovados

Características:
- Alterações são controladas (governança)
- Dados são relativamente estáveis
- Versionamento e auditoria são importantes

### 2) Operation (Execução de Campo)
Responsável por registrar eventos e evidências do que aconteceu na prática.

Exemplos típicos:
- Montagens realizadas
- Inspeções / validações
- Evidências (fotos, anexos, assinaturas)
- Ocorrências e retrabalhos

Características:
- Alto volume transacional
- Histórico e rastreabilidade são essenciais
- Permite reprocessamento e auditoria

## Diretrizes de Arquitetura

### Separação de responsabilidades
- Registry não depende de Operation para existir.
- Operation referencia Registry (nunca o contrário).

### Modelo em camadas (visão lógica)
- **Domain**: regras de negócio puras (entidades, value objects, políticas)
- **Application**: casos de uso (orquestração, comandos/queries)
- **Infrastructure**: banco, filas, storage, integrações externas
- **Interfaces**: API/CLI/UI (entrada do sistema)

### Princípios
- Código limpo e modular
- Mudanças pequenas e rastreáveis
- Commits pequenos e descritivos
- Decisões arquiteturais registradas em `DECISIONS.md`

## Fora de escopo (por enquanto)
- Detalhes de stack (linguagem/framework) antes da decisão formal
- Estrutura de pastas definitiva antes do primeiro esqueleto do app
- Regras de autorização e perfis (será definido após o fluxo base)

## Implementação Atual (Core + Adapters)

O EXPANSÃO360 adota uma arquitetura em camadas, onde o **core de domínio**
permanece independente de frameworks e interfaces. As interfaces (CLI/Web)
atuam como **adapters**, responsáveis por entrada, apresentação e orquestração,
sem concentrar regras de negócio.

### Core
- Regras de negócio puras (Domain / Application)
- Entidades como Chamado, Equipamento e Kit
- Casos de uso validados via testes (TDD)

### Adapters / Interfaces

#### CLI
- Interface de linha de comando para operações do sistema
- Não depende da camada Web

#### Web (Django)
A camada Web é implementada com Django, organizada em apps:

- `cadastro`: Registry (Cadastro Mestre)
- `execucao`: Operation (Chamados e execução)
- `iam`: Identidade, autenticação e permissões (em evolução)

Diretrizes:
- A Web atua como camada de entrega e persistência.
- Models Django **não** contêm regras de negócio do core.
- A UI Web é tratada como adapter: entrada, apresentação e orquestração.
