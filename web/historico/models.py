# web/historico/models.py
from __future__ import annotations

from django.conf import settings
from django.db import models


class HistoricoExecucao(models.Model):
    """
    Snapshot imutável consolidado de um Chamado finalizado.
    Leitura apenas — nunca altera operação.
    """

    chamado_id = models.IntegerField(unique=True, db_index=True)
    protocolo = models.CharField(max_length=32, db_index=True)

    # contexto do chamado
    tipo = models.CharField(max_length=20)
    status_final = models.CharField(max_length=20)

    # loja
    loja_codigo = models.CharField(max_length=50, db_index=True)
    loja_nome = models.CharField(max_length=120)

    # projeto
    projeto_codigo = models.CharField(max_length=50)
    projeto_nome = models.CharField(max_length=120)
    subprojeto_codigo = models.CharField(max_length=50)
    subprojeto_nome = models.CharField(max_length=120)

    # kit
    kit_nome = models.CharField(max_length=120)

    # fiscal
    contabilidade_numero = models.CharField(max_length=40, blank=True, default="")
    nf_saida_numero = models.CharField(max_length=40, blank=True, default="")

    # timestamps
    criado_em = models.DateTimeField()
    finalizado_em = models.DateTimeField(null=True, blank=True)
    cancelado_em = models.DateTimeField(null=True, blank=True)

    # executor
    finalizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="historicos_finalizados",
    )

    # snapshot completo dos itens (JSON)
    itens_snapshot = models.JSONField(default=list)

    # snapshot de evidências (JSON)
    evidencias_snapshot = models.JSONField(default=list)

    # auditoria
    gerado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Execução"
        verbose_name_plural = "Históricos de Execução"
        ordering = ["-finalizado_em", "-criado_em"]

    def __str__(self) -> str:
        return f"{self.protocolo} → {self.loja_codigo}"


class HistoricoAtivoTimeline(models.Model):
    """
    Linha do tempo imutável de um ativo rastreável.
    Cada registro = um evento (instalação, retorno, etc).
    """

    class TipoEvento(models.TextChoices):
        INSTALADO = "INSTALADO", "Instalado"
        RETORNADO = "RETORNADO", "Retornado"
        CANCELADO = "CANCELADO", "Cancelado"

    ativo = models.CharField(max_length=80, db_index=True)
    numero_serie = models.CharField(max_length=120, blank=True, default="")

    tipo_evento = models.CharField(max_length=20, choices=TipoEvento.choices)

    loja_codigo = models.CharField(max_length=50, db_index=True)
    loja_nome = models.CharField(max_length=120)

    chamado_id = models.IntegerField(db_index=True)
    protocolo = models.CharField(max_length=32)

    equipamento_nome = models.CharField(max_length=120)
    tipo_equipamento = models.CharField(max_length=80, blank=True, default="")

    ocorrido_em = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = "Timeline de Ativo"
        verbose_name_plural = "Timelines de Ativos"
        ordering = ["-ocorrido_em"]
        indexes = [
            models.Index(fields=["ativo", "ocorrido_em"]),
            models.Index(fields=["loja_codigo", "ocorrido_em"]),
        ]

    def __str__(self) -> str:
        return f"{self.ativo} → {self.tipo_evento} @ {self.loja_codigo}"