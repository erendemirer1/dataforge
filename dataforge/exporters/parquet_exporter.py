"""
Parquet exporter for DataForge.
Requires: pandas, pyarrow
"""
from __future__ import annotations
from pathlib import Path
from typing import Any


def export_parquet(
    records: list[dict[str, Any]],
    output_path: Path,
) -> Path:
    """Write records to a Parquet file using pandas + pyarrow.

    Args:
        records: List of record dicts.
        output_path: Destination .parquet file path.

    Returns:
        The resolved output path.
    """
    try:
        import pandas as pd  # noqa: PLC0415
    except ImportError as exc:
        raise ImportError(
            "pandas is required for Parquet export. "
            "Install with: pip install pandas pyarrow"
        ) from exc

    if not records:
        raise ValueError("No records to export.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(records)
    df.to_parquet(output_path, index=False, engine='pyarrow')

    return output_path
