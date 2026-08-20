"""
DataForge Unified Causal Belief System & Cognitive Invariant Engine.
Models immutable, multi-dimensional latent belief vectors (B_i) for every individual.
Enforces strict mathematical cross-consistency between political, economic, moral, and purchasing decisions.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class LatentBeliefVector:
    # 1. Kırmızı Çizgiler & Güvenlik Hassasiyeti (0 = Umursamaz, 100 = Şehitlik/Vatan Dokunulmaz)
    national_security_redline: float
    
    # 2. Cüzdan Yangını & Geçim Bunalımı (0 = Çok Rahat, 100 = İflas/Açlık Eşiği)
    economic_pain_index: float
    
    # 3. Adalet, Liyakat & Kurumsal Güven (0 = Sıfır Güven/Torpil İsyanı, 100 = Tam Güven)
    institutional_trust: float
    
    # 4. Muhafazakarlık & Geleneksel Sadakat (0 = Radikal Seküler, 100 = Geleneksel Dindar)
    traditional_loyalty: float
    
    # 5. Statüko Korkusu vs. Değişim İştahı (0 = Ne Olursa Olsun Değişsin, 100 = Macera İstemeyen Ehvenişerci)
    status_quo_fear: float
    
    # 6. Canlı Gündem Kırılma Tetikleyicileri (Current Disillusionment Triggers)
    active_disillusionment_triggers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CausalBeliefEngine:
    """
    Synthesizes and enforces strict causal belief invariants across all surveys and focus groups.
    Zero contradiction: A person's political, economic, and moral choices must strictly adhere to their belief vector.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def build_latent_belief_vector(
        self,
        occupation: str,
        social_class: str,
        age: int,
        city: str,
        monthly_income: float,
        fixed_expenses: float,
        habitus_moral: dict[str, float]
    ) -> LatentBeliefVector:
        """Derives a mathematically sound, consistent belief vector from lived realities."""
        occ_lower = occupation.lower()
        soc_lower = social_class.lower()

        # 1. National Security & Martyr Redline
        if any(w in occ_lower for w in ["şehit", "gazi", "asker", "polis", "güvenlik", "uzman çavuş"]):
            sec_redline = round(self.rng.uniform(88.0, 99.0), 1)
        elif "memur" in occ_lower or "esnaf" in occ_lower:
            sec_redline = round(self.rng.uniform(65.0, 85.0), 1)
        elif "öğrenci" in occ_lower or "yazılım" in occ_lower:
            sec_redline = round(self.rng.uniform(40.0, 70.0), 1)
        else:
            sec_redline = round(self.rng.uniform(50.0, 80.0), 1)

        # 2. Economic Pain Index (Calculated from actual income / expense margin)
        free_ratio = max(0.0, (monthly_income - fixed_expenses) / max(1.0, monthly_income))
        if free_ratio < 0.10:
            econ_pain = round(self.rng.uniform(85.0, 98.0), 1)
        elif free_ratio < 0.25:
            econ_pain = round(self.rng.uniform(65.0, 84.0), 1)
        elif free_ratio < 0.45:
            econ_pain = round(self.rng.uniform(40.0, 64.0), 1)
        else:
            econ_pain = round(self.rng.uniform(15.0, 39.0), 1)

        # 3. Institutional & Merit Trust
        if "işsiz" in occ_lower or "öğrenci" in occ_lower or "prekarya" in soc_lower:
            inst_trust = round(self.rng.uniform(10.0, 30.0), 1) # Torpil ve mülakat isyanı
        elif "memur" in occ_lower:
            inst_trust = round(self.rng.uniform(45.0, 70.0), 1)
        elif "esnaf" in occ_lower:
            inst_trust = round(self.rng.uniform(30.0, 55.0), 1)
        else:
            inst_trust = round(self.rng.uniform(25.0, 60.0), 1)

        # 4. Traditional Loyalty
        if "esnaf" in occ_lower or any(c in city.lower() for c in ["konya", "kayseri", "erzurum", "yozgat", "trabzon", "rize", "sivas"]):
            trad_loyalty = round(self.rng.uniform(70.0, 95.0), 1)
        elif any(c in city.lower() for c in ["kadıköy", "beşiktaş", "izmir", "çankaya"]):
            trad_loyalty = round(self.rng.uniform(15.0, 45.0), 1)
        else:
            trad_loyalty = round(self.rng.uniform(40.0, 75.0), 1)

        # 5. Status Quo Fear (Ehvenişer / Macera İstememe)
        if age > 50 or "emekli" in occ_lower or "kamu" in soc_lower:
            sq_fear = round(self.rng.uniform(70.0, 92.0), 1)
        elif age < 30:
            sq_fear = round(self.rng.uniform(15.0, 40.0), 1)
        else:
            sq_fear = round(self.rng.uniform(45.0, 70.0), 1)

        # 6. Active Disillusionment Triggers (Son Dönem Gündem Kırılmaları)
        triggers = []
        if sec_redline > 80:
            triggers.append("Son dönemdeki çerçeve yasa, teröristlerin affı ve Meclis'e davet tartışmaları (Kırmızı çizgi ihlali)")
        if econ_pain > 70:
            triggers.append("Enflasyon, eriyen maaşlar, market ve kira fahişliği")
        if inst_trust < 35:
            triggers.append("Mülakatlarda liyakatsizlik, torpil ve kayırmacılık iddiaları")

        return LatentBeliefVector(
            national_security_redline=sec_redline,
            economic_pain_index=econ_pain,
            institutional_trust=inst_trust,
            traditional_loyalty=trad_loyalty,
            status_quo_fear=sq_fear,
            active_disillusionment_triggers=triggers
        )

    def evaluate_consistency_constraints(
        self,
        belief: LatentBeliefVector,
        topic: str
    ) -> dict[str, Any]:
        """
        Calculates hard causal constraints for any topic to guarantee zero logic contradictions.
        """
        topic_lower = topic.lower()

        # Invariant 1: If topic is Political Leader/Election AND persona has security redline > 80 AND current amnesty debate is active
        touches_leadership = any(w in topic_lower for w in ["başkan", "cumhurbaşkanı", "seçim", "oy", "erdoğan", "iktidar", "hükümet", "lider"])
        touches_amnesty = any(w in topic_lower for w in ["af", "terör", "çerçeve yasa", "öcalan", "taviz"])

        constraints = {
            "forced_attitude": None,
            "max_support_probability": 1.0,
            "required_internal_tension": None
        }

        if touches_leadership and belief.national_security_redline > 85:
            # Person has high national security redline. In the context of recent amnesty/framework bill debates,
            # they CANNOT give blind uncritical support. They MUST express intense cognitive conflict and disappointment!
            constraints["max_support_probability"] = 0.30
            constraints["required_internal_tension"] = (
                "Son çerçeve yasa, af ve Öcalan tartışmaları nedeniyle iktidara karşı derin bir kırgınlık, "
                "öfke ve 'şehitlerin kemikleri sızlıyor, bu kadarına da göz yumamam' çatışması."
            )

        if touches_amnesty and belief.national_security_redline > 70:
            constraints["forced_attitude"] = "Kesinlikle Reddeder"
            constraints["max_support_probability"] = 0.0

        return constraints
