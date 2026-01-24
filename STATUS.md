# STATUS — EXPANSÃO360

## Sprint Atual
**Sprint 4 — UX Operacional & Views**

Objetivo desta sprint:
Evoluir a **experiência operacional** do sistema,
refinando UI, views e feedbacks visuais,
sem alterações no core de domínio.

---

## Sprint Anterior
**Sprint 3 — Fluxo Inverso e Evolução Operacional**  
📌 Status: ✅ Concluída

Objetivo desta sprint:
Consolidar o **core operacional** do EXPANSÃO360,
incluindo fluxo inverso, evidências, regras de exceção
e IAM mínimo por capability.

### Entregas
- Chamado com fluxo direto e inverso
- Regras completas de finalização e retorno
- Modelo de itens operacionais com rastreabilidade
- Evidências associadas à execução
- IAM mínimo baseado em capabilities
- Views web funcionais para execução
- Testes organizados cobrindo regras críticas

Encerramento formal do release **v0.3.0**.

---

## Sprint 2
**Sprint 2 — Cadastro e Execução Base (Web + CLI)**  
📌 Status: ✅ Concluída

Objetivo desta sprint:
Consolidar o cadastro mestre (Registry) e a execução base (Chamado),
com testes automatizados e separação clara entre core, CLI e Web.

### Principais Entregas
- Core de domínio independente de framework
- CLI funcional para Registry e Operation
- Camada Web (Django) para Cadastro e Execução
- Entidade Chamado com workflow e validações
- UI Web inicial para histórico, detalhe e edição de Chamados

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

## Planejamento — Sprint 4

### UI / Fluxo Operacional
- [ ] UI dedicada para fluxo inverso
- [ ] Status operacional explícito (`EM_EXECUCAO`)
- [ ] Upload de evidências com feedback visual
- [ ] Estados vazios e mensagens orientativas

### Views / Web
- [ ] Views mais semânticas e específicas
- [ ] Mensagens claras de permissão (IAM → UX)
- [ ] Ajustes de navegação e legibilidade

---

## Observações
- O core permanece independente de framework.
- Django atua exclusivamente como camada de entrega.
- Nenhuma regra de negócio será adicionada na Sprint 4.
- Evoluções estruturais exigem ADR.
