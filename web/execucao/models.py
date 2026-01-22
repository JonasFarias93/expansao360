from cadastro.models import Equipamento, Kit, Loja, Projeto, Subprojeto
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Chamado(models.Model):
    class Status(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        EM_EXECUCAO = "EM_EXECUCAO", "Em execução"
        FINALIZADO = "FINALIZADO", "Finalizado"

    loja = models.ForeignKey(Loja, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    subprojeto = models.ForeignKey(Subprojeto, on_delete=models.PROTECT)
    kit = models.ForeignKey(Kit, on_delete=models.PROTECT)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTO)
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)
    protocolo = models.CharField(max_length=32, unique=True, editable=False)

    servicenow_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)
    contabilidade_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)
    nf_saida_numero = models.CharField(max_length=40, unique=True, null=True, blank=True)

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
            )


def finalizar(self) -> None:
    if self.status == self.Status.FINALIZADO:
        raise ValidationError("Chamado já está finalizado.")

    itens = list(self.itens.all())
    if not itens:
        raise ValidationError("Não é possível finalizar um chamado sem itens.")

    erros: list[str] = []

    for item in itens:
        if item.requer_configuracao and item.status_configuracao != StatusConfiguracao.CONFIGURADO:
            erros.append(
                "Não é possível finalizar: "
                f"'{item.equipamento.nome} {item.tipo}' ainda não foi marcado como CONFIGURADO."
            )

        if item.tem_ativo:
            if not item.ativo.strip() or not item.numero_serie.strip():
                erros.append(
                    "Item rastreável "
                    f"'{item.equipamento.nome} {item.tipo}' "
                    "exige Ativo e Número de Série."
                )
        else:
            if not item.confirmado:
                erros.append(
                    f"Item contável '{item.equipamento.nome} {item.tipo}' precisa ser confirmado."
                )

    if erros:
        raise ValidationError(erros)

    self.status = self.Status.FINALIZADO
    self.finalizado_em = timezone.now()
    self.save(update_fields=["status", "finalizado_em"])


class StatusConfiguracao(models.TextChoices):
    AGUARDANDO = "AGUARDANDO", "Aguardando"
    EM_CONFIGURACAO = "EM_CONFIGURACAO", "Em configuração"
    CONFIGURADO = "CONFIGURADO", "Configurado"


class InstalacaoItem(models.Model):
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

    class Meta:
        verbose_name = "Item de Instalação"
        verbose_name_plural = "Itens de Instalação"

    def __str__(self) -> str:
        return f"{self.equipamento.nome} {self.tipo} ({self.quantidade})"


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

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} - {self.chamado.protocolo}"
