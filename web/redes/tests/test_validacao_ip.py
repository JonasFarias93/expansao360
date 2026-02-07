import pytest

from web.redes.services.validacao import (
    REASON_PREFIX_MISMATCH,
    # --- RETAGUARDA_LOJA ---
    REASON_RETAGUARDA_LEGACY_OK,
    REASON_RETAGUARDA_LEGACY_REJECT,
    REASON_RETAGUARDA_SEGMENTADO_OK,
    REASON_RETAGUARDA_SEGMENTADO_REJECT,
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
# 1) Helpers / fixtures locais
# -------------------------------------------------------------------

# Perfis fake (sem Django / sem DB)
PERFIL_LEGADO = {"tipo": "LEGACY_FLAT"}
PERFIL_SEGMENTADO = {"tipo": "SEGMENTADO"}

# Base IP exemplo por perfil (prefixo da loja)
BASE_IP = "10.20.30.1"


def ip_offset(base_ip: str, offset: int) -> str:
    """
    Monta um IP dentro do mesmo /24 do base_ip, trocando apenas o último octeto.
    Ex.: base_ip 10.20.30.1 + offset 11 => 10.20.30.11
    """
    a, b, c, _ = base_ip.split(".")
    return f"{a}.{b}.{c}.{offset}"


# -------------------------------------------------------------------
# 2) Global (já existe)
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
# 3) TC (já existe)
# -------------------------------------------------------------------
# LEGACY_FLAT — TC


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
    result = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, ip_offset(BASE_IP, 134), "TC")

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_LEGACY_REJECT_134


# SEGMENTADO — TC


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
    result = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, ip_offset(BASE_IP, 11), "TC")

    assert result.is_valid is False
    assert result.severity == Severity.ERROR
    assert result.reason == REASON_TC_SEGMENTADO_REJECT_11


# -------------------------------------------------------------------
# TYPO WARNING (já existe)
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
# 4) RETAGUARDA_LOJA (novo bloco)
# -------------------------------------------------------------------
# LEGACY_FLAT — RETAGUARDA
# Contrato mínimo:
# - Banco12 aceita .12; rejeita .13
# - Gerência aceita .30; rejeita .130
# - Farma aceita .60; rejeita .131
# - RH aceita .70; rejeita .129


@pytest.mark.parametrize(
    "tipo, ok_offset, reject_offset",
    [
        ("BANCO12", 12, 13),
        ("GERENCIA", 30, 130),
        ("FARMA", 60, 131),
        ("RH", 70, 129),
    ],
)
def test_legado_retaguarda_aceita_offset_fixo_e_rejeita_cruzado(tipo, ok_offset, reject_offset):
    ok = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, ip_offset(BASE_IP, ok_offset), tipo)
    assert ok.is_valid is True
    assert ok.severity == Severity.INFO
    assert ok.reason == REASON_RETAGUARDA_LEGACY_OK

    bad = validar_ip_para_tipo(PERFIL_LEGADO, BASE_IP, ip_offset(BASE_IP, reject_offset), tipo)
    assert bad.is_valid is False
    assert bad.severity == Severity.ERROR
    assert bad.reason == REASON_RETAGUARDA_LEGACY_REJECT


# SEGMENTADO — RETAGUARDA
# Contrato mínimo:
# - RH aceita .129; rejeita .70
# - Gerência aceita .130; rejeita .30
# - Farma aceita .131; rejeita .60
# - Banco12 aceita .12; rejeita .11 (colisão com TC/legado)


@pytest.mark.parametrize(
    "tipo, ok_offset, reject_offset",
    [
        ("RH", 129, 70),
        ("GERENCIA", 130, 30),
        ("FARMA", 131, 60),
        ("BANCO12", 12, 11),
    ],
)
def test_segmentado_retaguarda_aceita_offset_fixo_e_rejeita_cruzado(tipo, ok_offset, reject_offset):
    ok = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, ip_offset(BASE_IP, ok_offset), tipo)
    assert ok.is_valid is True
    assert ok.severity == Severity.INFO
    assert ok.reason == REASON_RETAGUARDA_SEGMENTADO_OK

    bad = validar_ip_para_tipo(PERFIL_SEGMENTADO, BASE_IP, ip_offset(BASE_IP, reject_offset), tipo)
    assert bad.is_valid is False
    assert bad.severity == Severity.ERROR
    assert bad.reason == REASON_RETAGUARDA_SEGMENTADO_REJECT


# -------------------------------------------------------------------
# CLASSIFICAÇÃO (contrato mínimo)
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
