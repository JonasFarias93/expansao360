# STATUS — EXPANSÃO360

## Sprint Atual
**Sprint 2 — Cadastro e Execução Base (Web + CLI)**

Objetivo desta sprint:
Consolidar o cadastro mestre (Registry) e a execução base (Chamado),
com testes automatizados e separação clara entre core, CLI e Web.

---

## Histórico (Sprint 0)

### Fundação do Git
- [x] Criação do repositório remoto
- [x] Clone do repositório no WSL
- [x] Configuração de identidade Git
- [x] Criação da branch `develop`
- [x] Criação da branch `docs/init`

### Documentação Base
- [x] README.md — Visão geral e objetivo do projeto
- [x] ARCHITECTURE.md — Arquitetura e camadas conceituais
- [x] DECISIONS.md — Registro de decisões técnicas

---

## Progresso Atual

### Core + CLI
- [x] Core de domínio implementado
- [x] Casos de uso testados (TDD)
- [x] CLI funcional para Location e Mount
- [x] Persistência local (arquivo JSON)

### Web (Django)

#### Cadastro (Registry)
- [x] Categoria
- [x] Equipamento (com regra `tem_ativo`)
- [x] Loja
- [x] Projeto / Subprojeto
- [x] Kit / ItemKit (equipamento + tipo + quantidade)
- [x] Admin configurado
- [x] Migrations aplicadas
- [x] Testes de integridade do cadastro

#### Execução (Operation)
- [x] Entidade Chamado
- [x] Protocolo único automático (`EX360-YYYYMMDD-XXXXXX`)
- [x] Referências externas únicas (ServiceNow, Contabilidade, NF)
- [x] Campo de auditoria `finalizado_em`
- [x] Validação de finalização do Chamado
- [x] Geração de itens de execução a partir do Kit
- [x] Snapshot de `tem_ativo` por item
- [x] Admin com busca e filtros aprimorados
- [x] Testes automatizados do app `execucao`

#### UI / Layout Web
- [x] Layout base (`base.html`)
- [x] Estrutura de templates (`partials/`, `components/`)
- [x] Tailwind CSS via CDN
- [x] Página de histórico de Chamados (Histórico v1)
- [x] Página de detalhe do Chamado
- [x] Edição de itens do Chamado
- [x] Badges de status (Aberto / Em execução / Finalizado)



---

## Marcos

- **Dia 8 — Execução Web v1 concluída**
  - Histórico de Chamados
  - Detalhe do Chamado
  - Edição de itens
  - Validações de finalização (TDD)
  - Workflow de status (Aberto → Em execução → Finalizado)
  - Badges de status na UI
  - ADR do fluxo inverso Loja → Matriz

---

## Em Andamento
- [x] Validações finais da execução:
  - exigir Ativo + Série quando `tem_ativo=True`
  - exigir confirmação quando `tem_ativo=False`
- [x] Controle de status do Chamado (ABERTO → EM_EXECUCAO → FINALIZADO)
- [ ] Permissões e perfis (IAM)
- [ ] Fluxo inverso de execução (Loja → Matriz)
- [ ] Regras de finalização para retorno (retornado / não retornado)


## Observações
- O core permanece independente de framework.
- Django atua como camada de entrega e persistência.
- Toda regra de negócio é validada via testes.
- Fluxos operacionais críticos são registrados via ADR.
---
