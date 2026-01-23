# STATUS — EXPANSÃO360

## Sprint Atual  
**Sprint 2 — Execução Operacional Web (Registry + Operation)**

**Objetivo da sprint**  
Consolidar a execução operacional via Web (Django), garantindo:
- separação rigorosa entre Registry e Operation  
- rastreabilidade por item  
- governança de finalização  
- base sólida para auditoria, IAM e fluxos inversos  

---

## Histórico (Sprint 0)

### Fundação do Repositório
- [x] Criação do repositório remoto
- [x] Clone no ambiente WSL
- [x] Configuração de identidade Git
- [x] Branches base (`main`, `develop`)
- [x] Disciplina de versionamento por microtarefas

### Documentação Base
- [x] README.md — visão geral e objetivos
- [x] ARCHITECTURE.md — camadas e responsabilidades
- [x] DECISIONS.md — decisões técnicas (ADR)

---

## Progresso Atual

### Core + CLI
- [x] Core de domínio independente
- [x] Casos de uso cobertos por testes (TDD)
- [x] CLI funcional (Location / Mount)
- [x] Persistência local para CLI
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
- [x] Consistência de dados validada

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

### UI / Layout Web
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
- [x] Início da separação de static files (`web/execucao/static/`)

---

## Marcos Concluídos

### Sprint 2 — Execução Web v1 (Dias 1–12)
- Execução operacional completa
- Snapshot por item
- Configuração técnica individual
- Evidências por Chamado
- Governança de finalização
- ADRs consolidados
- Código alinhado à documentação

---

## Planejamento Atualizado

### Próximos Dias (Sprint 2 — continuação)

#### Dia 13 — Organização técnica
- [ ] Finalizar separação de static files (CSS / JS)
- [ ] Remover dependências inline desnecessárias
- [ ] Atualizar ARCHITECTURE.md (UI + static)

#### Dia 14 — IAM mínimo
- [ ] Implementar modelo de capacidades
- [ ] Integração inicial com Django
- [ ] UI condicionada por permissão
- [ ] ADR de IAM consolidado

#### Dia 15 — Fluxo inverso (Loja → Matriz)
- [ ] Modelo de Chamado de retorno
- [ ] Vínculo com Chamado original
- [ ] Regras específicas de finalização
- [ ] Integração com evidências

#### Dia 16 — Buffer / Consolidação
- [ ] Revisão de UX
- [ ] Robustez e edge cases
- [ ] Revisão geral da documentação
- [ ] Preparação para próxima sprint

---

## Em Andamento
- [ ] IAM mínimo baseado em capacidades
- [ ] Fluxo inverso de execução (Loja → Matriz)
- [ ] Regras específicas de finalização de retorno
- [ ] Consolidação de static files

---

## Observações
- O domínio permanece independente de framework.
- Django atua exclusivamente como adapter (UI + persistência).
- Toda regra crítica está:
  - documentada (ADR)
  - validada no domínio
- Nenhuma decisão estrutural é implícita ou acidental.
