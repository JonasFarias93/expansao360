from __future__ import annotations


from django.urls import reverse
from django.utils import timezone

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from iam.execucao_capabilities import CAP_EXECUCAO_CHAMADO_FINALIZAR
from iam.models import UserCapability

from ._base import WebAuthBaseTestCase, grant_cap


class TestChamadoDetalheGetView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "execucao.chamado.visualizar")

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _url(self, chamado_id: int) -> str:
        return reverse("execucao:chamado_detalhe", args=[chamado_id])

    def _mk_chamado_base(
        self,
        *,
        status: str = Chamado.Status.ABERTO,
        tipo: str = Chamado.Tipo.ENVIO,
    ) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=status,
            tipo=tipo,
        )

    def _make_itens_ok(self, chamado: Chamado) -> None:
        chamado.gerar_itens_de_instalacao()

        for item in chamado.itens.all():
            changed: list[str] = []

            if getattr(item, "tem_ativo", False):
                if hasattr(item, "ativo"):
                    item.ativo = "ATV-OK"
                    changed.append("ativo")
                if hasattr(item, "numero_serie"):
                    item.numero_serie = "SN-OK"
                    changed.append("numero_serie")
            else:
                if hasattr(item, "confirmado"):
                    item.confirmado = True
                    changed.append("confirmado")

            if changed:
                item.save(update_fields=changed)

    def _assert_data_can_finalize(self, html: str, expected: str) -> None:
        pattern = rf'data-can-finalize\s*=\s*["\']?{expected}["\']?'
        self.assertRegex(html, pattern)

    def _assert_btn_enabled(self, html: str) -> None:
        self.assertIn('id="btn-finalizar-chamado"', html)
        self.assertNotRegex(html, r'id="btn-finalizar-chamado"[^>]*\sdisabled')

    # ---------------------------------------------------------
    # Básicos
    # ---------------------------------------------------------

    def test_quando_em_abertura_entao_redireciona_para_setup(self) -> None:
        chamado = self._mk_chamado_base(status=Chamado.Status.EM_ABERTURA)

        resp = self.client.get(self._url(chamado.id))

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp.url,
            reverse("execucao:chamado_setup", args=[chamado.id]),
        )

    def test_quando_aberto_entao_renderiza_template_execucao_com_contexto(self) -> None:
        chamado = self._mk_chamado_base(status=Chamado.Status.ABERTO)

        resp = self.client.get(self._url(chamado.id))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "execucao/chamado_execucao.html")
        self.assertIn("chamado", resp.context)
        self.assertEqual(resp.context["chamado"].id, chamado.id)

    def test_quando_renderiza_execucao_entao_expoe_execution_root_data_attrs_contract(
        self,
    ) -> None:
        chamado = self._mk_chamado_base(status=Chamado.Status.ABERTO)

        resp = self.client.get(self._url(chamado.id))
        html = resp.content.decode("utf-8")

        self.assertIn('id="execution-root"', html)
        self.assertIn("data-has-session=", html)
        self.assertIn("data-can-edit=", html)
        self.assertIn("data-can-finalize=", html)

    # ---------------------------------------------------------
    # Reentrada rastreável
    # ---------------------------------------------------------

    def test_reabertura_renderiza_ativo_e_serie_persistidos_nos_inputs(self) -> None:
        categoria = Categoria.objects.create(nome="Informatica")
        tipo = TipoEquipamento.objects.create(categoria=categoria, nome="TC")
        kit = Kit.objects.create(nome="Kit Reentrada (tests)")

        eq_rastreavel = Equipamento.objects.create(
            codigo="MICRO_REENTRADA_TEST",
            nome="Micro Reentrada",
            categoria=categoria,
            tem_ativo=True,
            configuravel=True,
        )

        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_rastreavel,
            quantidade=1,
            requer_configuracao=False,
        )

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        chamado.gerar_itens_de_instalacao()
        item = chamado.itens.get(tem_ativo=True)

        item.ativo = "ATV-REENTRADA"
        item.numero_serie = "SN-REENTRADA"
        item.save(update_fields=["ativo", "numero_serie"])

        resp = self.client.get(self._url(chamado.id))
        html = resp.content.decode("utf-8")

        self.assertIn(f'name="ativo_{item.id}"', html)
        self.assertIn('value="ATV-REENTRADA"', html)
        self.assertIn(f'name="serie_{item.id}"', html)
        self.assertIn('value="SN-REENTRADA"', html)

    # ---------------------------------------------------------
    # Finalizar - OK
    # ---------------------------------------------------------

    def test_quando_tudo_ok_entao_can_finalize_1_e_btn_habilitado(self) -> None:
        grant_cap(self.user, CAP_EXECUCAO_CHAMADO_FINALIZAR)

        chamado = self._mk_chamado_base()
        create_active_session(chamado=chamado, user=self.user)

        chamado.contabilidade_numero = "14141414"
        chamado.nf_saida_numero = "14141414"
        chamado.coleta_confirmada_em = timezone.now()
        chamado.save()

        self._make_itens_ok(chamado)

        resp = self.client.get(self._url(chamado.id))
        html = resp.content.decode("utf-8")

        self._assert_data_can_finalize(html, "1")
        self._assert_btn_enabled(html)

    # ---------------------------------------------------------
    # Finalizar - Bordas
    # ---------------------------------------------------------

    def test_quando_sem_sessao_entao_can_finalize_0(self) -> None:
        grant_cap(self.user, CAP_EXECUCAO_CHAMADO_FINALIZAR)

        chamado = self._mk_chamado_base()

        chamado.contabilidade_numero = "14141414"
        chamado.nf_saida_numero = "14141414"
        chamado.coleta_confirmada_em = timezone.now()
        chamado.save()

        self._make_itens_ok(chamado)

        resp = self.client.get(self._url(chamado.id))
        html = resp.content.decode("utf-8")

        # sem sessão, o botão pode nem existir. contrato é o que importa.
        self._assert_data_can_finalize(html, "0")

    def test_quando_sem_permissao_finalizar_entao_can_finalize_0(self) -> None:
        # remove permissões herdadas da base
        UserCapability.objects.filter(
            user=self.user,
            capability__code=CAP_EXECUCAO_CHAMADO_FINALIZAR,
        ).delete()
        UserCapability.objects.filter(
            user=self.user,
            capability__code="execucao.chamado.finalizar",
        ).delete()

        chamado = self._mk_chamado_base()
        create_active_session(chamado=chamado, user=self.user)

        chamado.contabilidade_numero = "14141414"
        chamado.nf_saida_numero = "14141414"
        chamado.coleta_confirmada_em = timezone.now()
        chamado.save()

        self._make_itens_ok(chamado)

        resp = self.client.get(self._url(chamado.id))
        html = resp.content.decode("utf-8")

        # sem permissão, botão pode ou não existir. contrato é o que importa.
        self._assert_data_can_finalize(html, "0")
