from __future__ import annotations

from django.apps import apps

from chamados.models import Chamado, InstalacaoItem, StatusConfiguracao
from chamados.selectors.fila_rows import build_fila_rows

from ._base import ChamadoBaseTestCase


def _get_model(app_label: str, *names: str):
    for n in names:
        try:
            return apps.get_model(app_label, n)
        except LookupError:
            continue
    raise LookupError(f"Não achei model {app_label}.{names!r}")


class TestFilaRowsBuilder(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._eq_seq = 0

    def _mk_chamado(self, *, protocolo: str) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
            status=Chamado.Status.ABERTO,
            protocolo=protocolo,
        )

    def _mk_equipamento(self, *, tem_ativo: bool, configuravel: bool = True):
        Equipamento = _get_model("cadastro", "Equipamento")

        self._eq_seq += 1
        return Equipamento.objects.create(
            codigo=f"EQ{self._eq_seq}",
            nome=f"Equipamento {self._eq_seq}",
            categoria=self.categoria,
            tem_ativo=tem_ativo,
            configuravel=configuravel,
        )

    def _mk_item(
        self,
        *,
        chamado: Chamado,
        tem_ativo: bool,
        deve_configurar: bool,
    ) -> InstalacaoItem:
        equipamento = self._mk_equipamento(tem_ativo=tem_ativo)

        return InstalacaoItem.objects.create(
            chamado=chamado,
            equipamento=equipamento,
            quantidade=1,
            tem_ativo=tem_ativo,
            deve_configurar=deve_configurar,
        )

    def test_dado_itens_rastreaveis_quando_builder_entao_conta_bipados_por_ativo_e_numero_serie(
        self,
    ) -> None:
        ch = self._mk_chamado(protocolo="ROW-1")

        i1 = self._mk_item(chamado=ch, tem_ativo=True, deve_configurar=False)
        i1.ativo = "A1"
        i1.numero_serie = "S1"
        i1.save(update_fields=["ativo", "numero_serie"])

        i2 = self._mk_item(chamado=ch, tem_ativo=True, deve_configurar=False)
        i2.ativo = "A2"
        i2.numero_serie = ""  # sem série -> não bipado
        i2.save(update_fields=["ativo", "numero_serie"])

        rows = build_fila_rows([ch])

        assert rows[0]["bip_total"] == 2
        assert rows[0]["bipados"] == 1

    def test_dado_itens_contaveis_quando_builder_entao_conta_checados_por_confirmado(
        self,
    ) -> None:
        ch = self._mk_chamado(protocolo="ROW-2")

        i1 = self._mk_item(chamado=ch, tem_ativo=False, deve_configurar=False)
        i1.confirmado = True
        i1.save(update_fields=["confirmado"])

        i2 = self._mk_item(chamado=ch, tem_ativo=False, deve_configurar=False)
        i2.confirmado = False
        i2.save(update_fields=["confirmado"])

        rows = build_fila_rows([ch])

        assert rows[0]["check_total"] == 2
        assert rows[0]["checados"] == 1

    def test_dado_itens_configuraveis_quando_builder_entao_conta_cfg_done_por_configurado_e_ip(
        self,
    ) -> None:
        ch = self._mk_chamado(protocolo="ROW-3")

        i1 = self._mk_item(chamado=ch, tem_ativo=False, deve_configurar=True)
        i1.status_configuracao = StatusConfiguracao.CONFIGURADO
        i1.ip = "10.0.0.1"
        i1.save(update_fields=["status_configuracao", "ip"])

        i2 = self._mk_item(chamado=ch, tem_ativo=False, deve_configurar=True)
        i2.status_configuracao = StatusConfiguracao.CONFIGURADO
        i2.ip = ""  # sem ip -> não conta
        i2.save(update_fields=["status_configuracao", "ip"])

        rows = build_fila_rows([ch])

        assert rows[0]["cfg_total"] == 2
        assert rows[0]["cfg_done"] == 1
