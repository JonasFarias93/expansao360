from __future__ import annotations

from cadastro.models import Categoria, Kit, Loja, Projeto, Subprojeto
from django.contrib.auth import get_user_model
from django.test import TestCase
from iam.models import Capability, UserCapability


def grant_cap(user, code: str) -> None:
    cap, _ = Capability.objects.get_or_create(code=code)
    UserCapability.objects.get_or_create(user=user, capability=cap)


class ChamadoBaseTestCase(TestCase):
    """Setup comum para cenários de execução."""

    def setUp(self) -> None:
        self.categoria = Categoria.objects.create(nome="Infra")
        self.loja = Loja.objects.create(codigo="L1", nome="Loja 1")
        self.projeto = Projeto.objects.create(codigo="P1", nome="Projeto 1")
        self.sub = Subprojeto.objects.create(
            projeto=self.projeto,
            codigo="S1",
            nome="Sub 1",
        )
        self.kit = Kit.objects.create(nome="Kit PDV")


class WebAuthBaseTestCase(ChamadoBaseTestCase):
    """Base para testes web (client autenticado + capabilities)."""

    def setUp(self) -> None:
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="x")
        self.client.force_login(self.user)

        # Capabilities necessárias para os endpoints que são POST e sensíveis.
        grant_cap(self.user, "execucao.chamado.editar_itens")
        grant_cap(self.user, "execucao.evidencia.upload")
        grant_cap(self.user, "execucao.evidencia.remover")
        grant_cap(self.user, "execucao.item_configuracao.alterar_status")
        grant_cap(self.user, "execucao.chamado.finalizar")
