from __future__ import annotations
from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import create_active_session
from ._base import WebAuthBaseTestCase, grant_cap
from django.utils import timezone


class TestChamadoDetalheGetView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "execucao.chamado.visualizar")

    def test_quando_em_abertura_entao_redireciona_para_setup(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.EM_ABERTURA,
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("execucao:chamado_setup", args=[chamado.id]))

    def test_quando_aberto_entao_renderiza_template_execucao_com_contexto(self) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "execucao/chamado_execucao.html")
        self.assertIn("chamado", resp.context)
        self.assertEqual(resp.context["chamado"].id, chamado.id)

    def test_quando_renderiza_execucao_entao_inclui_script_execucao_detalhe_js(
        self,
    ) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode("utf-8")
        self.assertIn("execucao/js/execucao_detalhe.js", html)

    def test_quando_renderiza_execucao_entao_expoe_execution_root_data_attrs_contract(
        self,
    ) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
        )

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode("utf-8")

        self.assertIn('id="execution-root"', html)
        self.assertIn("data-has-session=", html)
        self.assertIn("data-can-edit=", html)
        self.assertIn("data-can-finalize=", html)

    def test_reabertura_renderiza_ativo_e_serie_persistidos_nos_inputs(self) -> None:
        # Kit determinístico: 1 equipamento rastreável (tem_ativo=True)
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

        resp = self.client.get(
            reverse("execucao:chamado_detalhe", kwargs={"chamado_id": chamado.id})
        )
        self.assertEqual(resp.status_code, 200)

        html = resp.content.decode("utf-8")

        self.assertIn(f'name="ativo_{item.id}"', html)
        self.assertIn('value="ATV-REENTRADA"', html)

        self.assertIn(f'name="serie_{item.id}"', html)
        self.assertIn('value="SN-REENTRADA"', html)

    def test_quando_gates_ok_entao_can_finalize_1_e_btn_finalizar_habilitado(
        self,
    ) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

        # sessão ativa costuma ser pré-condição do "modo execução"
        create_active_session(chamado=chamado, user=self.user)

        # pré-requisitos típicos
        chamado.contabilidade_numero = "14141414"
        chamado.nf_saida_numero = "14141414"
        chamado.coleta_confirmada_em = timezone.now()
        chamado.save()

        url = reverse("execucao:chamado_detalhe", args=[chamado.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode("utf-8")

        # contrato do state manager
        self.assertIn('data-can-finalize="1"', html)

        # botão habilitado (sem disabled)
        self.assertIn('id="btn-finalizar-chamado"', html)
        self.assertNotIn('id="btn-finalizar-chamado" disabled', html)
        self.assertNotIn('id="btn-finalizar-chamado"\n            disabled', html)
