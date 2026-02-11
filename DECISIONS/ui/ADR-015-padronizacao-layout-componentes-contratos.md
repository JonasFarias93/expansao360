# ADR-015 — Padronização de Layout, Componentes e Contratos de Templates (Execução & Cadastro)

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
Padronizar o layout, componentes visuais e contratos de templates dos módulos
**Execução** e **Cadastro**, estabelecendo:

- Um layout base único (sidebar + topbar + mensagens)
- Componentes reutilizáveis bem definidos (ex.: `card`, `actions`, headers)
- Separação clara entre listagem (fila), detalhe, setup e execução
- Um padrão visual consistente para tabelas, botões, badges e formulários

## Contexto
Antes desta mudança, o sistema apresentava:

- Variação visual entre telas de Execução e Cadastro
- Templates com responsabilidades misturadas (setup + execução no mesmo HTML)
- Uso inconsistente de cores, botões e estruturas de página
- Dificuldade de evoluir UI sem medo de regressão
- Falta de um “contrato mental” claro sobre o papel de cada template

O crescimento do fluxo de Execução exigia clareza absoluta entre:
planejamento, fila operacional, execução ativa e histórico.

## Decisões Técnicas Aplicadas

### 1) Layout Base Unificado
- `base.html` torna-se o ponto único de:
  - Sidebar
  - Topbar
  - Mensagens (`_messages`)
- Execução e Cadastro usam o mesmo layout estrutural, mudando apenas o conteúdo.

### 2) Componentização Clara
Consolidação de componentes reutilizáveis:

- `_sidebar.html`
- `_topbar.html`
- `_messages.html`
- `_card.html`
- `_actions.html`

Esses componentes não contêm regra de negócio, apenas estrutura visual.

### 3) Execução — Contrato de Templates
- Fila operacional usa cards compactos (somente leitura + CTA)
- Detalhe do chamado contém:
  - Header informativo (`_header_chamado`)
  - Itens de execução
- Ações operacionais não aparecem na fila
- O template de execução deixa de ser “tudo-em-um”

Objetivo: reduzir `if status == ...` espalhados pelo HTML.

### 4) Execução — UX de Configuração
Campos sensíveis (ex.: IP) passam a:
- Abrir em modo leitura
- Ter edição explícita via ação do usuário

### 5) Cadastro — Padronização Visual
Listagens e formulários (Lojas, Categorias, Equipamentos, Kits, Projetos, Subprojetos)
seguem o mesmo padrão:

- Header da página
- Card com tabela
- Botões primários (`slate`)
- Badges semânticos (Sim/Não, status)

### 6) CSS e Estáticos
- Confirmação explícita de carregamento de `ui.css`
- Separação consciente de CSS global (layout) vs CSS local (quando necessário)
- Evitar duplicação e “CSS fantasma”

## Consequências

### Positivas
- UI previsível e consistente
- Templates mais simples e legíveis
- Redução de branching por status
- Facilidade para onboarding
- Base sólida para evolução (gates, finalização, auditoria)
- Menor risco de regressão visual

### Custos / Trade-offs
- Refatoração inicial extensa de templates
- Necessidade de disciplina para manter contratos
- Ajustes em telas antigas para aderir ao padrão

## Nota
Decisão implementada e validada em Codespaces e ambiente local.