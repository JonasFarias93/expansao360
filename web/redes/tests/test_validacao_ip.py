import pytest

from web.redes.services.validacao import (
    # --- CONSULTA_PRECO ---
    REASON_CONSULTA_PRECO_SEGMENTADO_OK,
    REASON_CONSULTA_PRECO_SEGMENTADO_REJECT,
    # --- IMPRESSORAS_ETH ---
    REASON_IMPRESSORAS_ETH_SEGMENTADO_OK,
    REASON_IMPRESSORAS_ETH_SEGMENTADO_REJECT,
    REASON_PREFIX_MISMATCH,
    # --- RETAGUARDA_LOJA ---
    REASON_TC_LEGACY_OK,
    REASON_TC_LEGACY_REJECT_134,
    REASON_TC_SEGMENTADO_OK,
    REASON_TC_SEGMENTADO_REJECT_11,
    REASON_TYPO_WARNING,
    Severity,
    classificar_ip,
    validar_ip_para_tipo,
)

# -------------------------------------------------------------------
# Helpers / fixtures
# -------------------------------------------------------------------

PERFIL_LEGADO = {"tipo": "LEGACY_FLAT"}
PERFIL_SEGMENTADO = {"tipo": "SEGMENTADO"}

BASE_IP = "10.20.30.1"


def ip_offset(base_ip: str, offset: int) -> str:
    a, b, c, _ = base_ip.split(".")
    return f"{a}.{b}.{c}.{offset}"


# -------------------------------------------------------------------
# PREFIXO
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
# TC
# -------------------------------------------------------------------


@pytest.mark.parametrize(
    "ip",
    [
        ip_offset(BASE_IP, 11),
        ip_offset(BASE_IP, 13),
        ip_offset(BASE_IP, 14),
        ip_offset(BASE_IP, 15),
    ],
)
def test_legado_tc_aceita_ips_validos(ip):
    result = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, ip, "TC")

    assert result.is_valid is True
    assert result.severity == Severity.INFO
    assert result.reason == REASON_TC_LEGACY_OK


def test_legado_tc_rejeita_134():
    result = validar_ip_para_tipo(
        PERFIL_LEGADO,
        BASE_IP,
        ip_offset(BASE_IP, 134),
        "TC",
    )

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_LEGACY_REJECT_134


@pytest.mark.parametrize(
    "ip",
    [
        ip_offset(BASE_IP, 134),
        ip_offset(BASE_IP, 135),
        ip_offset(BASE_IP, 200),
    ],
)
def test_segmentado_tc_aceita_134_ou_maior(ip):
    result = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, ip, "TC")

    assert result.is_valid is True
    assert result.severity == Severity.INFO
    assert result.reason == REASON_TC_SEGMENTADO_OK


def test_segmentado_tc_rejeita_11():
    result = validar_ip_para_tipo(
        PERFIL_SEGMENTADO,
        BASE_IP,
        ip_offset(BASE_IP, 11),
        "TC",
    )

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_SEGMENTADO_REJECT_11


# -------------------------------------------------------------------
# TYPO WARNING
# -------------------------------------------------------------------


def test_typo_warning_111_quando_esperado_11():
    result = validar_ip_para_tipo(
        PERFIL_LEGADO,
        BASE_IP,
        ip_offset(BASE_IP, 111),
        "TC",
    )

    assert result.is_valid is True
    assert result.severity == Severity.WARN
    assert result.reason == REASON_TYPO_WARNING
    assert result.suggestion is not None


# -------------------------------------------------------------------
# IMPRESSORAS_ETH — SEGMENTADO
# -------------------------------------------------------------------


@pytest.mark.parametrize("offset", [161, 162, 163])
def test_segmentado_impressoras_eth_aceita_offsets_validos(offset):
    ok = validar_ip_para_tipo(
        PERFIL_SEGMENTADO,
        BASE_IP,
        ip_offset(BASE_IP, offset),
        "IMPRESSORAS_ETH",
    )

    assert ok.is_valid is True
    assert ok.severity == Severity.INFO
    assert ok.reason == REASON_IMPRESSORAS_ETH_SEGMENTADO_OK


@pytest.mark.parametrize("offset", [193, 130, 1])
def test_segmentado_impressoras_eth_rejeita_offsets_cruzados(offset):
    bad = validar_ip_para_tipo(
        PERFIL_SEGMENTADO,
        BASE_IP,
        ip_offset(BASE_IP, offset),
        "IMPRESSORAS_ETH",
    )

    assert bad.is_valid is False
    assert bad.severity == Severity.ERROR
    assert bad.reason == REASON_IMPRESSORAS_ETH_SEGMENTADO_REJECT


# -------------------------------------------------------------------
# CONSULTA_PRECO — SEGMENTADO
# -------------------------------------------------------------------


@pytest.mark.parametrize("offset", [193, 194])
def test_segmentado_consulta_preco_aceita_offsets_validos(offset):
    ok = validar_ip_para_tipo(
        PERFIL_SEGMENTADO,
        BASE_IP,
        ip_offset(BASE_IP, offset),
        "CONSULTA_PRECO",
    )

    assert ok.is_valid is True
    assert ok.severity == Severity.INFO
    assert ok.reason == REASON_CONSULTA_PRECO_SEGMENTADO_OK


@pytest.mark.parametrize(
    "offset",
    [
        161,  # impressora
        134,  # TC
        12,  # banco12
    ],
)
def test_segmentado_consulta_preco_rejeita_offsets_cruzados(offset):
    bad = validar_ip_para_tipo(
        PERFIL_SEGMENTADO,
        BASE_IP,
        ip_offset(BASE_IP, offset),
        "CONSULTA_PRECO",
    )

    assert bad.is_valid is False
    assert bad.severity == Severity.ERROR
    assert bad.reason == REASON_CONSULTA_PRECO_SEGMENTADO_REJECT


# -------------------------------------------------------------------
# CLASSIFICAÇÃO
# -------------------------------------------------------------------


def test_classificar_ip_reconhece_tc_legado():
    result = classificar_ip(
        PERFIL_LEGADO,
        BASE_IP,
        ip_offset(BASE_IP, 11),
    )

    assert result.probable_tipo == "TC"
    assert result.severity == Severity.INFO


def test_classificar_ip_warning_ainda_classifica_tc():
    result = classificar_ip(
        PERFIL_LEGADO,
        BASE_IP,
        ip_offset(BASE_IP, 111),
    )

    assert result.probable_tipo == "TC"
    assert result.severity == Severity.WARN
