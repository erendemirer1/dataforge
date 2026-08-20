"""
DataForge Household & Family Structure Engine.
Demographically conditioned on TÜİK 2024/2025 marital, fertility, and housing statistics.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class HouseholdProfile:
    marital_status: str
    children_count: int
    household_size: int
    housing_status: str


class HouseholdEngine:
    """Simulates realistic Turkish household, marital status, and family structure."""

    _instance: Optional["HouseholdEngine"] = None

    @classmethod
    def get_instance(cls) -> "HouseholdEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_household(
        self,
        age: int,
        income_segment: str = "orta_gelir",
        region: str = "TR1",
        rng: Optional[random.Random] = None,
    ) -> HouseholdProfile:
        """Generate statistically grounded household structure."""
        if rng is None:
            rng = random.Random()

        # 1. Marital Status (TÜİK age-conditioned marriage probability)
        if age < 23:
            marital = rng.choices(["Bekar", "Evli"], weights=[0.94, 0.06])[0]
        elif age < 30:
            marital = rng.choices(["Bekar", "Evli", "Boşanmış"], weights=[0.48, 0.50, 0.02])[0]
        elif age < 45:
            marital = rng.choices(["Evli", "Bekar", "Boşanmış"], weights=[0.76, 0.16, 0.08])[0]
        elif age < 65:
            marital = rng.choices(["Evli", "Boşanmış", "Dul", "Bekar"], weights=[0.80, 0.10, 0.06, 0.04])[0]
        else:
            marital = rng.choices(["Evli", "Dul", "Boşanmış", "Bekar"], weights=[0.64, 0.28, 0.05, 0.03])[0]

        # 2. Children Count (TÜİK regional fertility rate: higher in TRC/TRA, lower in TR1/TR3)
        if marital in ["Evli", "Boşanmış", "Dul"] and age >= 23:
            if region in ["TRC", "TRA", "TRB"]:  # Güneydoğu & Doğu Anadolu
                children = rng.choices([1, 2, 3, 4], weights=[0.15, 0.35, 0.35, 0.15])[0]
            elif region in ["TR1", "TR3", "TR2"]:  # İstanbul, Ege, Marmara
                children = rng.choices([0, 1, 2, 3], weights=[0.25, 0.45, 0.26, 0.04])[0]
            else:
                children = rng.choices([0, 1, 2, 3], weights=[0.15, 0.40, 0.35, 0.10])[0]
        else:
            children = 0

        # 3. Household Size
        if marital == "Bekar":
            household_size = 1 if (age >= 24 and income_segment in ["orta_gelir", "orta_ust", "ust_gelir"] and rng.random() > 0.4) else rng.randint(2, 4)
        elif marital == "Evli":
            household_size = 2 + children
        else:  # Boşanmış / Dul
            household_size = 1 + children

        # 4. Housing Status (TÜİK: 56% Ev Sahibi, 28% Kiracı, 16% Aile Evi)
        if age < 25:
            housing = rng.choices(["Aile Evi", "Kiracı", "Ev Sahibi"], weights=[0.70, 0.25, 0.05])[0]
        elif income_segment in ["ust_gelir", "orta_ust"]:
            housing = rng.choices(["Ev Sahibi", "Kiracı"], weights=[0.82, 0.18])[0]
        elif income_segment in ["alt_gelir", "orta_alt"]:
            housing = rng.choices(["Kiracı", "Ev Sahibi", "Aile Evi"], weights=[0.55, 0.30, 0.15])[0]
        else:
            housing = rng.choices(["Ev Sahibi", "Kiracı"], weights=[0.58, 0.42])[0]

        return HouseholdProfile(
            marital_status=marital,
            children_count=children,
            household_size=household_size,
            housing_status=housing,
        )
