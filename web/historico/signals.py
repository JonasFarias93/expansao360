# web/historico/signals.py
from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from chamados.models import Chamado
from historico.services.projecao import gerar_historico_execucao


@receiver(post_save, sender=Chamado)
def chamado_finalizado_ou_cancelado(sender, instance: Chamado, **kwargs) -> None:
    if instance.status in ("FINALIZADO", "CANCELADO"):
        gerar_historico_execucao(instance)