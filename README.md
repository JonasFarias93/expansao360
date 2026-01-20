# EXPANSÃO360

Plataforma para gestão de expansão, padronização e operação de campo, separando claramente
cadastro administrativo (mestre) da execução operacional, com rastreabilidade completa.

## Objetivo

O EXPANSÃO360 tem como objetivo estruturar e padronizar a expansão de operações físicas,
garantindo que o que foi definido no planejamento seja corretamente executado em campo,
com histórico, evidências e governança.

## Status do Projeto

🚧 **Sprint 0 — Fundação do Repositório**

Neste momento, o projeto está em fase de estruturação técnica:
- Definição de arquitetura
- Padrões de versionamento
- Documentação base
- Ambiente de desenvolvimento

## Conceito Central

O sistema é baseado em uma separação clara de camadas:

- **Registry (Cadastro Mestre)**  
  Define *o que existe* e *como deve ser* (ex: lojas, projetos, layouts, padrões).

- **Operation (Execução de Campo)**  
  Registra *o que foi executado*, *quando*, *por quem* e *com quais evidências*.

Essa separação garante rastreabilidade, auditoria e evolução segura do sistema.


---

## Como rodar o projeto localmente

### Pré-requisitos
- Git
- Conda (Miniforge / Miniconda)
- GNU Make

### Setup do ambiente

```bash
# criar o ambiente
conda env create -f environment.yml

# ativar
conda activate expansao360
