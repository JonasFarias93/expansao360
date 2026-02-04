# conftest.py (raiz)
import pytest


@pytest.fixture(autouse=True)
def media_root_tmp(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
