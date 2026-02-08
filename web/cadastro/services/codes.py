from __future__ import annotations

from django.db import transaction

from cadastro.models import CodeSequence


def generate_code(prefix: str, width: int = 6) -> str:
    """
    Gera um código no formato PREFIXO-000001 com lock por prefixo.
    """
    prefix = (prefix or "").strip().upper()
    if not prefix:
        raise ValueError("prefix não pode ser vazio")

    with transaction.atomic():
        seq, _ = CodeSequence.objects.select_for_update().get_or_create(prefix=prefix)
        seq.last_value += 1
        seq.save(update_fields=["last_value", "updated_at"])
        return f"{prefix}-{seq.last_value:0{width}d}"
