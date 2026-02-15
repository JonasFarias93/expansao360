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
# validar_ip_para_tipo — TC (LEGADO)
# -------------------------------------------------------------------


@pytest.mark.parametrize(
    "ip", ["10.20.30.11", "10.20.30.13", "10.20.30.14", "10.20.30.15"]
)
def test_dado_legado_tc_quando_ip_valido_entao_retorna_ok_info_reason_ok(ip):
    result = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, ip, "TC")

    assert result.is_valid is True
    assert result.severity == Severity.INFO
    assert result.reason == REASON_TC_LEGACY_OK


def test_dado_legado_tc_quando_ip_134_entao_rejeita_error_reason_134():
    result = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, "10.20.30.134", "TC")

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_LEGACY_REJECT_134


# -------------------------------------------------------------------
# validar_ip_para_tipo — TC (SEGMENTADO)
# -------------------------------------------------------------------


@pytest.mark.parametrize("ip", ["10.20.30.134", "10.20.30.135", "10.20.30.200"])
def test_dado_segmentado_tc_quando_ip_134_ou_maior_entao_ok(ip):
    result = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, ip, "TC")

    assert result.is_valid is True
    assert result.severity == Severity.INFO
    assert result.reason == REASON_TC_SEGMENTADO_OK


def test_dado_segmentado_tc_quando_ip_11_entao_rejeita_error_reason_11():
    result = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, "10.20.30.11", "TC")

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_SEGMENTADO_REJECT_11


# -------------------------------------------------------------------
# Regra global — prefixo da loja
# -------------------------------------------------------------------


def test_quando_prefixo_diverge_entao_rejeita_error_reason_prefix_mismatch():
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
# Typo warning — ainda válido, mas WARN
# -------------------------------------------------------------------


def test_dado_legado_tc_quando_ip_111_entao_warn_valido_com_suggestion():
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
# classificar_ip — contrato mínimo
# -------------------------------------------------------------------


def test_classificar_ip_quando_tc_legado_entao_probable_tipo_tc_info():
    result = classificar_ip(
        PERFIL_LEGADO,
        BASE_IP,
        "10.20.30.11",
    )

    assert result.probable_tipo == "TC"
    assert result.severity == Severity.INFO


def test_classificar_ip_quando_typo_warning_entao_probable_tipo_tc_warn():
    result = classificar_ip(
        PERFIL_LEGADO,
        BASE_IP,
        "10.20.30.111",
    )

    assert result.probable_tipo == "TC"
    assert result.severity == Severity.WARN
