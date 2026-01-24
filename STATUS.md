# STATUS — EXPANSÃO360

## Sprint Atual
**Sprint 3 — Fluxo Inverso e Evolução Operacional**

**Objetivo da sprint**  
Evoluir a execução operacional já consolidada, introduzindo:
- fluxo inverso (Loja → Matriz)
- regras específicas de retorno
- amadurecimento do IAM mínimo
- robustez operacional e UX

Esta sprint parte de uma base estável entregue na Sprint 2.

---

## Sprint Anterior
**Sprint 2 — Cadastro e Execução Base (Web + CLI)**  
Status: ✅ **Concluída**

Objetivo atingido:
Consolidação do cadastro mestre (Registry) e da execução base (Chamado),
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
- [x] DECISIONS.md — Registro de decisões técnicas (ADR)

---

## Progresso Consolidado (até Sprint 2)

### Core + CLI
- [x] Core de domínio independente
- [x] Casos de uso cobertos por testes (TDD)
- [x] CLI funcional (Location / Mount)
- [x] Persistência local (arquivo JSON)
- [x] Registry desacoplado da execução

---

### Web (Django)

#### Cadastro (Registry)
- [x] Categoria
- [x] Equipamento  
  - classificação rastreável vs contável (`tem_ativo`)
- [x] Loja
- [x] Projeto / Subprojeto
- [x] Kit
- [x] ItemKit  
  - equipamento  
  - tipo  
  - quantidade  
  - `requer_configuracao`
- [x] Admin configurado
- [x] Migrations aplicadas
- [x] Consistência e integridade de dados validadas

---

#### Execução (Operation)

##### Chamado
- [x] Entidade Chamado
- [x] Protocolo automático (`EX360-YYYYMMDD-XXXXXX`)
- [x] Referências externas únicas  
  - ServiceNow  
  - Contabilidade  
  - NF
- [x] Status do Chamado  
  - ABERTO → EM_EXECUCAO → FINALIZADO
- [x] Campo de auditoria `finalizado_em`
- [x] Imutabilidade após finalização
- [x] Validações de finalização no domínio

##### Itens de Execução
- [x] Geração automática de itens a partir do Kit
- [x] Snapshot operacional por item  
  - `tem_ativo`  
  - `requer_configuracao`
- [x] Separação clara:  
  - item contável  
  - item rastreável
- [x] Validações:  
  - ativo + série obrigatórios quando rastreável  
  - confirmação obrigatória quando contável

##### Configuração Técnica por Item
- [x] Status individual de configuração:  
  - AGUARDANDO  
  - EM_CONFIGURACAO  
  - CONFIGURADO
- [x] Progresso calculado dinamicamente no Chamado
- [x] UI com botões de transição por item
- [x] Regra de finalização:  
  - Chamado não finaliza com item configurável pendente
- [x] ADR formalizando governança de configuração

---

#### Evidências (Anexos)
- [x] Entidade EvidenciaChamado
- [x] Upload de arquivos por Chamado
- [x] Tipos de evidência  
  - NF  
  - Carta de Conteúdo  
  - Exceção
- [x] Listagem e download
- [x] Remoção condicionada ao status do Chamado
- [x] Governança registrada em ADR

---

#### IAM (mínimo)
- [x] Modelo de Capability
- [x] Associação User ↔ Capability
- [x] Admin configurado
- [x] Decorator `capability_required`
- [x] Enforcement nas actions críticas de Execução
- [x] ADR de IAM mínimo por capacidades

---

#### UI / Layout Web
- [x] Layout base (`base.html`)
- [x] Estrutura de templates  
  - `partials/`  
  - `components/`
- [x] Tailwind CSS (CDN — MVP)
- [x] Histórico de Chamados
- [x] Detalhe completo do Chamado
- [x] Edição de itens de execução
- [x] Barra de progresso de configuração
- [x] Evidências integradas ao fluxo
- [x] Separação de static files (CSS / JS)

---

## Planejamento — Sprint 3

### Fluxo Inverso (Loja → Matriz)
- [ ] Modelo de Chamado de retorno
- [ ] Vínculo explícito com Chamado original
- [ ] Regras específicas de finalização
- [ ] Integração com evidências
- [ ] Visibilidade de retornos pendentes

### IAM — Evolução
- [ ] Capabilities específicas para retorno
- [ ] UI condicionada por permissão (ocultar/desabilitar ações)
- [ ] Testes de autorização (403 / redirect controlado)

### Robustez e UX
- [ ] Revisão de mensagens e feedbacks
- [ ] Edge cases operacionais
- [ ] Revisão geral de documentação
- [ ] Preparação para próxima sprint

---

## Observações
- O domínio permanece independente de framework.
- Django atua exclusivamente como adapter (UI + persistência).
- Toda regra crítica está:
  - documentada (ADR)
  - validada no domínio
- Nenhuma decisão estrutural é implícita ou acidental.
