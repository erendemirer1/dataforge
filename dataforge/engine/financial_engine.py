"""
DataForge Financial & Credit Health Engine.
Simulates BDDK credit card limits, KKB Findeks credit scores (1-1900),
and investment/savings behavioral profiles.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class FinancialProfile:
    findeks_credit_score: int
    credit_score_rating: str
    credit_card_limit: float
    savings_preference: str
    has_bes_pension: bool


class FinancialEngine:
    """Calculates realistic credit scores and financial limits according to BDDK & KKB rules."""

    _instance: Optional["FinancialEngine"] = None

    @classmethod
    def get_instance(cls) -> "FinancialEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_financial_profile(
        self,
        monthly_income: float,
        income_segment: str,
        age: int,
        occupation: str = "",
        rng: Optional[random.Random] = None,
    ) -> FinancialProfile:
        """Generate statistically validated financial DNA."""
        if rng is None:
            rng = random.Random()

        # 1. Findeks Credit Score (1 - 1900)
        # Public servants, physicians, tech architects have higher baseline score stability
        is_stable_profession = any(p in occupation for p in ["Memur", "Doktor", "Öğretmen", "Mühendis", "Mimar", "Hakim", "Savcı", "Yazılım"])

        if income_segment == "ust_gelir":
            score = rng.randint(1650, 1890)
        elif income_segment == "orta_ust":
            score = rng.randint(1520, 1840)
        elif income_segment == "orta_gelir":
            score = rng.randint(1400, 1750) if is_stable_profession else rng.randint(1250, 1650)
        elif income_segment == "orta_alt":
            score = rng.randint(1200, 1550)
        else:  # alt_gelir
            score = rng.randint(950, 1380)

        # Rating label
        if score >= 1700:
            rating = "Çok İyi"
        elif score >= 1500:
            rating = "İyi"
        elif score >= 1300:
            rating = "Az Riskli"
        elif score >= 1100:
            rating = "Orta Riskli"
        else:
            rating = "Yüksek Riskli"

        # 2. Credit Card Limit (BDDK rule: 2x - 4x net income)
        if age < 22:
            card_limit = round(rng.uniform(10000.0, min(monthly_income * 2.0, 30000.0)), 2)
        elif score >= 1600:
            card_limit = round(monthly_income * rng.uniform(3.0, 4.0), 2)
        elif score >= 1300:
            card_limit = round(monthly_income * rng.uniform(2.0, 3.0), 2)
        else:
            card_limit = round(monthly_income * rng.uniform(1.2, 2.0), 2)

        # 3. Savings & Investment DNA
        if income_segment in ["ust_gelir", "orta_ust"]:
            savings = rng.choices(
                ["Borsa BIST & Eurobond", "Gayrimenkul / Fon", "Altın / Döviz", "Vadeli TL Mevduat"],
                weights=[0.35, 0.30, 0.20, 0.15]
            )[0]
            has_bes = rng.random() < 0.75
        elif income_segment == "orta_gelir":
            savings = rng.choices(
                ["Altın / Döviz", "Vadeli TL Mevduat", "Bireysel Emeklilik (BES)", "Borsa BIST", "Kripto Varlıklar"],
                weights=[0.35, 0.25, 0.20, 0.10, 0.10]
            )[0]
            has_bes = rng.random() < 0.55
        else:
            savings = rng.choices(
                ["Yastık Altı Altın", "Vadeli TL Mevduat", "Düşük Tasarruf / Borç Ödeme"],
                weights=[0.40, 0.20, 0.40]
            )[0]
            has_bes = rng.random() < 0.20

        return FinancialProfile(
            findeks_credit_score=score,
            credit_score_rating=rating,
            credit_card_limit=card_limit,
            savings_preference=savings,
            has_bes_pension=has_bes,
        )
