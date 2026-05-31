# web/historico/services.py
from __future__ import annotations

from chamados.models import Chamado, InstalacaoItem
from historico.models import HistoricoAtivoTimeline, HistoricoExecucao


def gerar_historico_execucao(chamado: Chamado, finalizado_por=None) -> HistoricoExecucao:
    """
    Gera snapshot imutável consolidado de um Chamado.
    Idempotente: atualiza se já existir.
    """
    itens = list(chamado.itens.select_related("equipamento").all())

    itens_snapshot = [
        {
            "id": item.id,
            "equipamento": item.equipamento.nome,
            "tipo": item.tipo,
            "quantidade": item.quantidade,
            "tem_ativo": item.tem_ativo,
            "ativo": item.ativo or "",
            "numero_serie": item.numero_serie or "",
            "confirmado": item.confirmado,
            "deve_configurar": item.deve_configurar,
            "ip": str(item.ip) if item.ip else "",
            "status_configuracao": item.status_configuracao,
            "configurado_em": item.configurado_em.isoformat() if item.configurado_em else None,
        }
        for item in itens
    ]

    evidencias = list(chamado.evidencias.all())
    evidencias_snapshot = [
        {
            "tipo": ev.tipo,
            "descricao": ev.descricao,
            "arquivo": ev.arquivo.name if ev.arquivo else "",
            "criado_em": ev.criado_em.isoformat(),
        }
        for ev in evidencias
    ]

    historico, _ = HistoricoExecucao.objects.update_or_create(
        chamado_id=chamado.pk,
        defaults={
            "protocolo": chamado.protocolo,
            "tipo": chamado.tipo,
            "status_final": chamado.status,
            "loja_codigo": chamado.loja.codigo,
            "loja_nome": chamado.loja.nome,
            "projeto_codigo": chamado.projeto.codigo,
            "projeto_nome": chamado.projeto.nome,
            "subprojeto_codigo": chamado.subprojeto.codigo,
            "subprojeto_nome": chamado.subprojeto.nome,
            "kit_nome": chamado.kit.nome,
            "contabilidade_numero": chamado.contabilidade_numero or "",
            "nf_saida_numero": chamado.nf_saida_numero or "",
            "criado_em": chamado.criado_em,
            "finalizado_em": chamado.finalizado_em,
            "cancelado_em": chamado.cancelado_em,
            "finalizado_por": finalizado_por,
            "itens_snapshot": itens_snapshot,
            "evidencias_snapshot": evidencias_snapshot,
        },
    )

    # gera timeline de ativos rastreáveis
    _gerar_timeline_ativos(chamado, itens)

    return historico


def _gerar_timeline_ativos(chamado: Chamado, itens: list) -> None:
    """
    Registra evento na timeline para cada ativo rastreável.
    Idempotente por (ativo, chamado_id).
    """
    tipo_evento = (
        HistoricoAtivoTimeline.TipoEvento.RETORNADO
        if chamado.tipo == "RETORNO"
        else HistoricoAtivoTimeline.TipoEvento.INSTALADO
        if chamado.status == "FINALIZADO"
        else HistoricoAtivoTimeline.TipoEvento.CANCELADO
    )

    ocorrido_em = chamado.finalizado_em or chamado.cancelado_em or chamado.criado_em

    for item in itens:
        if not item.tem_ativo:
            continue
        if not (item.ativo or "").strip():
            continue

        HistoricoAtivoTimeline.objects.get_or_create(
            ativo=item.ativo,
            chamado_id=chamado.pk,
            defaults={
                "numero_serie": item.numero_serie or "",
                "tipo_evento": tipo_evento,
                "loja_codigo": chamado.loja.codigo,
                "loja_nome": chamado.loja.nome,
                "protocolo": chamado.protocolo,
                "equipamento_nome": item.equipamento.nome,
                "tipo_equipamento": item.tipo,
                "ocorrido_em": ocorrido_em,
            },
        )