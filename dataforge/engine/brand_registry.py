"""
DataForge Brand and Merchant Registry.
Loads and indexes structured real Turkish retail brands and merchants from brands.json.
Provides demographic, income-tier, and geographic coverage filtering.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Optional

BRANDS_FILE = Path(__file__).parent.parent / "data" / "brands.json"


class BrandRegistry:
    """Manages the index of authentic Turkish enterprise and retail brands."""

    _instance: Optional["BrandRegistry"] = None

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or BRANDS_FILE
        self._brands: list[dict[str, Any]] = []
        self._by_category: dict[str, list[dict[str, Any]]] = {}
        self._load()

    @classmethod
    def get_instance(cls) -> "BrandRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load(self) -> None:
        if not self.file_path.exists():
            return
        with open(self.file_path, "r", encoding="utf-8") as f:
            self._brands = json.load(f)

        self._by_category = {}
        for b in self._brands:
            cat = b.get("category", "other")
            if cat not in self._by_category:
                self._by_category[cat] = []
            self._by_category[cat].append(b)

    def get_merchants(
        self,
        category: str,
        income_segment: str = "orta_gelir",
        is_metro: bool = True,
    ) -> list[str]:
        """Return matching brand names filtered by category, income tier, and city tier."""
        pool = self._by_category.get(category, self._brands)

        # 1. Map income_segment to target tiers
        if income_segment in ["alt_gelir", "orta_alt"]:
            target_tiers = {"budget", "mid"}
        elif income_segment == "orta_gelir":
            target_tiers = {"budget", "mid", "premium"}
        else:  # orta_ust, ust_gelir
            target_tiers = {"mid", "premium"}

        # 2. Filter by tier and coverage
        filtered = []
        for b in pool:
            if b.get("tier") in target_tiers:
                if not is_metro and b.get("coverage") == "metro_only":
                    continue
                filtered.append(b.get("name"))

        if not filtered:
            # Fallback to any brand in category without metro restriction if pool empty
            filtered = [b.get("name") for b in pool if is_metro or b.get("coverage") != "metro_only"]

        return filtered if filtered else ["Yerel İşletme"]

    def select_merchant(
        self,
        rng: Optional[random.Random],
        category: str,
        income_segment: str = "orta_gelir",
        is_metro: bool = True,
    ) -> str:
        """Select a single coherent merchant using pseudo-random generator."""
        if rng is None:
            rng = random.Random()

        candidates = self.get_merchants(category, income_segment, is_metro)
        return rng.choice(candidates)
