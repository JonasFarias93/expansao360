# web/cadastro/services/import_lojas.py

from __future__ import annotations


def normalizar_loja_row(row: dict[str, str]) -> dict[str, str | None]:
    """
    Normaliza uma linha vinda do layout externo:

    Filial;Hist.;Nome Filial;Endereço;Bairro;Cidade;UF;Logomarca;Telefone;IP Banco 12

    Regras:
    - 'Filial' é o identificador operacional (na UI é chamado de "Java").
    - 'Nome Filial' é o nome de exibição (na UI é chamado de "Nome loja").
    - UF sempre em uppercase.
    - IP Banco 12 vira None quando vazio.
    """

    def s(key: str) -> str:
        return (row.get(key) or "").strip()

    uf = s("UF").upper()
    ip = s("IP Banco 12")
    ip_banco_12 = ip if ip else None

    return {
        "filial": s("Filial"),
        "hist": s("Hist."),
        "nome_loja": s("Nome Filial"),
        "endereco": s("Endereço"),
        "bairro": s("Bairro"),
        "cidade": s("Cidade"),
        "uf": uf,
        "logomarca": s("Logomarca"),
        "telefone": s("Telefone"),
        "ip_banco_12": ip_banco_12,
    }
