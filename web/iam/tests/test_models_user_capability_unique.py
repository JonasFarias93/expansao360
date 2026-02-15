from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from iam.models import Capability, UserCapability


class TestUserCapabilityUniqueness(TestCase):
    def test_quando_mesmo_user_e_capability_entao_viola_unicidade(self):
        User = get_user_model()
        user = User.objects.create_user(username="u1", password="x")

        cap = Capability.objects.create(code="execucao.chamado.finalizar")

        UserCapability.objects.create(user=user, capability=cap)

        # Garante que o IntegrityError seja capturado de forma determinística
        # (sem depender do comportamento de commit implícito).
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserCapability.objects.create(user=user, capability=cap)
