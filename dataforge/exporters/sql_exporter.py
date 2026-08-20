"""
SQL INSERT exporter for DataForge.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any


def _sql_value(v: Any) -> str:
    """Convert a Python value to a SQL literal."""
    if v is None:
        return 'NULL'
    if isinstance(v, bool):
        return '1' if v else '0'
    if isinstance(v, (int, float)):
        return str(v)
    # Escape single quotes by doubling them
    escaped = str(v).replace("'", "''")
    return f"'{escaped}'"


def export_sql(
    records: list[dict[str, Any]],
    output_path: Path,
    table_name: str | None = None,
) -> Path:
    """Write records as SQL INSERT statements.

    Args:
        records: List of record dicts.
        output_path: Destination .sql file path.
        table_name: Override the table name; defaults to the file stem.

    Returns:
        The resolved output path.
    """
    if not records:
        raise ValueError("No records to export.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table = table_name or output_path.stem
    fieldnames = list(records[0].keys())
    columns = ', '.join(f"`{c}`" for c in fieldnames)

    lines = [
        f"-- DataForge SQL export",
        f"-- Table: {table}",
        f"-- Records: {len(records)}",
        f"",
    ]

    for record in records:
        values = ', '.join(_sql_value(record[k]) for k in fieldnames)
        lines.append(f"INSERT INTO `{table}` ({columns}) VALUES ({values});")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path
