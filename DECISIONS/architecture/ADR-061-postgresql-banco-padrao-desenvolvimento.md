# ADR-061 — PostgreSQL como banco padrão de desenvolvimento

- **Data:** 2026-02-12
- **Status:** Proposto

---

## Decisão

PostgreSQL passa a ser o banco de dados padrão para o ambiente de desenvolvimento do projeto EXPANSÃO360.

SQLite deixa de ser utilizado como banco primário de desenvolvimento.

---

## Contexto

O sistema evoluiu para:

- Uso intensivo de Foreign Keys
- Regras de integridade mais complexas
- Dependência de comportamento real de constraints
- Sessões exclusivas com lock
- Recalculo automático de status
- Execução concorrente

SQLite possui diferenças relevantes em relação ao PostgreSQL, incluindo:

- Tratamento mais permissivo de constraints
- Diferenças em tipos de dados
- Limitações em comportamento de transações e locks

Além disso, o ambiente produtivo utilizará PostgreSQL.

Manter SQLite como banco padrão de desenvolvimento aumenta o risco de divergência entre ambiente local e produção.

---

## Consequências

### Positivas

- Maior fidelidade entre desenvolvimento e produção
- Detecção precoce de erros de integridade
- Confiabilidade em migrations
- Testes mais realistas

### Negativas

- Necessidade de docker-compose para dev
- Setup inicial mais complexo
- Dependência de variável de ambiente

---

## Impacto

- Atualização de settings.py para uso via env
- Atualização da documentação de setup
- Atualização da pipeline de testes
- Atualização do README