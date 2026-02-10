from __future__ import annotations

from cadastro.models import Equipamento, ItemKit, TipoEquipamento
from django.contrib.auth import get_user_model
from django.utils import timezone

from execucao.models import Chamado
from execucao.tests._base import ChamadoBaseTestCase


class InstalacaoItemConfiguradoAuditTests(ChamadoBaseTestCase):
    def test_item_registra_configurado_em_e_por(self) -> None:
        User = get_user_model()
        tec = User.objects.create_user(username="tec", password="x")

        # mínimo para gerar itens do chamado via kit.itens
        tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="Micro")
        eq = Equipamento.objects.create(categoria=self.categoria, codigo="MICRO", nome="Micro")

        ItemKit.objects.create(
            kit=self.kit,
            equipamento=eq,
            tipo=tipo,
            quantidade=1,
            requer_configuracao=False,
        )

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status="ABERTO",
        )

        chamado.gerar_itens_de_instalacao()
        item = chamado.itens.get()

        now = timezone.now()
        item.configurado_em = now
        item.configurado_por = tec
        item.save()

        item.refresh_from_db()
        self.assertIsNotNone(item.configurado_em)
        self.assertEqual(item.configurado_por_id, tec.id)
        self.assertTrue(item.configurado)
