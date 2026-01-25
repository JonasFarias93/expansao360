# STATUS — EXPANSÃO360

## Sprint Atual
**Sprint 4 — UX Operacional & Views**

🎯 **Objetivo da Sprint**  
Evoluir a **experiência operacional** do sistema,
refinando UI, views e feedbacks visuais,
**sem alterações no core de domínio**.

Esta sprint foca exclusivamente em:
- clareza operacional
- redução de atrito na execução
- comunicação visual de status e permissões

---

## Sprint Anterior
**Sprint 3 — Fluxo Inverso e Evolução Operacional**  
📌 **Status:** ✅ Concluída  
🏷 **Release:** v0.3.0

🎯 **Objetivo da Sprint**  
Consolidar o **core operacional** do EXPANSÃO360,
incluindo fluxo inverso, evidências, regras de exceção
e IAM mínimo por capability.

### Entregas
- Chamado com suporte a:
  - fluxo direto (Matriz → Loja)
  - fluxo inverso (Loja → Matriz)
- Regras completas de finalização e retorno
- Modelo de itens operacionais com rastreabilidade
- Evidências associadas à execução (anexos)
- IAM mínimo baseado em capabilities
- Views Web funcionais para execução operacional
- Testes automatizados cobrindo regras críticas

Encerramento formal do release **v0.3.0**.

---

## Sprint 2
**Sprint 2 — Cadastro e Execução Base (Web + CLI)**  
📌 **Status:** ✅ Concluída

🎯 **Objetivo da Sprint**  
Consolidar o **Cadastro Mestre (Registry)** e a
**Execução Base (Operation)**,
com testes automatizados e separação clara entre core, CLI e Web.

### Principais Entregas
- Core de domínio independente de framework
- CLI funcional para Registry e Operation
- Camada Web (Django) para:
  - Cadastro administrativo
  - Execução operacional
- Entidade Chamado com workflow e validações
- UI Web inicial para:
  - histórico
  - detalhe
  - edição de Chamados

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

## Observações Arquiteturais
- O core permanece **independente de framework**.
- Django atua exclusivamente como **camada de entrega**.
- Nenhuma regra de negócio será adicionada na Sprint 4.
- Evoluções estruturais exigem **ADR explícita**.
