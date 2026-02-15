from __future__ import annotations

from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from execucao.tests._base import WebAuthBaseTestCase
from iam.models import UserCapability


class TestChamadoSalvarDadosFiscaisPermissoesView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

    def _url(self) -> str:
        return reverse("execucao:chamado_salvar_dados_fiscais", args=[self.chamado.id])

    def test_quando_sem_sessao_entao_retorna_403(self) -> None:
        resp = self.client.post(
            self._url(),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": "123"},
        )
        self.assertEqual(resp.status_code, 403)

    def test_quando_sem_capability_editar_entao_retorna_403(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        UserCapability.objects.filter(
            user=self.user,
            capability__code="execucao.chamado_editar",
        ).delete()

        resp = self.client.post(
            self._url(),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": "123"},
        )
        self.assertEqual(resp.status_code, 403)

    def test_quando_com_sessao_e_capability_entao_salva_e_normaliza_campos(
        self,
    ) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        resp = self.client.post(
            self._url(),
            data={"contabilidade_numero": "  PED-001  ", "nf_saida_numero": " 123 45 "},
        )
        self.assertEqual(resp.status_code, 302)

        self.chamado.refresh_from_db()
        self.assertEqual(self.chamado.contabilidade_numero, "PED-001")
        self.assertEqual(self.chamado.nf_saida_numero, "12345")

    def test_quando_nf_tem_letras_entao_nao_salva_nf_saida(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        resp = self.client.post(
            self._url(),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": "12A3"},
        )
        self.assertEqual(resp.status_code, 302)

        self.chamado.refresh_from_db()
        self.assertFalse((self.chamado.nf_saida_numero or "").strip())
