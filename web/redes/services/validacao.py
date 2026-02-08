from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from ipaddress import AddressValueError, IPv4Address
from typing import Any


class Severity(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    reason: str
    severity: Severity
    suggestion: str | None = None


@dataclass(frozen=True)
class ClassificationResult:
    probable_tipo: str | None  # MVP: "tipo" == codigo da regra (ex: "TC")
    severity: Severity
    reason: str
    suggestion: str | None = None


# -------------------------------------------------------------------
# Reasons padronizados (curtos e testáveis)
# -------------------------------------------------------------------

REASON_INVALID_IP_FORMAT = "INVALID_IP_FORMAT"
REASON_PREFIX_MISMATCH = "PREFIX_MISMATCH"  # "não pertence à loja"
REASON_NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

# TC
REASON_TC_LEGACY_OK = "TC_LEGACY_OK"
REASON_TC_LEGACY_REJECT_134 = "TC_LEGACY_REJECT_134"
REASON_TC_LEGACY_REJECT = "TC_LEGACY_REJECT"

REASON_TC_SEGMENTADO_OK = "TC_SEGMENTADO_OK"
REASON_TC_SEGMENTADO_REJECT_11 = "TC_SEGMENTADO_REJECT_11"
REASON_TC_SEGMENTADO_REJECT = "TC_SEGMENTADO_REJECT"

# Typo warning
REASON_TYPO_WARNING = "TYPO_WARNING"

# RETAGUARDA_LOJA (MVP: offsets fixos por item e por perfil)
REASON_RETAGUARDA_LEGACY_OK = "RETAGUARDA_LEGACY_OK"
REASON_RETAGUARDA_LEGACY_REJECT = "RETAGUARDA_LEGACY_REJECT"
REASON_RETAGUARDA_SEGMENTADO_OK = "RETAGUARDA_SEGMENTADO_OK"
REASON_RETAGUARDA_SEGMENTADO_REJECT = "RETAGUARDA_SEGMENTADO_REJECT"

# IMPRESSORAS_ETH (RD_SEGMENTADO_2024/2025)
REASON_IMPRESSORAS_ETH_SEGMENTADO_OK = "IMPRESSORAS_ETH_SEGMENTADO_OK"
REASON_IMPRESSORAS_ETH_SEGMENTADO_REJECT = "IMPRESSORAS_ETH_SEGMENTADO_REJECT"

# CONSULTA_PRECO (RD_SEGMENTADO_2024/2025) — novo
REASON_CONSULTA_PRECO_SEGMENTADO_OK = "CONSULTA_PRECO_SEGMENTADO_OK"
REASON_CONSULTA_PRECO_SEGMENTADO_REJECT = "CONSULTA_PRECO_SEGMENTADO_REJECT"


# -------------------------------------------------------------------
# Catálogo MVP (sem DB): offsets por perfil e tipo
# -------------------------------------------------------------------

RETAGUARDA_OFFSETS_LEGACY: dict[str, int] = {
    "BANCO12": 12,
    "GERENCIA": 30,
    "FARMA": 60,
    "RH": 70,
}

RETAGUARDA_OFFSETS_SEGMENTADO: dict[str, int] = {
    "RH": 129,
    "GERENCIA": 130,
    "FARMA": 131,
    "BANCO12": 12,
}

IMPRESSORAS_ETH_OFFSETS_SEGMENTADO: set[int] = {161, 162, 163}

# Consulta preço: MVP só .193/.194 (.195 a confirmar)
CONSULTA_PRECO_OFFSETS_SEGMENTADO: set[int] = {193, 194}

# Aliases aceitos (mantém compatível com nomes mais “humanos”/docs)
TIPO_ALIASES: dict[str, str] = {
    "MICRO_GERENCIA": "GERENCIA",
    "MICRO_FARMA": "FARMA",
    "PORTAL_DO_SABER": "RH",
    "PORTAL_DO_SABER_RH": "RH",
}


def classificar_ip(perfil: Any, base_ip: str, ip: str) -> ClassificationResult:
    """
    MVP: só classifica "TC" (demais tipos ficam como desconhecido por enquanto).
    """
    prefix_check = _validate_prefix(base_ip, ip)
    if prefix_check is not None:
        return ClassificationResult(
            probable_tipo=None,
            severity=prefix_check.severity,
            reason=prefix_check.reason,
            suggestion=prefix_check.suggestion,
        )

    tc = validar_ip_para_tipo(perfil, base_ip, ip, "TC")
    if tc.severity == Severity.WARN and tc.reason == REASON_TYPO_WARNING:
        return ClassificationResult(
            probable_tipo="TC",
            severity=Severity.WARN,
            reason=REASON_TYPO_WARNING,
            suggestion=tc.suggestion,
        )

    if tc.is_valid:
        return ClassificationResult(
            probable_tipo="TC",
            severity=Severity.INFO,
            reason=tc.reason,
            suggestion=tc.suggestion,
        )

    return ClassificationResult(
        probable_tipo=None,
        severity=Severity.WARN,
        reason=REASON_NOT_IMPLEMENTED,
        suggestion="Tipo não identificado no MVP (apenas TC está coberto).",
    )


def validar_ip_para_tipo(perfil: Any, base_ip: str, ip: str, tipo: str) -> ValidationResult:
    """
    MVP:
    - TC
    - RETAGUARDA_LOJA: BANCO12, GERENCIA, FARMA, RH (com aliases)
    - IMPRESSORAS_ETH: offsets fixos no perfil SEGMENTADO (.161/.162/.163)
    - CONSULTA_PRECO: offsets fixos no perfil SEGMENTADO (.193/.194)
    """
    prefix_check = _validate_prefix(base_ip, ip)
    if prefix_check is not None:
        return prefix_check

    tipo_norm = _normalize_tipo(tipo)
    perfil_tipo = _get_perfil_tipo(perfil)
    last_octet = _last_octet(ip)

    # -----------------------
    # TC
    # -----------------------
    if tipo_norm == "TC":
        if last_octet == 111 and _tc_expects_11(perfil_tipo):
            return ValidationResult(
                is_valid=True,
                reason=REASON_TYPO_WARNING,
                severity=Severity.WARN,
                suggestion=_suggest_fix_last_octet(ip, 11),
            )

        if perfil_tipo == "LEGACY_FLAT":
            if last_octet == 134:
                return ValidationResult(
                    is_valid=False,
                    reason=REASON_TC_LEGACY_REJECT_134,
                    severity=Severity.ERROR,
                    suggestion="No legado, TC não pode usar .134.",
                )
            if last_octet in {11, 13, 14, 15}:
                return ValidationResult(
                    is_valid=True,
                    reason=REASON_TC_LEGACY_OK,
                    severity=Severity.INFO,
                )
            return ValidationResult(
                is_valid=False,
                reason=REASON_TC_LEGACY_REJECT,
                severity=Severity.ERROR,
                suggestion="No legado, TC aceita apenas finais .11/.13/.14/.15.",
            )

        if perfil_tipo == "SEGMENTADO":
            if last_octet == 11:
                return ValidationResult(
                    is_valid=False,
                    reason=REASON_TC_SEGMENTADO_REJECT_11,
                    severity=Severity.ERROR,
                    suggestion="No segmentado, TC não pode usar .11 (use .134+).",
                )
            if last_octet >= 134:
                return ValidationResult(
                    is_valid=True,
                    reason=REASON_TC_SEGMENTADO_OK,
                    severity=Severity.INFO,
                )
            return ValidationResult(
                is_valid=False,
                reason=REASON_TC_SEGMENTADO_REJECT,
                severity=Severity.ERROR,
                suggestion="No segmentado, TC deve ser .134 ou maior.",
            )

        return ValidationResult(
            is_valid=False,
            reason=REASON_NOT_IMPLEMENTED,
            severity=Severity.ERROR,
            suggestion="Tipo de perfil desconhecido (esperado LEGACY_FLAT ou SEGMENTADO).",
        )

    # -----------------------
    # RETAGUARDA_LOJA
    # -----------------------
    if tipo_norm in {"BANCO12", "GERENCIA", "FARMA", "RH"}:
        expected = _retaguarda_expected_offset(perfil_tipo, tipo_norm)
        if expected is None:
            return ValidationResult(
                is_valid=False,
                reason=REASON_NOT_IMPLEMENTED,
                severity=Severity.ERROR,
                suggestion="Tipo de perfil desconhecido (esperado LEGACY_FLAT ou SEGMENTADO).",
            )

        if last_octet == expected:
            return ValidationResult(
                is_valid=True,
                reason=(
                    REASON_RETAGUARDA_LEGACY_OK
                    if perfil_tipo == "LEGACY_FLAT"
                    else REASON_RETAGUARDA_SEGMENTADO_OK
                ),
                severity=Severity.INFO,
            )

        return ValidationResult(
            is_valid=False,
            reason=(
                REASON_RETAGUARDA_LEGACY_REJECT
                if perfil_tipo == "LEGACY_FLAT"
                else REASON_RETAGUARDA_SEGMENTADO_REJECT
            ),
            severity=Severity.ERROR,
            suggestion=_suggest_fix_last_octet(ip, expected),
        )

    # -----------------------
    # IMPRESSORAS_ETH (SEGMENTADO)
    # -----------------------
    if tipo_norm == "IMPRESSORAS_ETH":
        if perfil_tipo != "SEGMENTADO":
            return ValidationResult(
                is_valid=False,
                reason=REASON_NOT_IMPLEMENTED,
                severity=Severity.ERROR,
                suggestion="IMPRESSORAS_ETH é aplicável apenas ao perfil SEGMENTADO.",
            )

        if last_octet in IMPRESSORAS_ETH_OFFSETS_SEGMENTADO:
            return ValidationResult(
                is_valid=True,
                reason=REASON_IMPRESSORAS_ETH_SEGMENTADO_OK,
                severity=Severity.INFO,
            )

        expected_hint = min(IMPRESSORAS_ETH_OFFSETS_SEGMENTADO)
        return ValidationResult(
            is_valid=False,
            reason=REASON_IMPRESSORAS_ETH_SEGMENTADO_REJECT,
            severity=Severity.ERROR,
            suggestion=_suggest_fix_last_octet(ip, expected_hint),
        )

    # -----------------------
    # CONSULTA_PRECO (SEGMENTADO)
    # -----------------------
    if tipo_norm == "CONSULTA_PRECO":
        if perfil_tipo != "SEGMENTADO":
            return ValidationResult(
                is_valid=False,
                reason=REASON_NOT_IMPLEMENTED,
                severity=Severity.ERROR,
                suggestion="CONSULTA_PRECO é aplicável apenas ao perfil SEGMENTADO.",
            )

        if last_octet in CONSULTA_PRECO_OFFSETS_SEGMENTADO:
            return ValidationResult(
                is_valid=True,
                reason=REASON_CONSULTA_PRECO_SEGMENTADO_OK,
                severity=Severity.INFO,
            )

        expected_hint = min(CONSULTA_PRECO_OFFSETS_SEGMENTADO)
        return ValidationResult(
            is_valid=False,
            reason=REASON_CONSULTA_PRECO_SEGMENTADO_REJECT,
            severity=Severity.ERROR,
            suggestion=_suggest_fix_last_octet(ip, expected_hint),
        )

    return ValidationResult(
        is_valid=False,
        reason=REASON_NOT_IMPLEMENTED,
        severity=Severity.WARN,
        suggestion="MVP valida apenas tipo 'TC', "
        "itens de retaguarda, IMPRESSORAS_ETH e CONSULTA_PRECO.",
    )


# -------------------------------------------------------------------
# Helpers (privados)
# -------------------------------------------------------------------


def _normalize_tipo(tipo: str) -> str:
    norm = (tipo or "").strip().upper()
    return TIPO_ALIASES.get(norm, norm)


def _validate_prefix(base_ip: str, ip: str) -> ValidationResult | None:
    base = _parse_ipv4(base_ip)
    target = _parse_ipv4(ip)

    if base is None or target is None:
        return ValidationResult(
            is_valid=False,
            reason=REASON_INVALID_IP_FORMAT,
            severity=Severity.ERROR,
            suggestion="Use IPv4 no formato A.B.C.D (ex: 10.20.30.11).",
        )

    if _prefix_24(base) != _prefix_24(target):
        return ValidationResult(
            is_valid=False,
            reason=REASON_PREFIX_MISMATCH,
            severity=Severity.ERROR,
            suggestion="IP não pertence à loja (prefixo diferente do base_ip).",
        )

    return None


def _parse_ipv4(value: str) -> IPv4Address | None:
    try:
        return IPv4Address((value or "").strip())
    except AddressValueError:
        return None


def _prefix_24(ip: IPv4Address) -> tuple[int, int, int]:
    s = str(ip).split(".")
    return int(s[0]), int(s[1]), int(s[2])


def _last_octet(ip: str) -> int:
    return int(str(ip).split(".")[-1])


def _get_perfil_tipo(perfil: Any) -> str:
    if perfil is None:
        return ""

    if isinstance(perfil, str):
        return perfil.strip().upper()

    if isinstance(perfil, dict) and "tipo" in perfil:
        return str(perfil["tipo"]).strip().upper()

    tipo = getattr(perfil, "tipo", "")
    return str(tipo).strip().upper()


def _tc_expects_11(perfil_tipo: str) -> bool:
    return perfil_tipo == "LEGACY_FLAT"


def _retaguarda_expected_offset(perfil_tipo: str, tipo_norm: str) -> int | None:
    if perfil_tipo == "LEGACY_FLAT":
        return RETAGUARDA_OFFSETS_LEGACY.get(tipo_norm)

    if perfil_tipo == "SEGMENTADO":
        return RETAGUARDA_OFFSETS_SEGMENTADO.get(tipo_norm)

    return None


def _suggest_fix_last_octet(ip: str, expected_last: int) -> str:
    parts = str(ip).split(".")
    if len(parts) != 4:
        return "Verifique o IP informado."
    parts[-1] = str(expected_last)
    return f"Você quis dizer {'.'.join(parts)}?"
