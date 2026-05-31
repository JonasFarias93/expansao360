# web/historico/apps.py
from django.apps import AppConfig


class HistoricoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "historico"

    def ready(self) -> None:
        import historico.signals  # noqa: F401