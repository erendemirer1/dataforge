"""
JSON exporter for DataForge.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def export_json(
    records: list[dict[str, Any]],
    output_path: Path,
    compact: bool = False,
) -> Path:
    """Write records to a JSON file.

    Args:
        records: List of record dicts.
        output_path: Destination file path.
        compact: If True, write compact (no indentation). Default: pretty.

    Returns:
        The resolved output path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        if compact:
            json.dump(records, f, ensure_ascii=False, separators=(',', ':'))
        else:
            json.dump(records, f, ensure_ascii=False, indent=2)

    return output_path
