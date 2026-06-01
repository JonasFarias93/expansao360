# web/chamados/tests/test_models_chamado_avulso.py
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from chamados.models import Chamado
from chamados.tests._base import WebAuthBaseTestCase


class TestChamadoAvulso(WebAuthBaseTestCase):

    def test_chamado_avulso_sem_projeto_kit_subprojeto(self):
        chamado = Chamado.objects.create(
            loja=self.loja,
            projeto=None,
            subprojeto=None,
            kit=None,
            is_avulso=True,
            status=Chamado.Status.EM_ABERTURA,
        )
        self.assertTrue(chamado.is_avulso)
        self.assertIsNone(chamado.projeto)
        self.assertIsNone(chamado.kit)

    def test_chamado_projeto_exige_kit_e_subprojeto(self):
        chamado = Chamado(
            loja=self.loja,
            projeto=self.projeto,
            subprojeto=None,
            kit=None,
            is_avulso=False,
            status=Chamado.Status.EM_ABERTURA,
        )
        with self.assertRaises(ValidationError):
            chamado.full_clean()