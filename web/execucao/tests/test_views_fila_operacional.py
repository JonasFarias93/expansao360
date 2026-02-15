from __future__ import annotations

from django.urls import reverse
from django.utils import timezone
from execucao.models import Chamado

from ._base import WebAuthBaseTestCase, grant_cap


class TestFilaOperacionalGetView(WebAuthBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        grant_cap(self.user, "execucao.chamado.visualizar")

    def _criar_chamado(self, *, prioridade: str, status: str) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            prioridade=prioridade,
            status=status,
            criado_em=timezone.now(),
        )

    def test_quando_renderiza_fila_entao_counts_considera_apenas_chamados_na_fila(
        self,
    ) -> None:
        # Na fila
        self._criar_chamado(
            prioridade=Chamado.Prioridade.CRITICA,
            status=Chamado.Status.ABERTO,
        )
        self._criar_chamado(
            prioridade=Chamado.Prioridade.CRITICA,
            status=Chamado.Status.EM_EXECUCAO,
        )
        self._criar_chamado(
            prioridade=Chamado.Prioridade.ALTA,
            status=Chamado.Status.ABERTO,
        )

        # Fora da fila
        self._criar_chamado(
            prioridade=Chamado.Prioridade.BAIXA,
            status=Chamado.Status.FINALIZADO,
        )

        resp = self.client.get(reverse("execucao:fila"))
        self.assertEqual(resp.status_code, 200)

        counts = resp.context["counts"]
        self.assertEqual(counts["total"], 3)
        self.assertEqual(counts["critico"], 2)
        self.assertEqual(counts["alto"], 1)
        self.assertEqual(counts["medio"], 0)
        self.assertEqual(counts["baixo"], 0)

    def test_quando_prio_filtrada_entao_retorna_apenas_prioridade_selecionada(
        self,
    ) -> None:
        crit = self._criar_chamado(
            prioridade=Chamado.Prioridade.CRITICA,
            status=Chamado.Status.ABERTO,
        )
        self._criar_chamado(
            prioridade=Chamado.Prioridade.ALTA,
            status=Chamado.Status.ABERTO,
        )

        resp = self.client.get(reverse("execucao:fila") + "?prio=CRITICO")
        self.assertEqual(resp.status_code, 200)

        rows = resp.context["chamados"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["chamado"].id, crit.id)
        self.assertEqual(resp.context["prio_selected"], "CRITICO")

    def test_quando_prio_invalida_entao_ignora_filtro_e_prio_selected_e_none(
        self,
    ) -> None:
        self._criar_chamado(
            prioridade=Chamado.Prioridade.CRITICA,
            status=Chamado.Status.ABERTO,
        )
        self._criar_chamado(
            prioridade=Chamado.Prioridade.ALTA,
            status=Chamado.Status.ABERTO,
        )

        resp = self.client.get(reverse("execucao:fila") + "?prio=QUALQUERCOISA")
        self.assertEqual(resp.status_code, 200)

        rows = resp.context["chamados"]
        self.assertEqual(len(rows), 2)
        self.assertIsNone(resp.context["prio_selected"])
