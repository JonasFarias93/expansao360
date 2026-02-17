from __future__ import annotations

from django.apps import apps

from chamados.models import Chamado, InstalacaoItem
from chamados.services.itens_update import atualizar_itens

from ._base import ChamadoBaseTestCase


def _get_model(app_label: str, *names: str):
    for n in names:
        try:
            return apps.get_model(app_label, n)
        except LookupError:
            continue
    raise LookupError(f"Não achei model {app_label}.{names!r}")


class TestServiceAtualizarItens(ChamadoBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._eq_seq = 0

    def _mk_chamado(self, *, status: str, protocolo: str) -> Chamado:
        return Chamado.objects.create(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=self.sub,
            kit=self.kit,
            tipo=Chamado.Tipo.ENVIO,
            status=status,
            protocolo=protocolo,
        )

    def _mk_equipamento(self, *, tem_ativo: bool, configuravel: bool = True):
        Equipamento = _get_model("cadastro", "Equipamento")
        self._eq_seq += 1
        return Equipamento.objects.create(
            codigo=f"EQ-T7-{self._eq_seq}",
            nome=f"Equipamento T7 {self._eq_seq}",
            categoria=self.categoria,
            tem_ativo=tem_ativo,
            configuravel=configuravel,
        )

    def _mk_item(
        self,
        *,
        chamado: Chamado,
        tem_ativo: bool,
        configuravel: bool = True,
        deve_configurar: bool = False,
    ) -> InstalacaoItem:
        eq = self._mk_equipamento(tem_ativo=tem_ativo, configuravel=configuravel)
        return InstalacaoItem.objects.create(
            chamado=chamado,
            equipamento=eq,
            quantidade=1,
            tem_ativo=tem_ativo,
            deve_configurar=deve_configurar,
        )

    def test_dado_em_abertura_quando_deve_configurar_true_sem_ip_entao_rejeita_e_redireciona_setup(
        self,
    ) -> None:
        ch = self._mk_chamado(status=Chamado.Status.EM_ABERTURA, protocolo="T7-1")
        item = self._mk_item(chamado=ch, tem_ativo=False, configuravel=True)

        post = {f"deve_configurar_{item.id}": "on", f"ip_{item.id}": ""}

        result = atualizar_itens(chamado=ch, post_data=post)

        ch.refresh_from_db()
        assert ch.status == Chamado.Status.EM_ABERTURA
        assert result.redirect_name == "execucao:chamado_setup"
        assert result.redirect_kwargs["chamado_id"] == ch.id
        assert any(m.level == "error" for m in result.messages)

    def test_dado_em_abertura_quando_ok_entao_promove_para_aberto_e_redireciona_fila(
        self,
    ) -> None:
        ch = self._mk_chamado(status=Chamado.Status.EM_ABERTURA, protocolo="T7-2")
        item = self._mk_item(chamado=ch, tem_ativo=False, configuravel=True)

        post = {f"deve_configurar_{item.id}": "on", f"ip_{item.id}": "10.0.0.1"}

        result = atualizar_itens(chamado=ch, post_data=post)

        ch.refresh_from_db()
        item.refresh_from_db()
        assert ch.status == Chamado.Status.ABERTO
        assert item.deve_configurar is True
        assert item.ip == "10.0.0.1"
        assert result.redirect_name == "execucao:fila"
        assert any(m.level == "success" for m in result.messages)

    def test_dado_aberto_quando_operacional_entao_atualiza_e_promove_para_em_execucao(
        self,
    ) -> None:
        ch = self._mk_chamado(status=Chamado.Status.ABERTO, protocolo="T7-3")

        rastreavel = self._mk_item(chamado=ch, tem_ativo=True, configuravel=True)
        contavel = self._mk_item(chamado=ch, tem_ativo=False, configuravel=True)

        post = {
            f"ativo_{rastreavel.id}": "ATV",
            f"serie_{rastreavel.id}": "SER",
            f"confirmado_{contavel.id}": "on",
        }

        result = atualizar_itens(chamado=ch, post_data=post)

        ch.refresh_from_db()
        assert ch.status == Chamado.Status.EM_EXECUCAO
        assert result.redirect_name == "execucao:chamado_detalhe"
        assert result.redirect_kwargs["chamado_id"] == ch.id

        rastreavel.refresh_from_db()
        contavel.refresh_from_db()
        assert rastreavel.ativo == "ATV"
        assert rastreavel.numero_serie == "SER"
        assert contavel.confirmado is True

    def test_dado_equipamento_nao_configuravel_quando_marca_deve_configurar_entao_forca_false_e_limpa_ip(
        self,
    ) -> None:
        ch = self._mk_chamado(status=Chamado.Status.EM_ABERTURA, protocolo="T7-4")

        item = self._mk_item(chamado=ch, tem_ativo=False, configuravel=False)

        post = {f"deve_configurar_{item.id}": "on", f"ip_{item.id}": "10.0.0.9"}

        result = atualizar_itens(chamado=ch, post_data=post)

        item.refresh_from_db()
        assert item.deve_configurar is False
        assert item.ip is None

        ch.refresh_from_db()
        assert ch.status == Chamado.Status.ABERTO
        assert result.redirect_name == "execucao:fila"
