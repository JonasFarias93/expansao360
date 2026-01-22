# EXPANSÃO360

Plataforma para gestão de expansão, padronização e operação de campo, separando claramente
o cadastro administrativo (mestre) da execução operacional, com rastreabilidade completa.

> **Última versão estável:** `v0.2.0` — Web v1 (Registry + Chamado)

---

## Objetivo

O EXPANSÃO360 tem como objetivo estruturar e governar a expansão de operações físicas,
garantindo que o que foi definido no planejamento seja corretamente executado em campo,
com histórico, evidências e controle operacional.

O foco do sistema é **rastreabilidade, consistência e evolução segura** dos processos.

---

## Estado do Projeto

- Core de domínio estável e independente de framework
- Arquitetura em camadas (Domain / Application / Infrastructure)
- Casos de uso implementados com TDD
- CLI funcional como interface de referência
- Camada Web implementada com Django
- Execução operacional via Chamados (workflow básico)
- Persistência via arquivo local (CLI) e ORM (Web)
- Testes automatizados e pre-commit hooks

---

## Conceito Central

O sistema é baseado em uma separação clara de responsabilidades:

### Registry (Cadastro Mestre)
Define **o que existe** e **como deve ser**.
Exemplos:
- Lojas
- Projetos / Subprojetos
- Equipamentos
- Kits e padrões

Características:
- Governança
- Dados estáveis
- Versionamento e auditoria

### Operation (Execução de Campo)
Registra **o que foi executado**, **quando**, **por quem** e **com quais evidências**.

Características:
- Alto volume transacional
- Histórico imutável
- Suporte a auditoria e reprocessamento

Essa separação reduz ambiguidade e permite evolução do sistema com segurança.

---

## Como rodar o projeto localmente

### Pré-requisitos
- Git
- Conda (Miniforge / Miniconda)
- GNU Make

### Setup do ambiente

```bash
conda env create -f environment.yml
conda activate expansao360
```

---

## CLI (interface de referência / demonstração)

A CLI permite cadastrar entidades do Registry e registrar operações do Operation
sem depender de API ou camada Web.


### Ajuda


```bash
python -m expansao360 --help
python -m expansao360 location --help
python -m expansao360 mount --help
```

---
### Fluxo completo (exemplo)

```
# (opcional) limpar estado local
rm -f .expansao360-state.json

# 1) cadastrar Location no Registry
python -m expansao360 location add LOC-001 "Loja A"

# 2) registrar uma operação (somente se a Location existir)
python -m expansao360 mount register LOC-001 jonas

# 3) listar
python -m expansao360 location list
python -m expansao360 mount list
```


## Web (Django)

### A camada Web fornece:

 - Cadastro administrativo (Registry)

 - Execução operacional via Chamados

 - Interface administrativa (Django Admin)

 - UI Web para histórico, detalhe e edição de Chamados

### Comandos principais

```bash
# aplicar migrations
python web/manage.py migrate

# rodar servidor
python web/manage.py runserver

# rodar testes
python web/manage.py test
