# web/execucao/models.py

# =========
# imports
# =========
import secrets

from cadastro.models import Equipamento, Kit, Loja, Projeto, Subprojeto
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.utils import timezone


# ==================
# status configuração
# ==================
class StatusConfiguracao(models.TextChoices):
    AGUARDANDO = "AGUARDANDO", "Aguardando"
    EM_CONFIGURACAO = "EM_CONFIGURACAO", "Em configuração"
    CONFIGURADO = "CONFIGURADO", "Configurado"


# =======
# chamado
# =======
class Chamado(models.Model):
    class Status(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        EM_EXECUCAO = "EM_EXECUCAO", "Em execução"
        FINALIZADO = "FINALIZADO", "Finalizado"

    class Tipo(models.TextChoices):
        ENVIO = "ENVIO", "Envio (Matriz → Loja)"
        RETORNO = "RETORNO", "Retorno (Loja → Matriz)"

    loja = models.ForeignKey(Loja, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    subprojeto = models.ForeignKey(Subprojeto, on_delete=models.PROTECT)
    kit = models.ForeignKey(Kit, on_delete=models.PROTECT)

    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.ENVIO)

    chamado_origem = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="retornos",
        help_text="Chamado de origem (obrigatório quando tipo=RETORNO).",
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTO)
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)
    protocolo = models.CharField(max_length=32, unique=True, editable=False)

    servicenow_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)
    contabilidade_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)
    nf_saida_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.protocolo or f"Chamado {self.pk}"

    def clean(self):
        super().clean()

        if self.tipo == self.Tipo.RETORNO:
            if not self.chamado_origem_id:
                raise ValidationError(
                    {"chamado_origem": "Chamado de retorno exige um chamado de origem."}
                )

            if self.pk and self.chamado_origem_id == self.pk:
                raise ValidationError(
                    {"chamado_origem": "Chamado não pode ser origem de si mesmo."}
                )

            # garante origem finalizada (se objeto ainda não carregado, busca)
            origem = self.chamado_origem
            if origem and origem.status != self.Status.FINALIZADO:
                raise ValidationError(
                    {"chamado_origem": "Chamado de origem deve estar FINALIZADO."}
                )

        else:
            if self.chamado_origem_id:
                raise ValidationError(
                    {"chamado_origem": "Chamado de envio não deve possuir chamado de origem."}
                )

    # -------------------------
    # geração de itens do chamado
    # -------------------------
    def gerar_itens_de_instalacao(self) -> None:
        if self.itens.exists():
            return

        for item_kit in self.kit.itens.select_related("equipamento").all():
            InstalacaoItem.objects.create(
                chamado=self,
                equipamento=item_kit.equipamento,
                tipo=item_kit.tipo,
                quantidade=item_kit.quantidade,
                tem_ativo=item_kit.equipamento.tem_ativo,
                requer_configuracao=item_kit.requer_configuracao,
            )

    # ----------
    # finalizar
    # ----------
    def finalizar(self) -> None:
        if self.status == self.Status.FINALIZADO:
            raise ValidationError("Chamado já está finalizado.")

        itens = list(self.itens.all())
        if not itens:
            raise ValidationError("Não é possível finalizar um chamado sem itens.")

        erros: list[str] = []

        # ==========================
        # ENVIO (Matriz -> Loja)
        # ==========================
        if self.tipo == self.Tipo.ENVIO:
            for item in itens:
                # regra: se requer configuração, precisa estar CONFIGURADO
                if (
                    item.requer_configuracao
                    and item.status_configuracao != StatusConfiguracao.CONFIGURADO
                ):
                    erros.append(
                        "Não é possível finalizar: "
                        f"'{item.equipamento.nome} {item.tipo}' ainda não foi marcado como "
                        "CONFIGURADO."
                    )

                # regra: se rastreável, exige ativo e número de série
                if item.tem_ativo:
                    if not item.ativo.strip() or not item.numero_serie.strip():
                        erros.append(
                            "Item rastreável "
                            f"'{item.equipamento.nome} {item.tipo}' "
                            "exige Ativo e Número de Série."
                        )
                # regra: se contável, exige confirmação
                else:
                    if not item.confirmado:
                        erros.append(
                            f"Item contável '{item.equipamento.nome} {item.tipo}' "
                            "precisa ser confirmado."
                        )

        # ==========================
        # RETORNO (Loja -> Matriz)
        # ==========================
        elif self.tipo == self.Tipo.RETORNO:
            for item in itens:
                # regra: todo item precisa de desfecho
                if not item.status_retorno:
                    erros.append(
                        f"Defina o desfecho de retorno para '{item.equipamento.nome} {item.tipo}'."
                    )
                    continue

                # regra: NAO_RETORNADO exige motivo
                if item.status_retorno == item.StatusRetorno.NAO_RETORNADO:
                    if not item.motivo_nao_retorno.strip():
                        erros.append(
                            "Informe o motivo do não retorno para "
                            f"'{item.equipamento.nome} {item.tipo}'."
                        )

                    # não exige ativo/série em não-retorno
                    continue

                # regra: RETORNADO — se rastreável, exige ativo e número de série
                if item.status_retorno == item.StatusRetorno.RETORNADO:
                    if item.tem_ativo:
                        if not item.ativo.strip() or not item.numero_serie.strip():
                            erros.append(
                                "Item rastreável retornado "
                                f"'{item.equipamento.nome} {item.tipo}' "
                                "exige Ativo e Número de Série."
                            )

        else:
            erros.append(f"Tipo de chamado inválido: {self.tipo}")

        if erros:
            raise ValidationError(erros)

        # finaliza
        self.status = self.Status.FINALIZADO
        self.finalizado_em = timezone.now()
        self.save(update_fields=["status", "finalizado_em"])

    # -----------------------
    # salvar / gerar protocolo
    # -----------------------
    def save(self, *args, **kwargs):  # type: ignore[override]
        # se já tem protocolo, salva normal
        if self.protocolo:
            return super().save(*args, **kwargs)

        data = timezone.now().strftime("%Y%m%d")

        # tenta algumas vezes evitar colisão do unique
        for _ in range(5):
            self.protocolo = f"EX360-{data}-{secrets.token_hex(3).upper()}"
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                # colisão do unique, tenta de novo
                self.protocolo = ""

        # se falhar várias vezes, deixa o erro subir (melhor do que salvar inconsistente)
        return super().save(*args, **kwargs)


