import csv
import hashlib
from dataclasses import dataclass
from io import StringIO

from app.ingestion.amazon_reports.payment_transactions import decode_csv, detect_delimiter


@dataclass(frozen=True)
class GenericReportPreview:
    filename: str
    report_type: str
    encoding: str
    delimiter: str
    headers: list[str]
    row_count: int
    raw_rows: list[dict[str, str]]
    sample_rows: list[dict[str, str]]


def build_generic_report_preview(
    filename: str,
    content: bytes,
    report_type: str,
    sample_size: int = 10,
) -> GenericReportPreview:
    text, encoding = decode_csv(content)
    delimiter = detect_delimiter(text)
    reader = csv.DictReader(StringIO(text), delimiter=delimiter)
    rows = list(reader)
    return GenericReportPreview(
        filename=filename,
        report_type=report_type,
        encoding=encoding,
        delimiter=delimiter,
        headers=list(reader.fieldnames or []),
        row_count=len(rows),
        raw_rows=rows,
        sample_rows=rows[:sample_size],
    )


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
