"""
DataForge Health & Social Security Engine.
Simulates SGK insurance categories (4A/4B/4C/GSS), private health insurance (TSS/ÖSS),
and Kızılay Turkish national blood type distributions.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class HealthProfile:
    sgk_category: str
    health_insurance_type: str
    blood_type: str


class HealthProfileEngine:
    """Calculates realistic social security and health insurance profiles."""

    _instance: Optional["HealthProfileEngine"] = None

    @classmethod
    def get_instance(cls) -> "HealthProfileEngine":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_health_profile(
        self,
        occupation: str,
        income_segment: str,
        age: int,
        rng: Optional[random.Random] = None,
    ) -> HealthProfile:
        """Generate statistically validated health & social security profile."""
        if rng is None:
            rng = random.Random()

        # 1. SGK Social Security Status
        if "Emekli" in occupation or age >= 65:
            if "Memur" in occupation or "Öğretmen" in occupation:
                sgk = "4C (Emekli Sandığı)"
            elif "Çiftçi" in occupation or "Esnaf" in occupation:
                sgk = "4B (Bağ-Kur Emeklisi)"
            else:
                sgk = "4A (SSK Emeklisi)"
        elif any(p in occupation for p in ["Memur", "Öğretmen", "Polis", "Hakim", "Savcı", "Zabıta", "Doktor"]):
            sgk = "4C (Kamu Görevlisi - Emekli Sandığı)"
        elif any(p in occupation for p in ["Esnaf", "Bakkal", "Çiftçi", "Ziraat", "Kasap", "Kuyumcu"]):
            sgk = "4B (Bağ-Kur - Kendi Hesabına)"
        elif "Öğrenci" in occupation or age <= 21:
            sgk = "GSS (Genel Sağlık Sigortası / Aile Kapsamı)"
        else:
            sgk = "4A (SSK - Hizmet Akdiyle Çalışan)"

        # 2. Health Insurance Type (SGK, TSS, ÖSS)
        if income_segment == "ust_gelir":
            insurance = rng.choices(
                ["Özel Sağlık Sigortası (ÖSS - Kapsamlı)", "Tamamlayıcı Sağlık Sigortası (TSS)", "SGK Devlet Güvencesi"],
                weights=[0.75, 0.20, 0.05]
            )[0]
        elif income_segment == "orta_ust":
            insurance = rng.choices(
                ["Tamamlayıcı Sağlık Sigortası (TSS)", "Özel Sağlık Sigortası (ÖSS)", "SGK Devlet Güvencesi"],
                weights=[0.60, 0.25, 0.15]
            )[0]
        elif income_segment == "orta_gelir":
            insurance = rng.choices(
                ["SGK Devlet Güvencesi", "Tamamlayıcı Sağlık Sigortası (TSS)"],
                weights=[0.65, 0.35]
            )[0]
        else:
            insurance = "SGK Devlet Güvencesi / Yeşil Kart"

        # 3. Kızılay Turkish National Blood Type Distribution
        blood_types = [
            "A Rh(+)", "0 Rh(+)", "B Rh(+)", "AB Rh(+)",
            "A Rh(-)", "0 Rh(-)", "B Rh(-)", "AB Rh(-)",
        ]
        blood_weights = [0.378, 0.298, 0.142, 0.072, 0.042, 0.039, 0.016, 0.013]
        blood = rng.choices(blood_types, weights=blood_weights)[0]

        return HealthProfile(
            sgk_category=sgk,
            health_insurance_type=insurance,
            blood_type=blood,
        )
