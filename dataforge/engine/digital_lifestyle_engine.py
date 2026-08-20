"""
DataForge Digital Lifestyle & Consumer Telecommunications Engine.
Simulates mobile smartphone models, operating systems, GSM operators (BTK shares),
monthly data consumption, and digital subscription packages.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DigitalLifestyleProfile:
    smartphone_model: str
    operating_system: str
    gsm_operator: str
    monthly_data_gb: int
    digital_subscriptions: list[str]


class DigitalLifestyleEngine:
    """Calculates realistic digital device, carrier, and streaming subscription profiles."""

    _instance: Optional["DigitalLifestyleEngine"] = None

    @classmethod
    def get_instance(cls) -> "DigitalLifestyleEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_digital_profile(
        self,
        income_segment: str,
        age: int,
        rng: Optional[random.Random] = None,
    ) -> DigitalLifestyleProfile:
        """Generate statistically grounded telecom and digital profile."""
        if rng is None:
            rng = random.Random()

        # 1. Smartphone Model & Operating System
        if income_segment in ["ust_gelir", "orta_ust"]:
            if rng.random() < 0.72:
                model = rng.choice(["Apple iPhone 16 Pro Max", "Apple iPhone 15 Pro", "Apple iPhone 15", "Apple iPhone 14"])
                os_name = "iOS 18"
            else:
                model = rng.choice(["Samsung Galaxy S24 Ultra", "Samsung Galaxy Z Fold 5", "Xiaomi 14 Ultra"])
                os_name = "Android 15"
        elif income_segment == "orta_gelir":
            if rng.random() < 0.40:
                model = rng.choice(["Apple iPhone 13", "Apple iPhone 12", "Apple iPhone SE (2022)"])
                os_name = "iOS 17"
            else:
                model = rng.choice(["Samsung Galaxy A55 5G", "Samsung Galaxy A35", "Xiaomi Redmi Note 13 Pro", "POCO X6 Pro"])
                os_name = "Android 14"
        else:  # alt_gelir, orta_alt
            if age >= 68 and rng.random() < 0.40:
                model = "Nokia 3310 (Tuşlu Klasik)"
                os_name = "Feature Phone OS"
            else:
                model = rng.choice(["Samsung Galaxy A15", "Xiaomi Redmi 13C", "Reeder S19 Max Pro", "Casper VIA M30"])
                os_name = "Android 13"

        # 2. GSM Operator (BTK 2024 Market Share: Turkcell %41, Vodafone %31, Türk Telekom %28)
        operator = rng.choices(
            ["Turkcell", "Vodafone Türkiye", "Türk Telekom Mobil"],
            weights=[0.41, 0.31, 0.28]
        )[0]

        # 3. Monthly Mobile Internet Consumption (GB)
        if age < 28:
            data_gb = rng.randint(25, 60)
        elif age < 50:
            data_gb = rng.randint(15, 40)
        else:
            data_gb = rng.randint(5, 15)

        # 4. Digital Subscriptions (Streaming / Music / Video)
        sub_pool = []
        if age < 45:
            if rng.random() < 0.65:
                sub_pool.append("Spotify Türkiye")
            if rng.random() < 0.70:
                sub_pool.append("Netflix Türkiye")
            if rng.random() < 0.55:
                sub_pool.append("YouTube Premium")
            if rng.random() < 0.50:
                sub_pool.append("Amazon Prime Video")
            if rng.random() < 0.25:
                sub_pool.append("Disney+ Türkiye")
            if rng.random() < 0.30:
                sub_pool.append("TOD / beIN Connect")  # Süper Lig / Futbol
        else:
            if rng.random() < 0.45:
                sub_pool.append("Netflix Türkiye")
            if rng.random() < 0.35:
                sub_pool.append("BluTV")
            if rng.random() < 0.30:
                sub_pool.append("TOD / beIN Connect")

        return DigitalLifestyleProfile(
            smartphone_model=model,
            operating_system=os_name,
            gsm_operator=operator,
            monthly_data_gb=data_gb,
            digital_subscriptions=sub_pool,
        )
