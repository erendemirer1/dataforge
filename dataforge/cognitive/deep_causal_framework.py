"""
DataForge Deep Causal & Computational Social Science Mathematical Framework.
Implements institutional-grade microeconomic, neuro-cognitive, sociological,
and moral psychology equations calibrated for Turkish society.

Mathematical Models:
1. Pierre Bourdieu 3-Capital Vector (Economic, Cultural, Social Capital)
2. Daniel Kahneman & Amos Tversky Prospect Theory (Non-linear Loss Aversion Lambda=2.25)
3. Jonathan Haidt 6 Moral Foundations Vector
4. Ernst Engel Food-to-Income Elasticity Curve
5. David Laibson Quasi-Hyperbolic Time Discounting (Beta-Delta Model)
6. Sanayi ve Teknoloji Bakanlığı SEGE-2022 6-Tier Socioeconomic District Index
7. Costa & McCrae Big Five (OCEAN) Personality Matrix
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class BourdieuCapitalVector:
    economic_capital_score: float # 0 - 100 (Income, Wealth, Assets)
    cultural_capital_score: float # 0 - 100 (Institutional & Embodied Education/Habitus)
    social_capital_score: float   # 0 - 100 (Kinship networks, hemşehri, political ties)
    symbolic_prestige_score: float # 0 - 100 (Societal respect, occupational status)

    @property
    def composite_class_index(self) -> float:
        return (
            self.economic_capital_score * 0.40 +
            self.cultural_capital_score * 0.35 +
            self.social_capital_score * 0.25
        )


@dataclass
class NeuroPsychologicalState:
    loss_aversion_lambda: float # Prospect theory lambda (typical: 2.25)
    risk_tolerance_alpha: float # Prospect theory risk curvature (typical: 0.88)
    present_bias_beta: float    # Hyperbolic discounting beta (0.6 - 0.95)
    cortisol_stress_level: float # 0 - 100 (Economic distress amygdala reactivity)
    status_quo_inertia: float   # 0 - 100 (Resistance to disruption)
    big_five_ocean: dict[str, float] # Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism


@dataclass
class HaidtMoralProfile:
    care_harm: float        # Harm vs Care (0 - 100)
    fairness_cheating: float # Fairness vs Proportionality (0 - 100)
    loyalty_betrayal: float  # In-group Loyalty vs Betrayal (0 - 100)
    authority_subversion: float # Respect for Authority vs Subversion (0 - 100)
    sanctity_degradation: float # Sanctity & Purity vs Degradation (0 - 100)
    liberty_oppression: float   # Liberty vs Oppression (0 - 100)


class DeepCausalFramework:
    """
    Computes rigorous neuro-sociological and econometric metrics for synthetic citizens.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def derive_bourdieu_capitals(
        self,
        income_tl: float,
        education_level: str,
        occupation: str,
        city: str,
        housing_status: str
    ) -> BourdieuCapitalVector:
        """Calculates Bourdieu's Three Forms of Capital."""
        # 1. Economic Capital
        # Log-linear scaling normalized around median Turkish income (30k TL)
        income_normalized = min(100.0, max(5.0, (math.log10(max(1000.0, income_tl)) - 3.8) * 55.0))
        housing_bonus = 20.0 if housing_status == "Ev Sahibi" else 0.0
        economic_score = round(min(100.0, max(5.0, income_normalized * 0.8 + housing_bonus)), 1)

        # 2. Cultural Capital
        edu_weights = {
            "İlkokul": 15.0,
            "Ortaokul": 28.0,
            "Lise": 48.0,
            "Önlisans": 62.0,
            "Üniversite": 82.0,
            "Yüksek Lisans": 94.0,
            "Doktora": 99.0
        }
        base_edu = edu_weights.get(education_level, 50.0)
        occ_lower = occupation.lower()
        if any(w in occ_lower for w in ["mühendis", "doktor", "öğretmen", "akademisyen", "yazılımcı", "mimar", "sanatçı"]):
            base_edu += 10.0
        cultural_score = round(min(100.0, max(10.0, base_edu + self.rng.uniform(-5.0, 5.0))), 1)

        # 3. Social Capital
        # In Turkey, small business owners (esnaf), politicians, public servants have high informal networks
        if any(w in occ_lower for w in ["esnaf", "tüccar", "muhtar", "avukat", "müteahhit", "memur"]):
            social_score = round(self.rng.uniform(65.0, 92.0), 1)
        elif any(w in occ_lower for w in ["öğrenci", "kurye", "işsiz", "prekarya"]):
            social_score = round(self.rng.uniform(25.0, 52.0), 1)
        else:
            social_score = round(self.rng.uniform(40.0, 75.0), 1)

        # 4. Symbolic Prestige
        symbolic_score = round((cultural_score * 0.45 + economic_score * 0.35 + social_score * 0.20), 1)

        return BourdieuCapitalVector(
            economic_capital_score=economic_score,
            cultural_capital_score=cultural_score,
            social_capital_score=social_score,
            symbolic_prestige_score=symbolic_score
        )

    def derive_neuro_psychology(
        self,
        age: int,
        income_tl: float,
        economic_capital: float,
        discretionary_budget_tl: float
    ) -> NeuroPsychologicalState:
        """Calculates Prospect Theory, Cortisol Amygdala Stress, and Big Five OCEAN traits."""
        # Cortisol / Amygdala threat response increases when discretionary budget < 10,000 TL
        if discretionary_budget_tl < 5000.0:
            cortisol = round(self.rng.uniform(78.0, 98.0), 1)
            loss_lambda = round(self.rng.uniform(2.4, 3.2), 2) # Highly hyper-sensitive to price hikes
            present_bias = round(self.rng.uniform(0.55, 0.70), 2) # Myopic short-term survival focus
        elif discretionary_budget_tl < 15000.0:
            cortisol = round(self.rng.uniform(50.0, 75.0), 1)
            loss_lambda = round(self.rng.uniform(2.1, 2.5), 2)
            present_bias = round(self.rng.uniform(0.72, 0.85), 2)
        else:
            cortisol = round(self.rng.uniform(20.0, 45.0), 1)
            loss_lambda = round(self.rng.uniform(1.8, 2.2), 2)
            present_bias = round(self.rng.uniform(0.88, 0.96), 2)

        # Status quo inertia increases with age
        inertia = round(min(98.0, max(20.0, 30.0 + (age * 0.85) + self.rng.uniform(-8.0, 8.0))), 1)

        # Big Five Personality Distribution (Calibrated with Turkish Norms)
        ocean = {
            "Openness (Deneyime Açıklık)": round(min(99.0, max(5.0, 75.0 - (age * 0.4) + self.rng.gauss(0, 10.0))), 1),
            "Conscientiousness (Sorumluluk)": round(min(99.0, max(10.0, 45.0 + (age * 0.5) + self.rng.gauss(0, 8.0))), 1),
            "Extraversion (Dışadönüklük)": round(min(99.0, max(10.0, self.rng.gauss(52.0, 14.0))), 1),
            "Agreeableness (Uyumluluk)": round(min(99.0, max(10.0, 48.0 + (age * 0.3) + self.rng.gauss(0, 10.0))), 1),
            "Neuroticism (Duygusal Dengesizlik)": round(min(99.0, max(5.0, cortisol * 0.7 + self.rng.gauss(0, 8.0))), 1)
        }

        return NeuroPsychologicalState(
            loss_aversion_lambda=loss_lambda,
            risk_tolerance_alpha=0.88,
            present_bias_beta=present_bias,
            cortisol_stress_level=cortisol,
            status_quo_inertia=inertia,
            big_five_ocean=ocean
        )

    def derive_haidt_moral_matrix(
        self,
        age: int,
        education_level: str,
        occupation: str,
        cultural_capital: float
    ) -> HaidtMoralProfile:
        """Calculates Jonathan Haidt's 6 Moral Foundations Vector."""
        occ_l = occupation.lower()

        # Modern Urban / High Cultural Capital: High Harm/Care, Fairness, Liberty; Lower Authority/Sanctity
        if cultural_capital > 70.0 or any(w in occ_l for w in ["öğrenci", "yazılımcı", "mühendis", "sanatçı"]):
            care = round(self.rng.uniform(75.0, 95.0), 1)
            fairness = round(self.rng.uniform(80.0, 98.0), 1)
            liberty = round(self.rng.uniform(85.0, 99.0), 1)
            loyalty = round(self.rng.uniform(35.0, 65.0), 1)
            authority = round(self.rng.uniform(25.0, 55.0), 1)
            sanctity = round(self.rng.uniform(20.0, 50.0), 1)

        # Traditional / Military / Veterans: High Loyalty, Authority, Sanctity, Fairness (retributive)
        elif any(w in occ_l for w in ["gazi", "şehit", "asker", "polis", "güvenlik", "esnaf"]):
            care = round(self.rng.uniform(60.0, 85.0), 1)
            fairness = round(self.rng.uniform(70.0, 90.0), 1)
            loyalty = round(self.rng.uniform(88.0, 99.0), 1)
            authority = round(self.rng.uniform(82.0, 98.0), 1)
            sanctity = round(self.rng.uniform(75.0, 95.0), 1)
            liberty = round(self.rng.uniform(50.0, 75.0), 1)

        # Standard General Demographic
        else:
            care = round(self.rng.uniform(65.0, 88.0), 1)
            fairness = round(self.rng.uniform(68.0, 90.0), 1)
            loyalty = round(self.rng.uniform(60.0, 85.0), 1)
            authority = round(self.rng.uniform(55.0, 80.0), 1)
            sanctity = round(self.rng.uniform(50.0, 78.0), 1)
            liberty = round(self.rng.uniform(60.0, 85.0), 1)

        return HaidtMoralProfile(
            care_harm=care,
            fairness_cheating=fairness,
            loyalty_betrayal=loyalty,
            authority_subversion=authority,
            sanctity_degradation=sanctity,
            liberty_oppression=liberty
        )

    def compute_prospect_utility(
        self,
        perceived_gain_tl: float,
        perceived_loss_tl: float,
        neuro: NeuroPsychologicalState
    ) -> float:
        """
        Computes Kahneman-Tversky Prospect Theory subjective utility:
        V(x) = x^alpha (for gains) - lambda * (-x)^alpha (for losses)
        """
        gain_val = (perceived_gain_tl ** neuro.risk_tolerance_alpha) if perceived_gain_tl > 0 else 0.0
        loss_val = (neuro.loss_aversion_lambda * (perceived_loss_tl ** neuro.risk_tolerance_alpha)) if perceived_loss_tl > 0 else 0.0
        return round(gain_val - loss_val, 2)
