# web/cadastro/services/import_lojas.py

from __future__ import annotations

from typing import Any

from cadastro.models import Loja


def _get(row: dict[str, Any], *keys: str) -> str:
    """
    Pega o primeiro valor existente dentre as chaves informadas.
    Tolerante a BOM no início do header e variações de case/trim.
    """
    if not row:
        return ""

    # mapa normalizado: remove BOM, strip e lower
    normalized_row: dict[str, Any] = {}
    for k, v in row.items():
        nk = str(k).replace("\ufeff", "").strip().lower()
        normalized_row[nk] = v

    for k in keys:
        nk = str(k).replace("\ufeff", "").strip().lower()
        if nk in normalized_row and normalized_row[nk] is not None:
            return str(normalized_row[nk]).strip()

    return ""


def normalizar_loja_row(row: dict[str, Any]) -> dict[str, Any]:
    """
    Normaliza uma linha vinda do Excel/CSV (layout Banco 12) para o formato interno do model Loja.

    Aceita:
    - layout externo:
      Filial;Hist.;Nome Filial;Endereço;Bairro;Cidade;UF;Logomarca;Telefone;IP Banco 12
    - layout interno: codigo/nome/...
    """
    codigo = _get(row, "codigo", "Java", "Filial")
    nome = _get(row, "nome", "Nome loja", "Nome Filial")

    hist = _get(row, "hist", "Hist.", "Hist")
    endereco = _get(row, "endereco", "Endereço", "Endereco")
    bairro = _get(row, "bairro", "Bairro")
    cidade = _get(row, "cidade", "Cidade")
    uf = _get(row, "uf", "UF").upper()

    logomarca = _get(row, "logomarca", "Logomarca").upper()
    telefone = _get(row, "telefone", "Telefone")

    ip = _get(row, "ip_banco_12", "IP Banco 12", "IP Banco 12 ", "IP Banco12")
    ip_banco_12 = ip if ip else None

    return {
        "codigo": codigo,
        "nome": nome,
        "hist": hist,
        "endereco": endereco,
        "bairro": bairro,
        "cidade": cidade,
        "uf": uf,
        "logomarca": logomarca,
        "telefone": telefone,
        "ip_banco_12": ip_banco_12,
    }


def _row_changed(loja: Loja, data: dict[str, Any]) -> bool:
    fields = [
        "nome",
        "hist",
        "endereco",
        "bairro",
        "cidade",
        "uf",
        "logomarca",
        "telefone",
        "ip_banco_12",
    ]
    for f in fields:
        if getattr(loja, f) != data.get(f):
            return True
    return False


def importar_lojas(rows: list[dict[str, str]]) -> dict[str, int]:
    """
    Import idempotente:
    - cria quando não existe (por codigo)
    - atualiza apenas quando houver diferença
    - não duplica nunca
    Retorna contadores: created, updated, unchanged, skipped.
    """
    created = 0
    updated = 0
    unchanged = 0
    skipped = 0

    for raw in rows:
        normalized = normalizar_loja_row(raw)

        codigo = (normalized.get("codigo") or "").strip()
        if not codigo:
            skipped += 1
            continue

        defaults = {
            "nome": normalized.get("nome", "") or "",
            "hist": normalized.get("hist", "") or "",
            "endereco": normalized.get("endereco", "") or "",
            "bairro": normalized.get("bairro", "") or "",
            "cidade": normalized.get("cidade", "") or "",
            "uf": normalized.get("uf", "") or "",
            "logomarca": normalized.get("logomarca", "") or "",
            "telefone": normalized.get("telefone", "") or "",
            "ip_banco_12": normalized.get("ip_banco_12", None),
        }

        loja, was_created = Loja.objects.get_or_create(codigo=codigo, defaults=defaults)

        if was_created:
            created += 1
            continue

        if _row_changed(loja, defaults):
            for k, v in defaults.items():
                setattr(loja, k, v)
            loja.save()
            updated += 1
        else:
            unchanged += 1

    return {
        "created": created,
        "updated": updated,
        "unchanged": unchanged,
        "skipped": skipped,
    }
