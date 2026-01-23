from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from .models import Capability, UserCapability


class IamModelsTest(TestCase):
    def test_user_capability_is_unique(self):
        User = get_user_model()
        user = User.objects.create_user(username="u1", password="x")

        cap = Capability.objects.create(code="execucao.chamado.finalizar")

        UserCapability.objects.create(user=user, capability=cap)

        with self.assertRaises(IntegrityError):
            UserCapability.objects.create(user=user, capability=cap)
