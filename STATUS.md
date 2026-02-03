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

### Entregas já realizadas na Sprint 4
- Importação idempotente de Lojas (CSV/XLSX)
- Padronização do cadastro de Lojas conforme base externa
- Normalização de campos operacionais (UF, Logomarca, Java)
- Ajustes de UX no cadastro e listagem de Lojas
- Testes automatizados cobrindo importação e normalização

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

## Observações Arquiteturais
- O core permanece **independente de framework**.
- Django atua exclusivamente como **camada de entrega**.
- Nenhuma regra de negócio será adicionada na Sprint 4.
- Evoluções estruturais exigem **ADR explícita**.
