from __future__ import annotations

from cadastro.models import Equipamento, ItemKit, TipoEquipamento
from django.contrib.auth import get_user_model
from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from execucao.tests._base import WebAuthBaseTestCase


class TestItemConfigurarEndpoint(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # kit com 1 item
        tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="Micro")
        eq = Equipamento.objects.create(
            categoria=self.categoria,
            codigo="MICRO",
            nome="Micro",
        )
        ItemKit.objects.create(kit=self.kit, equipamento=eq, tipo=tipo, quantidade=1)

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )
        self.chamado.gerar_itens_de_instalacao()
        self.item = self.chamado.itens.get()

    def _abrir_chamado_e_iniciar_sessao(self) -> None:
        url = reverse("execucao:chamado_abrir", args=[self.chamado.id])
        resp = self.client.post(url)
        assert resp.status_code in (302, 200)

    def test_quando_com_sessao_e_perm_entao_marca_configurado_e_registra_auditoria(
        self,
    ) -> None:
        self._abrir_chamado_e_iniciar_sessao()

        url = reverse("execucao:item_configurar", args=[self.item.id])
        resp = self.client.post(url)
        assert resp.status_code == 200

        self.item.refresh_from_db()
        assert self.item.configurado_em is not None
        assert self.item.configurado_por_id == self.user.id

    def test_quando_sem_sessao_entao_retorna_403(self) -> None:
        url = reverse("execucao:item_configurar", args=[self.item.id])
        resp = self.client.post(url)
        assert resp.status_code == 403

    def test_quando_sem_permissao_entao_retorna_403(self) -> None:
        User = get_user_model()
        u2 = User.objects.create_user(username="semcap", password="x")
        self.client.force_login(u2)

        create_active_session(chamado=self.chamado, user=u2)

        url = reverse("execucao:item_configurar", args=[self.item.id])
        resp = self.client.post(url)

        assert resp.status_code == 403

    def test_quando_duplo_clique_entao_e_idempotente_e_mantem_auditoria(self) -> None:
        self._abrir_chamado_e_iniciar_sessao()
        url = reverse("execucao:item_configurar", args=[self.item.id])

        r1 = self.client.post(url)
        assert r1.status_code == 200
        self.item.refresh_from_db()
        em1 = self.item.configurado_em
        por1 = self.item.configurado_por_id

        r2 = self.client.post(url)
        assert r2.status_code == 200
        self.item.refresh_from_db()

        assert self.item.configurado_em == em1
        assert self.item.configurado_por_id == por1
