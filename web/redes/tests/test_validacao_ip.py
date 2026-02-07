import pytest

from web.redes.services.validacao import (
    REASON_PREFIX_MISMATCH,
    REASON_TC_LEGACY_OK,
    REASON_TC_LEGACY_REJECT_134,
    REASON_TC_SEGMENTADO_OK,
    REASON_TC_SEGMENTADO_REJECT_11,
    REASON_TYPO_WARNING,
    Severity,
    classificar_ip,
    validar_ip_para_tipo,
)

# Perfis fake (sem Django / sem DB)
PERFIL_LEGADO = {"tipo": "LEGACY_FLAT"}
PERFIL_SEGMENTADO = {"tipo": "SEGMENTADO"}

BASE_IP = "10.20.30.1"


# -------------------------------------------------------------------
# LEGADO — TC
# -------------------------------------------------------------------


@pytest.mark.parametrize(
    "ip",
    [
        "10.20.30.11",
        "10.20.30.13",
        "10.20.30.14",
        "10.20.30.15",
    ],
)
def test_legado_tc_aceita_ips_validos(ip):
    result = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, ip, "TC")

    assert result.is_valid is True
    assert result.severity == Severity.INFO
    assert result.reason == REASON_TC_LEGACY_OK


def test_legado_tc_rejeita_134():
    result = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, "10.20.30.134", "TC")

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_LEGACY_REJECT_134


# -------------------------------------------------------------------
# SEGMENTADO — TC
# -------------------------------------------------------------------


@pytest.mark.parametrize(
    "ip",
    [
        "10.20.30.134",
        "10.20.30.135",
        "10.20.30.200",
    ],
)
def test_segmentado_tc_aceita_134_ou_maior(ip):
    result = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, ip, "TC")

    assert result.is_valid is True
    assert result.severity == Severity.INFO
    assert result.reason == REASON_TC_SEGMENTADO_OK


def test_segmentado_tc_rejeita_11():
    result = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, "10.20.30.11", "TC")

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_SEGMENTADO_REJECT_11


# -------------------------------------------------------------------
# REGRA GLOBAL — prefixo da loja
# -------------------------------------------------------------------


def test_prefixo_divergente_retorna_erro_nao_pertence_a_loja():
    result = validar_ip_para_tipo(
        PERFIL_LEGADO,
        BASE_IP,
        "10.20.99.11",
        "TC",
    )

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_PREFIX_MISMATCH


# -------------------------------------------------------------------
# TYPO WARNING
# -------------------------------------------------------------------


def test_typo_warning_111_quando_esperado_11():
    result = validar_ip_para_tipo(
        PERFIL_LEGADO,
        BASE_IP,
        "10.20.30.111",
        "TC",
    )

    assert result.is_valid is True
    assert result.severity == Severity.WARN
    assert result.reason == REASON_TYPO_WARNING
    assert result.suggestion is not None


# -------------------------------------------------------------------
# CLASSIFICAÇÃO (contrato mínimo)
# -------------------------------------------------------------------


def test_classificar_ip_reconhece_tc_legado():
    result = classificar_ip(
        PERFIL_LEGADO,
        BASE_IP,
        "10.20.30.11",
    )

    assert result.probable_tipo == "TC"
    assert result.severity == Severity.INFO


def test_classificar_ip_warning_ainda_classifica_tc():
    result = classificar_ip(
        PERFIL_LEGADO,
        BASE_IP,
        "10.20.30.111",
    )

    assert result.probable_tipo == "TC"
    assert result.severity == Severity.WARN
