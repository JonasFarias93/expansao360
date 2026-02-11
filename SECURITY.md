# Security — EXPANSÃO360

Este documento define diretrizes mínimas de segurança para o desenvolvimento
e manutenção do EXPANSÃO360, com foco em **prevenção de vazamento de credenciais**
e **disciplina operacional**.

Escopo atual: segurança de desenvolvimento e boas práticas de repositório.

---

## 1. Política de Secrets

### 1.1 Nunca versionar

❌ Não devem ser versionados:

* Arquivos `.env`
* Chaves de API
* Tokens
* Credenciais
* Certificados
* Dumps de banco de dados

`.env.example` deve conter apenas placeholders.

---

### 1.2 Vazamento de Secret

Se qualquer secret vazar no Git:

1. Considerar o secret comprometido
2. Rotacionar imediatamente
3. Revogar acessos relacionados
4. Avaliar necessidade de limpeza do histórico

---

## 2. Boas Práticas de Desenvolvimento

* Preferir **variáveis de ambiente** para configurações sensíveis
* Não hardcodar credenciais em código
* Não incluir credenciais em testes automatizados
* Não incluir valores sensíveis em fixtures ou seeds
* Revisar commits antes de `push` quando envolver:

  * configuração
  * infraestrutura
  * integrações externas

---

## 3. Segurança da Aplicação (As-Is)

### 3.1 CSRF

A aplicação utiliza proteção CSRF nativa do Django.

* Middleware ativo
* Templates utilizam `{% csrf_token %}`

---

### 3.2 Autenticação

* Baseada no sistema padrão do Django
* Login obrigatório para áreas operacionais

---

### 3.3 Autorização

* Modelo baseado em **capabilities**
* Enforcement ocorre no backend
* Templates apenas refletem permissões

---

### 3.4 Sessões de Execução

* Operações sensíveis exigem sessão ativa
* Tentativas inválidas retornam 403

---

## 4. Fora de Escopo (por enquanto)

* Hardening avançado de infraestrutura
* Secret managers corporativos
* WAF / IDS
* Compliance formal (ISO, SOC, etc.)
* Gestão avançada de chaves

---

## 5. Princípio Norteador

> Segurança é um processo contínuo, não um checklist único.

O EXPANSÃO360 prioriza:

* Uso correto dos mecanismos nativos do framework
* Simplicidade estrutural
* Clareza de responsabilidade
* Reação rápida a incidentes

---

Última revisão: 2026-02-11
Fonte: Código real em `web/` + práticas de desenvolvimento adotadas
