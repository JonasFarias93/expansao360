# Security — EXPANSÃO360

Este documento define diretrizes mínimas de segurança para o desenvolvimento
e manutenção do EXPANSÃO360, com foco em **prevenção de vazamento de credenciais**
e **disciplina operacional**.

---

## Política de Secrets

- ❌ **Nunca versionar**:
  - arquivos `.env`
  - chaves de API
  - tokens
  - credenciais
  - certificados
  - dumps de banco de dados

- ✅ Utilizar `.env.example` **apenas com placeholders**, nunca com valores reais.

- 🚨 Se qualquer secret **vazar no Git**:
  - considerar o secret **comprometido**
  - **rotacionar imediatamente**
  - remover o valor do histórico (quando aplicável)

---

## Boas Práticas

- Preferir **variáveis de ambiente** para configuração sensível.
- Utilizar **secret managers** quando aplicável (em ambientes futuros).
- Evitar:
  - credenciais hardcoded em código
  - credenciais em testes automatizados
  - valores sensíveis em fixtures ou seeds

- Revisar commits antes de `push` quando envolver:
  - configuração
  - infraestrutura
  - integrações externas

---

## Escopo Atual

Este documento cobre:
- práticas de desenvolvimento
- segurança básica de repositório
- disciplina de versionamento

**Fora de escopo (por enquanto):**
- hardening de infraestrutura
- políticas corporativas de IAM
- gestão avançada de segredos
- compliance formal (ISO, SOC, etc.)

Esses tópicos serão tratados quando o projeto atingir
maturidade operacional adequada.

---

## Princípio Norteador

> Segurança é um **processo contínuo**, não um checklist único.

O EXPANSÃO360 prioriza:
- prevenção simples
- clareza de responsabilidade
- reação rápida a incidentes

Sem burocracia desnecessária, sem falsa sensação de segurança.
