from __future__ import annotations

from django.urls import reverse
from django.utils import timezone
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from execucao.tests._base import WebAuthBaseTestCase, grant_cap


class TestChamadoFinalizarPendenciasItensAjaxView(WebAuthBaseTestCase):
    def _url(self, chamado_id: int) -> str:
        return reverse("execucao:chamado_finalizar", kwargs={"chamado_id": chamado_id})

    def _mk_chamado(self, *, coleta_confirmada_em) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            coleta_confirmada_em=coleta_confirmada_em,
        )

    def _grant_finalizar(self) -> None:
        grant_cap(self.user, "execucao.chamado_finalizar")
        grant_cap(self.user, "execucao.chamado.finalizar")

    def test_quando_finalizar_com_pendencias_de_itens_entao_retorna_400_listando_itens(
        self,
    ) -> None:
        chamado = self._mk_chamado(coleta_confirmada_em=timezone.now())
        create_active_session(chamado=chamado, user=self.user)
        self._grant_finalizar()

        chamado.gerar_itens_de_instalacao()
        item = chamado.itens.first()
        if item is None:
            self.skipTest("Chamado não gerou itens no cenário de teste.")

        # força pendência se existir campo serial/ativo/configurado
        changed = False
        if hasattr(item, "serial"):
            item.serial = ""
            changed = True
        if hasattr(item, "ativo"):
            item.ativo = ""
            changed = True
        if hasattr(item, "configurado_em") and getattr(item, "deve_configurar", False):
            item.configurado_em = None
            changed = True

        if not changed:
            self.skipTest(
                "Model de item não possui campos rastreáveis/configuráveis para este MVP."
            )

        item.save()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 400)

        pend = resp.json()["pendencias"]["itens"]
        self.assertTrue(len(pend) >= 1)
