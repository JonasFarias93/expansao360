from __future__ import annotations

import os

import pytest
from django.conf import settings
from django.db import connection


def _looks_like_postgres_engine(engine: str) -> bool:
    engine = (engine or "").lower()
    return "postgres" in engine or "psycopg" in engine


def test_ci_requires_postgres_db_engine() -> None:
    """
    Gate de CI: no GitHub Actions, o banco TEM que ser Postgres (por config).
    Evita regressão silenciosa onde o CI volta a usar SQLite por fallback.
    """
    if os.getenv("GITHUB_ACTIONS") != "true":
        return

    engine = settings.DATABASES["default"]["ENGINE"]
    assert _looks_like_postgres_engine(engine), (
        f"CI deve usar Postgres. ENGINE atual: {engine!r}"
    )


@pytest.mark.django_db
def test_ci_requires_postgres_vendor() -> None:
    """
    Gate de CI: valida o vendor real da conexão (garante que conectou em Postgres).
    """
    if os.getenv("GITHUB_ACTIONS") != "true":
        return

    assert connection.vendor == "postgresql", (
        f"CI deve conectar em Postgres. vendor atual: {connection.vendor!r}"
    )
