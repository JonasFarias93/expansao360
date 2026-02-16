from __future__ import annotations

from collections.abc import Iterable

from ..models import Chamado, InstalacaoItem, StatusConfiguracao


def _is_filled(value: str | None) -> bool:
    return bool((value or "").strip())


def build_fila_rows(chamados: Iterable[Chamado]) -> list[dict[str, object]]:
    """
    Converte chamados (com itens pré-carregados) em rows compatíveis com o template da fila.
    Move-only do cálculo existente na view.
    """
    rows: list[dict[str, object]] = []

    for ch in chamados:
        itens = list(ch.itens.all())

        rastreaveis: list[InstalacaoItem] = [i for i in itens if i.tem_ativo]
        contaveis: list[InstalacaoItem] = [i for i in itens if not i.tem_ativo]
        cfg: list[InstalacaoItem] = [i for i in itens if i.deve_configurar]

        bipados = sum(
            1 for i in rastreaveis if _is_filled(i.ativo) and _is_filled(i.numero_serie)
        )
        checados = sum(1 for i in contaveis if bool(i.confirmado))
        cfg_done = sum(
            1
            for i in cfg
            if i.status_configuracao == StatusConfiguracao.CONFIGURADO
            and _is_filled(i.ip)
        )

        rows.append(
            {
                "chamado": ch,
                "pode_liberar_nf": ch.pode_liberar_nf(),
                "bipados": bipados,
                "bip_total": len(rastreaveis),
                "checados": checados,
                "check_total": len(contaveis),
                "cfg_done": cfg_done,
                "cfg_total": len(cfg),
            }
        )

    return rows
