# Create your models here.
from cadastro.models import Equipamento, Kit, Loja, Projeto, Subprojeto
from django.db import models


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


class InstalacaoItem(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="itens")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=80)
    quantidade = models.PositiveIntegerField()

    tem_ativo = models.BooleanField()

    confirmado = models.BooleanField(default=False)

    ativo = models.CharField(max_length=80, blank=True, default="")
    numero_serie = models.CharField(max_length=120, blank=True, default="")
