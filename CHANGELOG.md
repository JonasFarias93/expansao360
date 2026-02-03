# Changelog — EXPANSÃO360

Todas as mudanças relevantes do projeto são documentadas neste arquivo.
O versionamento segue o padrão **SemVer**.

---

## [v0.3.0] — 2026-01-24
### Fluxo Operacional Completo

Este release consolida o **core operacional** do EXPANSÃO360, estabelecendo
uma base estável e governada para evolução de UI, UX e escala.

### Adicionado
- Suporte completo a **fluxo inverso** (retorno / devolução)
- Regras de negócio para **finalização, retorno e exceções** de Chamados
- Modelo de **itens operacionais** com rastreabilidade
- Associação de **evidências** à execução operacional
- IAM mínimo baseado em **capabilities**
- Validações explícitas de permissão na camada web

### Alterado
- Padronização e clareza dos **status operacionais** (ex.: `EM_EXECUCAO`)
- Ciclo de vida do Chamado ajustado para suportar fluxo direto e inverso
- Organização da suíte de testes (core, web/auth, model vs view)

### Corrigido
- Falhas intermitentes relacionadas a usuário e permissões
- Problemas de sincronização de estado (`refresh_from_db`)
- Duplicações indevidas em cenários específicos de execução

### Qualidade
- Regras críticas de negócio cobertas por testes automatizados
- Separação rigorosa entre domínio, aplicação e camada web
- Nenhuma regra de negócio acoplada à UI

### Observações
- Este release encerra a **Sprint 3 — Fluxo Inverso e Evolução Operacional**
- A partir deste ponto, a evolução prioriza **UX, Views e experiência operacional**
- Não houve mudanças estruturais que demandassem novo ADR

---

## [v0.2.0] — 2026-01-22
### Adicionado
- Core de domínio independente de framework
- Casos de uso implementados com TDD
- CLI funcional para Registry e Operation
- Camada Web (Django) para Cadastro e Execução
- Entidade Chamado com workflow e validações
- Geração automática de itens de execução a partir de Kits
- UI Web para histórico, detalhe e edição de Chamados

### Observações
- Primeira versão utilizável end-to-end do sistema
- Base arquitetural e ADRs consolidados
