from __future__ import annotations

from cadastro.models import Categoria, Equipamento, ItemKit, Kit, TipoEquipamento
from django.urls import reverse
from execucao.models import Chamado
from execucao.services.execution_session import (
    create_active_session,
    get_active_session,
)
from execucao.tests._base import WebAuthBaseTestCase


class TestChamadoSalvarExecucaoAjaxView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._url = lambda cid: reverse(
            "execucao:chamado_salvar_execucao_ajax", kwargs={"chamado_id": cid}
        )

        self.chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.ABERTO,
            tipo=Chamado.Tipo.ENVIO,
        )

    def _setup_kit_com_itens_gate_nf(self) -> Kit:
        categoria = Categoria.objects.create(nome="Informatica")
        tipo = TipoEquipamento.objects.create(categoria=categoria, nome="TC")
        kit = Kit.objects.create(nome="Kit Gate NF (tests)")

        eq_rastreavel = Equipamento.objects.create(
            codigo="MICRO_TC_TEST",
            nome="Micro TC",
            categoria=categoria,
            tem_ativo=True,
            configuravel=True,
        )
        eq_contavel = Equipamento.objects.create(
            codigo="MOUSE_TEST",
            nome="Mouse",
            categoria=categoria,
            tem_ativo=False,
            configuravel=False,
        )

        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_rastreavel,
            quantidade=2,
            requer_configuracao=False,
        )
        ItemKit.objects.create(
            kit=kit,
            tipo=tipo,
            equipamento=eq_contavel,
            quantidade=2,
            requer_configuracao=False,
        )
        return kit

    def _ensure_itens_gerados(self, chamado: Chamado) -> None:
        if not chamado.itens.exists():
            chamado.gerar_itens_de_instalacao()

    def _deixar_itens_ok_para_gate_nf(self, chamado: Chamado) -> None:
        self._ensure_itens_gerados(chamado)

        for item in chamado.itens.all():
            if item.tem_ativo:
                item.ativo = "ATV-123"
                item.numero_serie = "SN-123"
                item.save(update_fields=["ativo", "numero_serie"])
            else:
                item.confirmado = True
                item.save(update_fields=["confirmado"])

        assert chamado.pode_liberar_nf() is True

    def test_salvar_sem_sessao_retorna_403(self) -> None:
        resp = self.client.post(
            self._url(self.chamado.id),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": ""},
        )
        self.assertEqual(resp.status_code, 403)

    def test_primeiro_save_promove_em_execucao_e_mantem_sessao(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        resp = self.client.post(
            self._url(self.chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        self.chamado.refresh_from_db()
        self.assertEqual(str(self.chamado.status), str(Chamado.Status.EM_EXECUCAO))

        self.assertIsNotNone(get_active_session(chamado=self.chamado))

    def test_gate_nf_ok_promove_aguardando_nf_e_mantem_sessao(self) -> None:
        kit = self._setup_kit_com_itens_gate_nf()

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        create_active_session(chamado=chamado, user=self.user)

        self._deixar_itens_ok_para_gate_nf(chamado)
        chamado.contabilidade_numero = "PED-001"
        chamado.save(update_fields=["contabilidade_numero"])

        resp = self.client.post(
            self._url(chamado.id),
            data={"contabilidade_numero": "PED-001", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        chamado.refresh_from_db()
        self.assertEqual(str(chamado.status), str(Chamado.Status.AGUARDANDO_NF))

        self.assertIsNotNone(get_active_session(chamado=chamado))

    def test_nf_saida_preenchida_promove_aguardando_coleta_e_mantem_sessao(
        self,
    ) -> None:
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        create_active_session(chamado=chamado, user=self.user)

        resp = self.client.post(
            self._url(chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": "12345"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        chamado.refresh_from_db()
        self.assertEqual(str(chamado.status), str(Chamado.Status.AGUARDANDO_COLETA))

        self.assertIsNotNone(get_active_session(chamado=chamado))

    def test_item_configurado_promove_em_configuracao_e_mantem_sessao(self) -> None:
        kit = self._setup_kit_com_itens_gate_nf()

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        self._ensure_itens_gerados(chamado)
        item = chamado.itens.first()
        assert item is not None

        create_active_session(chamado=chamado, user=self.user)

        url_cfg = reverse("execucao:item_configurar", args=[item.id])
        self.client.post(url_cfg)

        resp = self.client.post(
            self._url(chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)

        chamado.refresh_from_db()
        self.assertEqual(str(chamado.status), str(Chamado.Status.EM_CONFIGURACAO))

        self.assertIsNotNone(get_active_session(chamado=chamado))

    def test_salvar_persiste_itens_e_mantem_sessao(self) -> None:
        kit = self._setup_kit_com_itens_gate_nf()

        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=kit,
            status=Chamado.Status.EM_EXECUCAO,
            tipo=Chamado.Tipo.ENVIO,
        )

        self._ensure_itens_gerados(chamado)

        rastreavel = chamado.itens.filter(tem_ativo=True).first()
        contavel = chamado.itens.filter(tem_ativo=False).first()

        create_active_session(chamado=chamado, user=self.user)

        self.client.post(
            self._url(chamado.id),
            data={
                f"ativo_{rastreavel.id}": "ATV-999",
                f"serie_{rastreavel.id}": "SN-999",
                f"confirmado_{contavel.id}": "on",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertIsNotNone(get_active_session(chamado=chamado))

        rastreavel.refresh_from_db()
        self.assertEqual(rastreavel.ativo, "ATV-999")
        self.assertEqual(rastreavel.numero_serie, "SN-999")

        contavel.refresh_from_db()
        self.assertTrue(contavel.confirmado)

    def test_salvar_execucao_mantem_sessao_ativa(self) -> None:
        create_active_session(chamado=self.chamado, user=self.user)

        self.client.post(
            self._url(self.chamado.id),
            data={"contabilidade_numero": "", "nf_saida_numero": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertIsNotNone(get_active_session(chamado=self.chamado))
