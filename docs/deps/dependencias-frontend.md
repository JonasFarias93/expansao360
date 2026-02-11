# Auditoria de Dependências Frontend / JS — EXPANSÃO360

Este documento registra a **stack JavaScript utilizada (ou planejada)** no projeto,
sua motivação, impacto na qualidade e consequências da remoção.

> Regra: qualquer dependência JS introduzida vira requisito não funcional
> e precisa estar documentada aqui.

---

## 1️⃣ Stack JS atual

### 1.1 Node / npm

- **Status:** Presente (via ambiente de desenvolvimento / tooling)
- **Uso:** Execução de ferramentas de teste e automação JS

📌 Observação:
- Node **não é dependência de runtime do sistema**
- É dependência de **qualidade e desenvolvimento**

---

### 1.2 Jest

- **Status:** Introduzido (exemplo citado)
- **Categoria:** Testes frontend / qualidade

Jest é utilizado para:
- Testar código JavaScript de frontend
- Garantir comportamento de scripts sem navegador real
- Automatizar regressões em interações DOM

---

### 1.3 jsdom

- **Status:** Dependência do Jest
- **Categoria:** Ambiente de simulação de DOM

jsdom fornece:
- `document`
- `window`
- eventos DOM
- manipulação de elementos HTML

➡️ Permite testar JS **sem browser real**.

---

## 2️⃣ Motivação técnica (por que existe)

### Problema real que cobre
Scripts JS no projeto:
- manipulam DOM
- reagem a eventos
- alteram estado visual/funcional da UI

Sem Jest + jsdom:
- esses scripts **não são testáveis automaticamente**
- bugs só aparecem em runtime/manual QA

### Exemplos de bugs cobertos
- JS não dispara evento esperado
- seletor DOM quebrado após refactor HTML
- script falha silenciosamente
- regressão visual/funcional não detectada

---

## 3️⃣ O que acontece se remover

### Sem Jest + jsdom:

❌ Não há testes automatizados de frontend  
❌ Regressões JS passam despercebidas  
❌ Confiança cai em mudanças de UI  
❌ QA vira manual e reativo  

➡️ Qualquer ajuste em JS vira risco oculto.

---

## 4️⃣ Classificação como requisito não funcional

A partir desta auditoria, ficam explícitos os seguintes **requisitos não funcionais**:

### RNF-FE-001 — Testabilidade de frontend
O sistema **deve permitir testes automatizados de JavaScript**
sem dependência de navegador real.

➡️ Justificativa:
- Reduz regressões
- Aumenta confiança em refactors de UI
- Padroniza qualidade

---

### RNF-FE-002 — Isolamento de runtime
Ferramentas JS (Node, Jest, jsdom):
- **não fazem parte do runtime de produção**
- são exclusivas do ambiente de desenvolvimento e CI

---

## 5️⃣ Decisão arquitetural implícita (agora explícita)

- ✔️ A stack JS existe **por qualidade**, não por moda
- ✔️ Remover Jest/jsdom **reduz cobertura e confiança**
- ✔️ Manter exige:
  - Node disponível em ambiente de dev/CI
  - Documentação clara (este arquivo)

---

## 6️⃣ Próximos passos (Ciclo 2)

- [ ] Confirmar se existem testes JS no repositório
- [ ] Se existirem, registrar exemplos reais
- [ ] Se não existirem ainda:
  - manter Jest/jsdom como **stack aprovada**
  - só remover mediante decisão formal (ADR)

---

## Status da auditoria

- [x] Stack JS mapeada
- [x] Motivação registrada
- [x] Impacto da remoção explícito
- [x] Requisitos não funcionais derivados