# web/execucao/templatetags/execucao_urgencia.py
from __future__ import annotations

from django import template

register = template.Library()

URGENCIA_TO_LABEL = {
    # compat / legado (valor persistido no banco)
    "MAIS_ANTIGO": "PADRÃO",
    # níveis do enum atual
    "BAIXA": "BAIXO",
    "MEDIA": "MÉDIO",
    "ALTA": "ALTO",
    "CRITICA": "CRÍTICO",
    # fallback genérico (defensivo)
    "NORMAL": "NORMAL",
}

URGENCIA_TO_BADGE_CLASS = {
    "MAIS_ANTIGO": "bg-slate-100 text-slate-800 border border-slate-200",
    "BAIXA": "bg-slate-100 text-slate-800 border border-slate-200",
    "MEDIA": "bg-blue-100 text-blue-800 border border-blue-200",
    "ALTA": "bg-amber-100 text-amber-800 border border-amber-200",
    "CRITICA": "bg-rose-100 text-rose-800 border border-rose-200",
    "NORMAL": "bg-slate-100 text-slate-800 border border-slate-200",
}


def _read_urgencia_slug(obj) -> str:
    """
    Lê o nível de urgência de forma resiliente, sem acoplar em um nome de campo único.

    Por ordem, tenta:
    - obj.prioridade (nosso modelo)
    - obj.urgencia (eventual uso futuro/compat)
    - obj.nivel_urgencia
    - obj.nivel_prioridade

    Retorna slug em UPPER (ex.: 'CRITICA', 'ALTA', ...).
    Fallback: 'MAIS_ANTIGO' (padrão do sistema / mais antigo).
    """
    for attr in ("prioridade", "urgencia", "nivel_urgencia", "nivel_prioridade"):
        val = getattr(obj, attr, None)
        if val is None:
            continue

        raw = getattr(val, "name", None) or str(val)
        slug = (raw or "").strip().upper()
        if slug:
            return slug

    return "MAIS_ANTIGO"


@register.simple_tag
def urgencia_badge_class(chamado) -> str:
    slug = _read_urgencia_slug(chamado)
    return URGENCIA_TO_BADGE_CLASS.get(slug, URGENCIA_TO_BADGE_CLASS["NORMAL"])


@register.simple_tag
def urgencia_label(chamado) -> str:
    slug = _read_urgencia_slug(chamado)
    return URGENCIA_TO_LABEL.get(slug, URGENCIA_TO_LABEL["NORMAL"])
