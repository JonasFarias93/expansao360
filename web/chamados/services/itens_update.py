from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chamados.models import Chamado


@dataclass(frozen=True)
class UIMessage:
    level: str  # "success" | "error" | "warning" | "info"
    text: str


@dataclass(frozen=True)
class ItensUpdateResult:
    redirect_name: str
    redirect_kwargs: dict[str, Any]
    messages: list[UIMessage]


def _is_on(value: str | None) -> bool:
    return value == "on"


def atualizar_itens(*, chamado: Chamado, post_data) -> ItensUpdateResult:
    """
    Use-case: atualiza itens do chamado (setup vs operacional).

    Não faz permissão nem HTTP. A view aplica messages e redirect.
    """
    if chamado.status == Chamado.Status.FINALIZADO:
        return ItensUpdateResult(
            redirect_name="execucao:chamado_detalhe",
            redirect_kwargs={"chamado_id": chamado.id},
            messages=[
                UIMessage(
                    "warning",
                    "Chamado já está finalizado. Não é possível editar itens.",
                )
            ],
        )

    chamado.gerar_itens_de_instalacao()
    itens = list(chamado.itens.select_related("equipamento").all())
    if not itens:
        return ItensUpdateResult(
            redirect_name="execucao:chamado_detalhe",
            redirect_kwargs={"chamado_id": chamado.id},
            messages=[
                UIMessage("warning", "Este chamado não possui itens para atualizar.")
            ],
        )

    # ==========================
    # SETUP (EM_ABERTURA)
    # ==========================
    if chamado.status == Chamado.Status.EM_ABERTURA:
        for item in itens:
            deve_configurar = _is_on(post_data.get(f"deve_configurar_{item.id}"))
            ip_raw = (post_data.get(f"ip_{item.id}") or "").strip()

            if not item.equipamento.configuravel:
                deve_configurar = False
                ip_raw = ""

            if deve_configurar and not ip_raw:
                return ItensUpdateResult(
                    redirect_name="execucao:chamado_setup",
                    redirect_kwargs={"chamado_id": chamado.id},
                    messages=[
                        UIMessage(
                            "error",
                            f"Informe o IP do item '{item.equipamento.nome}' (configuração marcada).",
                        )
                    ],
                )

            item.deve_configurar = deve_configurar
            item.ip = ip_raw or None
            item.save(update_fields=["deve_configurar", "ip"])

        chamado.status = Chamado.Status.ABERTO
        chamado.save(update_fields=["status"])

        return ItensUpdateResult(
            redirect_name="execucao:fila",
            redirect_kwargs={},
            messages=[
                UIMessage(
                    "success",
                    "Setup salvo. Chamado promovido para ABERTO e enviado para a fila.",
                )
            ],
        )

    # ==========================
    # OPERACIONAL (ABERTO+)
    # ==========================
    for item in itens:
        deve_configurar = _is_on(post_data.get(f"deve_configurar_{item.id}"))
        ip_raw = (post_data.get(f"ip_{item.id}") or "").strip()

        if not item.equipamento.configuravel:
            deve_configurar = False
            ip_raw = ""

        item.deve_configurar = deve_configurar
        item.ip = ip_raw or None
        update_fields: list[str] = ["deve_configurar", "ip"]

        if item.tem_ativo:
            item.ativo = (post_data.get(f"ativo_{item.id}") or "").strip()
            item.numero_serie = (post_data.get(f"serie_{item.id}") or "").strip()
            update_fields += ["ativo", "numero_serie"]
        else:
            item.confirmado = _is_on(post_data.get(f"confirmado_{item.id}"))
            update_fields += ["confirmado"]

        item.save(update_fields=update_fields)

    if chamado.status == Chamado.Status.ABERTO:
        chamado.status = Chamado.Status.EM_EXECUCAO
        chamado.save(update_fields=["status"])

    return ItensUpdateResult(
        redirect_name="execucao:chamado_detalhe",
        redirect_kwargs={"chamado_id": chamado.id},
        messages=[UIMessage("success", "Itens atualizados com sucesso.")],
    )
