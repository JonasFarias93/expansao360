# ADR-057 — Grupo de Rede como contrato estruturado do domínio Redes

**Data:** 2026-02-04  
**Status:** Aceito

## Decisão
Formalizar o conceito de **Grupo de Rede** como entidade conceitual do domínio,
com contrato estruturado obrigatório.

Um Grupo de Rede representa um conjunto lógico de equipamentos que:

- compartilham a mesma intenção operacional
- seguem regras homogêneas de endereçamento
- possuem padrões previsíveis de hostname
- são validados de forma consistente e testável

Todo grupo deve documentar:

- identificação
- perfis suportados
- configuração por perfil (máscara/gateway)
- itens internos
- regras de IP por item
- governança e severidade

## Contexto
À medida que as regras de rede evoluem, múltiplos tipos de equipamentos
compartilham padrões semelhantes (ex.: retaguarda).

Sem formalização do conceito de grupo:

- regras ficam dispersas
- máscara/gateway podem divergir silenciosamente
- validações tornam-se parciais
- documentação perde consistência

Era necessário transformar “grupo” em conceito explícito e governado.

## Consequências
- Todo novo grupo deve seguir o template oficial.
- Alterações estruturais em grupos exigem nova ADR.
- O grupo + testes formam um contrato vivo.
- Evita regressões conceituais e divergência semântica.