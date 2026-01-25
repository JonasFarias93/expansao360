# DECISIONS — EXPANSÃO360

Este documento registra decisões técnicas e arquiteturais relevantes do projeto,
com o objetivo de evitar ambiguidades, manter rastreabilidade e facilitar onboarding.

## Formato padrão de cada decisão
- Data (YYYY-MM-DD)
- Decisão
- Contexto
- Consequências

---

## 2026-01-20 — Separação conceitual: Registry x Operation

**Decisão**  
O sistema será modelado com duas camadas conceituais principais:
- **Registry (Cadastro Mestre)**: define “o que existe” e “como deve ser”
- **Operation (Execução de Campo)**: registra “o que foi executado”, com rastreabilidade e histórico

**Contexto**  
Precisamos garantir governança sobre padrões e, ao mesmo tempo, registrar a execução real em campo
sem poluir o cadastro mestre e sem perder histórico.

**Consequências**  
- Operation referencia Registry; Registry não depende de Operation.
- O domínio será desenhado para suportar auditoria e evolução segura.

---

## 2026-01-20 — Estratégia de trabalho: microtarefas + disciplina de versionamento

**Decisão**  
O desenvolvimento seguirá por microtarefas com validação objetiva,
usando branches e commits pequenos.

**Contexto**  
Queremos previsibilidade, rastreabilidade e redução de retrabalho.

**Consequências**  
- Cada microtarefa deve resultar em um commit (quando aplicável).
- Push frequente após validação.
- Branches com nomes descritivos (`docs/`, `feat/`, `fix/`).

---

## 2026-01-20 — Branches base: main / develop

**Decisão**  
Usaremos:
- `main` para estabilidade e releases
- `develop` para integração contínua

**Contexto**  
Separar o que está pronto para release do que está em desenvolvimento reduz risco operacional.

**Consequências**  
- Mudanças entram via branches derivadas.
- `main` recebe apenas conteúdo estável.

---

## 2026-01-20 — Repositório stack-agnostic (fase inicial)

**Decisão**  
O projeto permanecerá neutro quanto a stack e framework no estágio inicial.

**Contexto**  
Evitar acoplamento prematuro permite decisões baseadas em requisitos reais.

**Consequências**  
- `.gitignore` genérico
- Nenhuma estrutura de framework antecipada
- Stack definida posteriormente via ADR

---

## 2026-01-21 — Stack Web definida: Django

**Decisão**  
A camada Web será implementada em **Django**.

**Contexto**  
Após estabilização do core e da CLI, era necessário um framework maduro
para UI, autenticação, ORM e velocidade de entrega.

**Consequências**  
- Core permanece independente
- Django atua como adapter
- Models Django não contêm regras de negócio

---

## 2026-01-21 — Nomenclatura em PT-BR no domínio

**Decisão**  
O domínio e casos de uso utilizam nomenclatura em português (PT-BR).

**Contexto**  
Reduzir carga cognitiva e aproximar o código do negócio real.

**Consequências**  
- Core em PT-BR
- Framework/infra seguem convenções originais
- Glossário mantido para consistência

---

## 2026-01-21 — Entidade operacional “Chamado”

**Decisão**  
O termo **Chamado** substitui “Card” como entidade operacional.

**Contexto**  
“Card” é ambíguo e visual. “Chamado” representa melhor uma unidade operacional.

**Consequências**  
- Domínio, CLI e Web utilizam “Chamado”
- Possíveis aliases temporários para compatibilidade

---

## 2026-01-21 — Equipamentos rastreáveis vs contáveis (`tem_ativo`)

**Decisão**  
Equipamentos são classificados como:
- **Rastreáveis** (`tem_ativo=True`)
- **Contáveis** (`tem_ativo=False`)

**Contexto**  
Nem todos os itens exigem ativo/número de série.

**Consequências**  
- Execução valida campos conforme tipo
- Relatórios diferenciam ativos e consumíveis

---

## 2026-01-21 — Layout base Web com Tailwind (CDN)

**Decisão**  
Adotar Tailwind via CDN e estrutura base de templates (`base`, `partials`, `components`).

**Contexto**  
Padronizar UI desde o início sem custo de build frontend.

**Consequências**  
- Layout tratado como decisão arquitetural
- Evita HTML duplicado e decisões visuais ad-hoc

---

## 2026-01-21 — Camada Web como adapter

**Decisão**  
A Web atua apenas como adapter (UI + persistência + orquestração).

**Contexto**  
Evitar migração de regras de negócio para a camada Web.

**Consequências**  
- Core independente
- CLI e Web compartilham domínio
- Facilita API e mobile no futuro

---

## 2026-01-21 — Fluxo inverso via novo Chamado (Loja → Matriz)

**Decisão**  
Correções e retornos geram **novo Chamado**, nunca edição destrutiva.

**Contexto**  
Chamados representam eventos operacionais e contábeis reais.

**Consequências**  
- Histórico imutável
- Retornos exigem desfecho explícito
- Auditoria e contabilidade preservadas

---

## 2026-01-22 — Evidências (anexos) por Chamado

**Decisão**  
Evidências são entidades próprias vinculadas a Chamados.

**Contexto**  
NF, Carta de Conteúdo e documentos de exceção são parte do processo real.

**Consequências**  
- Finalização pode exigir evidência
- Auditoria fortalecida
- Modelo extensível (fotos, assinaturas, etc.)

---

## 2026-01-22 — IAM mínimo por capabilities

**Decisão**  
Adoção de **Capability-Based Access Control** na camada Web.

**Contexto**  
Precisamos restringir ações sensíveis sem acoplar IAM ao domínio.

**Consequências**  
- Backend valida permissões
- Templates apenas refletem
- Core permanece permission-agnostic

---

## ADR — 2026-01-24 — CBVs + CapabilityRequiredMixin

**Status:** Aceito  
**Contexto:** Sprint 3 — Execução / Fluxo Inverso / IAM

**Decisão**
- Migrar views críticas para CBVs
- Centralizar autorização em `CapabilityRequiredMixin`

**Consequências**
- Menos repetição
- Padrão consistente
- Migração incremental segura

---

## 2026-01-24 — Abertura de Chamado via UI

**Decisão**  
Chamados podem ser abertos via UI, gerando automaticamente Itens de Execução
a partir do Kit (snapshot operacional).

**Contexto**  
Necessidade de testes end-to-end e uso real do sistema.

**Consequências**  
- Chamado nasce do Registry
- Itens são imutáveis conceitualmente
- Planejamento e execução ficam claramente separados

---

**Chamados sempre nascem como eventos operacionais derivados do Registry.**
