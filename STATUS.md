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

---

## Em Andamento
- [ ] Validações finais da execução:
  - exigir Ativo + Série quando `tem_ativo=True`
  - exigir confirmação quando `tem_ativo=False`
- [ ] Controle de status do Chamado (workflow)
- [ ] Permissões e perfis (IAM)
- [ ] Evolução da UI do Chamado (detalhe / ações)

---

## Observações
- O core permanece independente de framework.
- Django atua como camada de entrega e persistência.
- Toda regra de negócio é validada via testes.
---
