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


# Reasons padronizados (curtos e testáveis)
REASON_INVALID_IP_FORMAT = "INVALID_IP_FORMAT"
REASON_PREFIX_MISMATCH = "PREFIX_MISMATCH"  # "não pertence à loja"
REASON_NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

REASON_TC_LEGACY_OK = "TC_LEGACY_OK"
REASON_TC_LEGACY_REJECT_134 = "TC_LEGACY_REJECT_134"
REASON_TC_LEGACY_REJECT = "TC_LEGACY_REJECT"

REASON_TC_SEGMENTADO_OK = "TC_SEGMENTADO_OK"
REASON_TC_SEGMENTADO_REJECT_11 = "TC_SEGMENTADO_REJECT_11"
REASON_TC_SEGMENTADO_REJECT = "TC_SEGMENTADO_REJECT"

REASON_TYPO_WARNING = "TYPO_WARNING"


def classificar_ip(perfil: Any, base_ip: str, ip: str) -> ClassificationResult:
    """
    classificar_ip(perfil, base_ip, ip) -> retorna tipo provável + severidade (ok/warn/erro)
    MVP: só classifica "TC" (demais tipos ficam como desconhecido por enquanto).
    """
    # 1) valida formato e prefixo (regra global)
    prefix_check = _validate_prefix(base_ip, ip)
    if prefix_check is not None:
        # erro de formato/prefixo: não tem como classificar corretamente
        return ClassificationResult(
            probable_tipo=None,
            severity=prefix_check.severity,
            reason=prefix_check.reason,
            suggestion=prefix_check.suggestion,
        )

    # 2) tenta classificar como TC (única regra MVP)
    tc = validar_ip_para_tipo(perfil, base_ip, ip, "TC")
    if tc.severity == Severity.WARN and tc.reason == REASON_TYPO_WARNING:
        # warning de typo, mas ainda “provável TC”
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

    # 3) sem match
    return ClassificationResult(
        probable_tipo=None,
        severity=Severity.WARN,
        reason=REASON_NOT_IMPLEMENTED,
        suggestion="Tipo não identificado no MVP (apenas TC está coberto).",
    )


def validar_ip_para_tipo(perfil: Any, base_ip: str, ip: str, tipo: str) -> ValidationResult:
    """
    validar_ip_para_tipo(perfil, base_ip, ip, tipo) -> ok/erro + motivo
    MVP: tipo é o codigo da regra (ex: "TC")
    """
    # 1) valida formato e prefixo (regra global)
    prefix_check = _validate_prefix(base_ip, ip)
    if prefix_check is not None:
        return prefix_check

    # 2) MVP: apenas TC
    tipo_norm = (tipo or "").strip().upper()
    if tipo_norm != "TC":
        return ValidationResult(
            is_valid=False,
            reason=REASON_NOT_IMPLEMENTED,
            severity=Severity.WARN,
            suggestion="MVP valida apenas tipo 'TC'.",
        )

    # 3) aplica regra por perfil (LEGACY vs SEGMENTADO)
    perfil_tipo = _get_perfil_tipo(perfil)

    last_octet = _last_octet(ip)

    # Typo warning (exigência): .111 quando esperado .11 -> WARN (não bloqueia)
    # MVP: só dispara esse warning quando o perfil/tipo teria como caso comum o .11
    if last_octet == 111 and _tc_expects_11(perfil_tipo):
        return ValidationResult(
            is_valid=True,
            reason=REASON_TYPO_WARNING,
            severity=Severity.WARN,
            suggestion=_suggest_fix_last_octet(ip, 11),
        )

    if perfil_tipo == "LEGACY_FLAT":
        # Legado: TC aceita .11/.13/.14/.15 e rejeita .134
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
        # Segmentado: TC aceita .134+ e rejeita .11
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

    # Perfil desconhecido => falha explícita e testável
    return ValidationResult(
        is_valid=False,
        reason=REASON_NOT_IMPLEMENTED,
        severity=Severity.ERROR,
        suggestion="Tipo de perfil desconhecido (esperado LEGACY_FLAT ou SEGMENTADO).",
    )


# -----------------------
# Helpers (privados)
# -----------------------


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
    # considera /24: compara 3 primeiros octetos
    s = str(ip).split(".")
    return int(s[0]), int(s[1]), int(s[2])


def _last_octet(ip: str) -> int:
    return int(str(ip).split(".")[-1])


def _get_perfil_tipo(perfil: Any) -> str:
    """
    Aceita:
    - objeto com atributo .tipo (ex: PerfilRede Django)
    - dict {"tipo": "..."}
    - string direta "LEGACY_FLAT"/"SEGMENTADO"
    """
    if perfil is None:
        return ""

    if isinstance(perfil, str):
        return perfil.strip().upper()

    if isinstance(perfil, dict) and "tipo" in perfil:
        return str(perfil["tipo"]).strip().upper()

    tipo = getattr(perfil, "tipo", "")
    return str(tipo).strip().upper()


def _tc_expects_11(perfil_tipo: str) -> bool:
    # MVP: no legado, .11 é esperado; no segmentado, é explicitamente rejeitado
    return perfil_tipo == "LEGACY_FLAT"


def _suggest_fix_last_octet(ip: str, expected_last: int) -> str:
    parts = str(ip).split(".")
    if len(parts) != 4:
        return "Verifique o IP informado."
    parts[-1] = str(expected_last)
    return f"Você quis dizer {'.'.join(parts)}?"
