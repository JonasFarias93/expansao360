from __future__ import annotations

from cadastro.models import Equipamento, ItemKit, TipoEquipamento
from django.urls import reverse

from execucao.models import Chamado
from execucao.tests._base import WebAuthBaseTestCase


class ItemConfigurarEndpointTests(WebAuthBaseTestCase):
    def _criar_chamado_com_item(self) -> tuple[Chamado, int]:
        tipo = TipoEquipamento.objects.create(categoria=self.categoria, nome="Micro")
        eq = Equipamento.objects.create(categoria=self.categoria, codigo="MICRO", nome="Micro")
        ItemKit.objects.create(kit=self.kit, equipamento=eq, tipo=tipo, quantidade=1)

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status="ABERTO",
        )
        chamado.gerar_itens_de_instalacao()
        item = chamado.itens.get()
        return chamado, item.id

    def _abrir_chamado_e_iniciar_sessao(self, chamado: Chamado) -> None:
        url = reverse("execucao:chamado_abrir", args=[chamado.id])
        resp = self.client.post(url)
        assert resp.status_code in (200, 302)

    def test_post_configurar_item_retorna_200_e_marca_auditoria(self) -> None:
        chamado, item_id = self._criar_chamado_com_item()
        self._abrir_chamado_e_iniciar_sessao(chamado)

        url = reverse("execucao:item_configurar", args=[item_id])
        resp = self.client.post(url)

        assert resp.status_code == 200
        payload = resp.json()
        assert payload["ok"] is True
        assert payload["already_configured"] is False

    def test_post_configurar_item_e_idempotente(self) -> None:
        chamado, item_id = self._criar_chamado_com_item()
        self._abrir_chamado_e_iniciar_sessao(chamado)

        url = reverse("execucao:item_configurar", args=[item_id])

        r1 = self.client.post(url)
        assert r1.status_code == 200

        r2 = self.client.post(url)
        assert r2.status_code == 200
        assert r2.json()["already_configured"] is True
