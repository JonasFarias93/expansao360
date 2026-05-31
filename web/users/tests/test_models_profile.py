# web/users/tests/test_models_profile.py
from __future__ import annotations

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from users.models import UserProfile

User = get_user_model()


class TestUserProfile(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tecnico1", password="senha123")

    def test_perfil_criado_manualmente(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.status, UserProfile.Status.ATIVO)
        self.assertEqual(profile.perfil, UserProfile.Perfil.TECNICO)

    def test_is_operacional_ativo(self):
        profile = UserProfile.objects.create(user=self.user, status=UserProfile.Status.ATIVO)
        self.assertTrue(profile.is_operacional)

    def test_is_operacional_bloqueado(self):
        profile = UserProfile.objects.create(user=self.user, status=UserProfile.Status.BLOQUEADO)
        self.assertFalse(profile.is_operacional)

    def test_is_operacional_afastado(self):
        profile = UserProfile.objects.create(user=self.user, status=UserProfile.Status.AFASTADO)
        self.assertFalse(profile.is_operacional)


class TestOperationalAuthBackend(TestCase):

    def test_usuario_sem_perfil_autentica(self):
        User.objects.create_user(username="semperfil", password="senha123")
        user = authenticate(username="semperfil", password="senha123")
        self.assertIsNotNone(user)

    def test_usuario_ativo_autentica(self):
        user = User.objects.create_user(username="ativo", password="senha123")
        UserProfile.objects.create(user=user, status=UserProfile.Status.ATIVO)
        result = authenticate(username="ativo", password="senha123")
        self.assertIsNotNone(result)

    def test_usuario_bloqueado_nao_autentica(self):
        user = User.objects.create_user(username="bloqueado", password="senha123")
        UserProfile.objects.create(user=user, status=UserProfile.Status.BLOQUEADO)
        result = authenticate(username="bloqueado", password="senha123")
        self.assertIsNone(result)

    def test_usuario_desligado_nao_autentica(self):
        user = User.objects.create_user(username="desligado", password="senha123")
        UserProfile.objects.create(user=user, status=UserProfile.Status.DESLIGADO)
        result = authenticate(username="desligado", password="senha123")
        self.assertIsNone(result)

    def test_senha_errada_nao_autentica(self):
        User.objects.create_user(username="qualquer", password="correta")
        result = authenticate(username="qualquer", password="errada")
        self.assertIsNone(result)
