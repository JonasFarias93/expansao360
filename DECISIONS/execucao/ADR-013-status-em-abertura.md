# ADR-013 — Status EM_ABERTURA e promoção explícita para ABERTO

**Data:** 2026-02-05  
**Status:** Aceito

## Decisão
Introduzir o status `EM_ABERTURA` no ciclo de vida de `Chamado`,
separando explicitamente:

- Abertura (setup / planejamento) → `EM_ABERTURA`
- Fila operacional → `ABERTO` em diante

## Contexto
A tela de setup ocorre imediatamente após o POST do formulário inicial,
quando o chamado já existe e os itens foram gerados, mas ainda não deve:

- Aparecer na fila operacional
- Permitir execução (bipagem / gates / finalizar)

Sem um estado explícito, a UI e as regras ficavam ambíguas,
gerando regressões e estados inconsistentes.

## Regras de Negócio
1. O POST da tela inicial cria o chamado com `status = EM_ABERTURA`.
2. Ao clicar em **Salvar setup**, o chamado é promovido para `status = ABERTO`.
3. A fila operacional lista apenas:
   - `ABERTO`
   - `EM_EXECUCAO`
   - `AGUARDANDO_*`
   - (nunca `EM_ABERTURA`)

## Consequências
- Separa claramente setup vs execução.
- Simplifica templates (modo setup vs modo execução).
- Simplifica regras e testes.
- Evita chamados “meio operacionais” logo após a criação.
- Torna o workflow mais explícito e auditável.