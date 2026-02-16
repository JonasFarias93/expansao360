from __future__ import annotations

from chamados.models import Chamado
from chamados.selectors.fila import FILA_STATUSES, fila_base_queryset, fila_counts

from ._base import ChamadoBaseTestCase


class TestFilaSelectorBaseQuerysetECounts(ChamadoBaseTestCase):
    def _criar_chamado(
        self,
        *,
        status: str,
        prioridade: str | None = None,
        protocolo: str,
    ) -> Chamado:
        """
        Fixture mínima e determinística para Chamado com FKs obrigatórias já
        providas pelo ChamadoBaseTestCase.
        """
        payload: dict[str, object] = {
            "loja": self.loja,
            "projeto": self.projeto,
            "subprojeto": self.sub,
            "kit": self.kit,
            "tipo": Chamado.Tipo.ENVIO,
            "status": status,
            "protocolo": protocolo,
        }
        if prioridade is not None:
            payload["prioridade"] = prioridade

        return Chamado.objects.create(**payload)

    def test_quando_buscar_queryset_base_da_fila_entao_filtra_apenas_status_operacionais(
        self,
    ) -> None:
        ch_ok = self._criar_chamado(
            status=Chamado.Status.ABERTO,
            protocolo="FILA-1",
        )
        ch_out_1 = self._criar_chamado(
            status=Chamado.Status.EM_ABERTURA,
            protocolo="OUT-1",
        )
        ch_out_2 = self._criar_chamado(
            status=Chamado.Status.FINALIZADO,
            protocolo="OUT-2",
        )

        qs = fila_base_queryset()
        ids = set(qs.values_list("id", flat=True))

        assert ch_ok.id in ids
        assert ch_out_1.id not in ids
        assert ch_out_2.id not in ids

        assert set(qs.values_list("status", flat=True)).issubset(set(FILA_STATUSES))

    def test_dado_chamados_com_prioridades_quando_calcular_counts_entao_agregados_conferem_e_ignoram_fora_da_fila(
        self,
    ) -> None:
        self._criar_chamado(
            status=Chamado.Status.ABERTO,
            prioridade=Chamado.Prioridade.CRITICA,
            protocolo="C-1",
        )
        self._criar_chamado(
            status=Chamado.Status.EM_EXECUCAO,
            prioridade=Chamado.Prioridade.CRITICA,
            protocolo="C-2",
        )
        self._criar_chamado(
            status=Chamado.Status.AGUARDANDO_NF,
            prioridade=Chamado.Prioridade.ALTA,
            protocolo="C-3",
        )
        self._criar_chamado(
            status=Chamado.Status.AGUARDANDO_COLETA,
            prioridade=Chamado.Prioridade.MEDIA,
            protocolo="C-4",
        )

        # fora da fila (não pode contar)
        self._criar_chamado(
            status=Chamado.Status.FINALIZADO,
            prioridade=Chamado.Prioridade.CRITICA,
            protocolo="OUT-3",
        )
        self._criar_chamado(
            status=Chamado.Status.EM_ABERTURA,
            prioridade=Chamado.Prioridade.ALTA,
            protocolo="OUT-4",
        )

        counts = fila_counts(fila_base_queryset())

        assert counts["total"] == 4
        assert counts["critico"] == 2
        assert counts["alto"] == 1
        assert counts["medio"] == 1
        assert counts["baixo"] == 0
