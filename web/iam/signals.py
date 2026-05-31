# web/iam/signals.py
from __future__ import annotations

from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from iam.models import Capability, GroupCapability, UserCapability


@receiver(m2m_changed, sender=User.groups.through)
def sync_capabilities_from_group(sender, instance, action, pk_set, **kwargs):
    """
    Ao adicionar usuário a um grupo → concede capabilities do grupo.
    Ao remover usuário de um grupo → remove capabilities exclusivas do grupo.
    """
    if action == "post_add":
        for group_id in (pk_set or []):
            for gc in GroupCapability.objects.filter(group_id=group_id).select_related("capability"):
                UserCapability.objects.get_or_create(
                    user=instance,
                    capability=gc.capability,
                )

    elif action == "post_remove":
        for group_id in (pk_set or []):
            for gc in GroupCapability.objects.filter(group_id=group_id).select_related("capability"):
                # só remove se não estiver em outro grupo do usuário
                outros_grupos = instance.groups.exclude(pk=group_id)
                em_outro_grupo = GroupCapability.objects.filter(
                    group__in=outros_grupos,
                    capability=gc.capability,
                ).exists()
                if not em_outro_grupo:
                    UserCapability.objects.filter(
                        user=instance,
                        capability=gc.capability,
                    ).delete()