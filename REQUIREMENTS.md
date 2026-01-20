# Requisitos — EXPANSÃO360

## Contexto
O EXPANSÃO360 separa claramente:
- **Registry (Cadastro Mestre):** define o que existe (ex.: Locations / lojas / locais).
- **Operation (Execução de Campo):** registra o que foi executado, com rastreabilidade completa.

## Definições
- **Location (Registry):** entidade que representa um local cadastrado (ex.: loja, ponto, unidade).
- **Mount (Operation):** registro de execução em campo associado a uma Location.

## Regras de Negócio (Core)

### RN-001 — Operação depende do cadastro mestre
Uma operação **só pode ser registrada** se existir uma **Location** correspondente no Registry.

**Critério de Aceite**
- Dado que uma Location **não existe**, quando tentar registrar um Mount, então o sistema deve **recusar** o registro.
- Dado que uma Location **existe**, quando registrar um Mount, então o sistema deve **persistir** o registro.

### RN-002 — Rastreabilidade mínima obrigatória
Toda operação (Mount) deve registrar obrigatoriamente:
- **Onde:** `registry_location_id` (referência à Location)
- **Quem:** `performed_by` (ator responsável)
- **Quando:** `performed_at` (data/hora)

**Critério de Aceite**
- Se qualquer um dos campos obrigatórios estiver ausente ou inválido, o sistema deve **recusar** o registro.

### RN-003 — Registry não depende de Operation
O cadastro mestre (Registry) não deve depender de operações para existir.
Operation sempre referencia Registry, e não o contrário.

## Observações
- Interfaces (CLI/Web/API) não devem conter regras de negócio; apenas acionar casos de uso.
- Persistência pode variar (JSON, SQLite, Django ORM) sem alterar o domínio e os casos de uso.
