from __future__ import annotations

from django.urls import reverse
from django.utils import timezone
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from execucao.tests._base import WebAuthBaseTestCase, grant_cap
from iam.models import UserCapability


class TestChamadoFinalizarAjaxView(WebAuthBaseTestCase):
    def _url(self, chamado_id: int) -> str:
        return reverse("execucao:chamado_finalizar", kwargs={"chamado_id": chamado_id})

    def _mk_chamado(
        self,
        *,
        tipo: str = Chamado.Tipo.ENVIO,
        status: str = Chamado.Status.AGUARDANDO_COLETA,
        contabilidade_numero: str = "123",
        nf_saida_numero: str = "999",
        coleta_confirmada_em=None,
    ) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            tipo=tipo,
            status=status,
            contabilidade_numero=contabilidade_numero,
            nf_saida_numero=nf_saida_numero,
            coleta_confirmada_em=coleta_confirmada_em,
        )

    def _grant_finalizar(self) -> None:
        # compat (há variações antigas/novas no projeto)
        grant_cap(self.user, "execucao.chamado_finalizar")
        grant_cap(self.user, "execucao.chamado.finalizar")

    def _revoke_finalizar_caps(self) -> None:
        UserCapability.objects.filter(
            user=self.user,
            capability__code__in=[
                "execucao.chamado.finalizar",
                "execucao.chamado_finalizar",
            ],
        ).delete()

    def test_quando_finalizar_sem_sessao_ativa_entao_retorna_403(self) -> None:
        chamado = self._mk_chamado(coleta_confirmada_em=timezone.now())
        self._grant_finalizar()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 403)

        chamado.refresh_from_db()
        self.assertNotEqual(chamado.status, Chamado.Status.FINALIZADO)

    def test_quando_finalizar_sem_permissao_entao_retorna_403(self) -> None:
        chamado = self._mk_chamado(coleta_confirmada_em=timezone.now())
        create_active_session(chamado=chamado, user=self.user)

        self._revoke_finalizar_caps()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 403)

        chamado.refresh_from_db()
        self.assertNotEqual(chamado.status, Chamado.Status.FINALIZADO)

    def test_quando_finalizar_sem_coleta_confirmada_entao_retorna_400_com_pendencias(
        self,
    ) -> None:
        chamado = self._mk_chamado(coleta_confirmada_em=None)
        create_active_session(chamado=chamado, user=self.user)
        self._grant_finalizar()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        self.assertEqual(data.get("ok"), False)
        self.assertIn("pendencias", data)

        pend = data["pendencias"]
        self.assertTrue(
            any(p["code"] == "COLETA_NAO_CONFIRMADA" for p in pend.get("coleta", []))
        )

        chamado.refresh_from_db()
        self.assertNotEqual(chamado.status, Chamado.Status.FINALIZADO)

    def test_quando_finalizar_com_pendencias_fiscais_entao_retorna_400_listando_codigos(
        self,
    ) -> None:
        chamado = self._mk_chamado(
            coleta_confirmada_em=timezone.now(),
            contabilidade_numero="",
            nf_saida_numero="",
        )
        create_active_session(chamado=chamado, user=self.user)
        self._grant_finalizar()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        pend = data["pendencias"]

        codes = {p["code"] for p in pend.get("fiscais", [])}
        self.assertIn("FISCAL_FALTA_CONTABIL", codes)
        self.assertIn("FISCAL_FALTA_NF_SAIDA", codes)

        chamado.refresh_from_db()
        self.assertNotEqual(chamado.status, Chamado.Status.FINALIZADO)

    def test_quando_finalizar_com_nf_saida_invalida_entao_retorna_400_listando_codigo(
        self,
    ) -> None:
        chamado = self._mk_chamado(
            coleta_confirmada_em=timezone.now(),
            contabilidade_numero="123",
            nf_saida_numero="12A",
        )
        create_active_session(chamado=chamado, user=self.user)
        self._grant_finalizar()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        pend = data["pendencias"]

        codes = {p["code"] for p in pend.get("fiscais", [])}
        self.assertIn("FISCAL_NF_SAIDA_INVALIDA", codes)

        chamado.refresh_from_db()
        self.assertNotEqual(chamado.status, Chamado.Status.FINALIZADO)

    def test_quando_finalizar_com_tudo_ok_entao_muda_status_para_finalizado_e_encerra_sessao(
        self,
    ) -> None:
        chamado = self._mk_chamado(
            coleta_confirmada_em=timezone.now(),
            contabilidade_numero="123",
            nf_saida_numero="999",
        )
        sessao = create_active_session(chamado=chamado, user=self.user)
        self._grant_finalizar()

        resp = self.client.post(
            self._url(chamado.id),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data.get("ok"), True)

        chamado.refresh_from_db()
        self.assertEqual(chamado.status, Chamado.Status.FINALIZADO)

        sessao.refresh_from_db()
        self.assertIsNotNone(sessao.ended_at)
        self.assertEqual(sessao.ended_reason, "FINALIZE")
