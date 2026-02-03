from __future__ import annotations

import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from cadastro.services.import_lojas import importar_lojas

try:
    import openpyxl  # type: ignore
except Exception:  # pragma: no cover
    openpyxl = None  # type: ignore


EXPECTED_HEADERS = [
    "Filial",
    "Hist.",
    "Nome Filial",
    "Endereço",
    "Bairro",
    "Cidade",
    "UF",
    "Logomarca",
    "Telefone",
    "IP Banco 12",
]


def _normalize_headers(headers: list[str]) -> list[str]:
    return [h.strip() for h in headers]


def _read_csv(path: Path) -> list[dict[str, str]]:
    # tenta utf-8 e depois latin-1 (por causa de acentos)
    for enc in ("utf-8", "latin-1"):
        try:
            with path.open("r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f, delimiter=";")
                if not reader.fieldnames:
                    return []

                headers = _normalize_headers(list(reader.fieldnames))
                if headers != EXPECTED_HEADERS:
                    # não trava; só segue (podemos endurecer depois se quiser)
                    pass

                return [dict(r) for r in reader]
        except UnicodeDecodeError:
            continue

    raise CommandError("Não foi possível ler o CSV (tentado utf-8 e latin-1).")


def _read_xlsx(path: Path, sheet: str | None = None) -> list[dict[str, str]]:
    if openpyxl is None:
        raise CommandError("openpyxl não está instalado. Instale para importar XLSX.")

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.active

    rows_iter = ws.iter_rows(values_only=True)
    try:
        header_row = next(rows_iter)
    except StopIteration:
        return []

    headers = _normalize_headers([str(h or "").strip() for h in header_row])
    if headers[: len(EXPECTED_HEADERS)] != EXPECTED_HEADERS:
        # não trava; só segue (podemos endurecer depois se quiser)
        pass

    out: list[dict[str, str]] = []
    for values in rows_iter:
        row_dict: dict[str, str] = {}
        for i, h in enumerate(headers):
            if not h:
                continue
            v = values[i] if i < len(values) else ""
            row_dict[h] = "" if v is None else str(v)
        out.append(row_dict)

    return out


class Command(BaseCommand):
    help = "Importa lojas (CSV ';' ou Excel XLSX), criando/atualizando por codigo (Java)."

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="Caminho para arquivo .csv ou .xlsx")
        parser.add_argument("--sheet", type=str, default=None, help="Nome da aba (opcional, XLSX)")

    def handle(self, *args, **options):
        path = Path(options["path"])
        sheet = options["sheet"]

        if not path.exists():
            raise CommandError(f"Arquivo não encontrado: {path}")

        suffix = path.suffix.lower()
        if suffix == ".csv":
            rows = _read_csv(path)
        elif suffix in (".xlsx", ".xlsm"):
            rows = _read_xlsx(path, sheet=sheet)
        else:
            raise CommandError("Formato não suportado. Use .csv ou .xlsx.")

        self.stdout.write(f"Linhas lidas: {len(rows)}")

        result = importar_lojas(rows)

        self.stdout.write(self.style.SUCCESS("Import concluído:"))
        self.stdout.write(f"- Novas lojas: {result['created']}")
        self.stdout.write(f"- Lojas atualizadas: {result['updated']}")
        self.stdout.write(f"- Lojas sem alteração: {result['unchanged']}")
        self.stdout.write(f"- Linhas ignoradas: {result['skipped']}")
