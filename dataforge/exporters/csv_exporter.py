"""
CSV exporter for DataForge.
"""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Any


def export_csv(
    records: list[dict[str, Any]],
    output_path: Path,
) -> Path:
    """Write records to a CSV file with headers.

    Args:
        records: List of record dicts (all dicts must share the same keys).
        output_path: Destination file path.

    Returns:
        The resolved output path.
    """
    if not records:
        raise ValueError("No records to export.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(records[0].keys())

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return output_path