# ================
# item da instalação
# ================
class InstalacaoItem(models.Model):
    class StatusRetorno(models.TextChoices):
        RETORNADO = "RETORNADO", "Retornado"
        NAO_RETORNADO = "NAO_RETORNADO", "Não retornado"

    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="itens")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)

    tipo = models.CharField(max_length=80)
    quantidade = models.PositiveIntegerField()

    tem_ativo = models.BooleanField()
    confirmado = models.BooleanField(default=False)

    requer_configuracao = models.BooleanField(
        default=False,
        help_text="Define se o item necessita de configuração técnica após instalação.",
    )

    status_configuracao = models.CharField(
        max_length=20,
        choices=StatusConfiguracao.choices,
        default=StatusConfiguracao.AGUARDANDO,
        help_text="Estado atual do processo de configuração do item.",
    )

    ativo = models.CharField(max_length=80, blank=True, default="")
    numero_serie = models.CharField(max_length=120, blank=True, default="")

    status_retorno = models.CharField(
        max_length=20,
        choices=StatusRetorno.choices,
        null=True,
        blank=True,
        default=None,
        help_text="Obrigatório para itens em Chamado do tipo RETORNO.",
    )

    motivo_nao_retorno = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Obrigatório quando status_retorno=NAO_RETORNADO.",
    )

    class Meta:
        verbose_name = "Item de Instalação"
        verbose_name_plural = "Itens de Instalação"

    def __str__(self) -> str:
        return f"{self.equipamento.nome} {self.tipo} ({self.quantidade})"


class ItemConfiguracaoLog(models.Model):
    item = models.ForeignKey(
        "InstalacaoItem", on_delete=models.CASCADE, related_name="logs_configuracao"
    )
    de_status = models.CharField(max_length=20, choices=StatusConfiguracao.choices)
    para_status = models.CharField(max_length=20, choices=StatusConfiguracao.choices)

    motivo = models.CharField(max_length=255, blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_configuracao_criados",
    )

    class Meta:
        ordering = ["-criado_em", "-id"]

    def __str__(self) -> str:
        return f"{self.item_id}: {self.de_status} -> {self.para_status}"


# ==================
# evidências do chamado
# ==================
class EvidenciaChamado(models.Model):
    class Tipo(models.TextChoices):
        NF_SAIDA = "NF_SAIDA", "NF Saída"
        NF_RETORNO = "NF_RETORNO", "NF Retorno"
        CARTA_CONTEUDO = "CARTA_CONTEUDO", "Carta de Conteúdo"
        EXCECAO = "EXCECAO", "Exceção"
        OUTRO = "OUTRO", "Outro"

    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="evidencias")
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    arquivo = models.FileField(upload_to="execucao/evidencias/")
    descricao = models.CharField(max_length=255, blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em", "-id"]

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} - {self.chamado.protocolo}"
