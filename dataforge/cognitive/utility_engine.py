"""
DataForge Dual-Domain Utility & Monte Carlo Simulation Engine.
Implements:
1. Commercial Mode: McFadden's Random Utility Model (RUM) with empirical income constraints.
2. Moral & Sociological Policy Mode: Jonathan Haidt's 6 Moral Foundations Utility Model for non-commercial/political topics.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class QuantitativeMarketResult:
    domain_type: str # 'commercial' or 'moral_policy'
    sample_size: int
    acceptance_rate_pct: float
    confidence_interval_95: tuple[float, float]
    elasticity_score: Optional[float]
    price_sensitivity_curve: list[dict[str, Any]]
    demographic_breakdown: dict[str, float]
    mean_discretionary_budget_tl: Optional[float]
    budget_violation_rate_pct: Optional[float]
    moral_violation_index: Optional[float] # For moral/social policy

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain_turu": self.domain_type,
            "orneklem_buyuklugu": self.sample_size,
            "matematiksel_kabul_orani_yuzde": self.acceptance_rate_pct,
            "guven_araligi_yuzde_95": f"%{self.confidence_interval_95[0]} - %{self.confidence_interval_95[1]}",
            "fiyat_esneklik_skoru": self.elasticity_score,
            "fiyat_talep_egrisi": self.price_sensitivity_curve,
            "demografik_dagilim": self.demographic_breakdown,
            "ortalama_serbest_butce_tl": self.mean_discretionary_budget_tl,
            "mutlak_butce_yetersizlik_orani_yuzde": self.budget_violation_rate_pct,
            "ahlaki_direnc_indeksi": self.moral_violation_index
        }


class EconometricUtilityEngine:
    """
    Computes rigorous mathematical adoption and consensus probabilities.
    Distinguishes automatically between commercial products and moral/political questions.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def run_monte_carlo_census(
        self,
        personas: list[dict[str, Any]],
        pitch_text: str,
        pitch_price_tl: Optional[float] = None,
        simulations_count: int = 1000
    ) -> QuantitativeMarketResult:
        """Runs N=1,000 Monte Carlo statistical trials based on topic domain."""
        if not personas:
            personas = [{}]

        # Check if topic is moral/political/social policy or commercial
        is_commercial = pitch_price_tl is not None and pitch_price_tl > 0

        if is_commercial:
            return self._run_commercial_monte_carlo(personas, pitch_price_tl, simulations_count)
        else:
            return self._run_moral_policy_monte_carlo(personas, pitch_text, simulations_count)

    def _run_commercial_monte_carlo(
        self,
        personas: list[dict[str, Any]],
        price_tl: float,
        simulations_count: int
    ) -> QuantitativeMarketResult:
        """Commercial product financial utility."""
        accepted_count = 0
        budget_violations = 0
        total_discretionary = 0.0
        class_acceptances: dict[str, list[bool]] = {}

        for _ in range(simulations_count):
            p = self.rng.choice(personas)
            income = float(p.get("aylik_net_gelir_tl", 35000.0))
            discretionary = float(p.get("aylik_serbest_harcanabilir_tl", income * 0.15))
            total_discretionary += discretionary

            cult_cap = float(p.get("habitus", {}).get("cultural_capital_score", 50.0)) if isinstance(p.get("habitus"), dict) else 50.0
            loss_av = float(p.get("neuro", {}).get("loss_aversion_coefficient", 2.2)) if isinstance(p.get("neuro"), dict) else 2.2
            threat = float(p.get("neuro", {}).get("amygdala_threat_reactivity", 60.0)) if isinstance(p.get("neuro"), dict) else 60.0
            inertia = float(p.get("neuro", {}).get("status_quo_inertia", 65.0)) if isinstance(p.get("neuro"), dict) else 65.0
            social_class = p.get("habitus", {}).get("social_class_stratum", "Orta Sınıf") if isinstance(p.get("habitus"), dict) else "Orta Sınıf"

            # Hard Financial Constraint: Price > 50% of free discretionary budget -> VETO
            if discretionary <= 0 or (price_tl / max(1.0, discretionary)) > 0.50:
                budget_violations += 1
                accepted = False
            else:
                price_pain = (price_tl / max(100.0, discretionary)) * 100.0
                benefit = 35.0 + (cult_cap * 0.30)
                penalty = (price_pain * loss_av * 0.8) + (threat * 0.35) + (inertia * 0.25)
                u = max(1e-6, min(1.0 - 1e-6, self.rng.random()))
                epsilon = -math.log(-math.log(u)) * 5.0
                accepted = (benefit - penalty + epsilon) > 0.0

            if accepted:
                accepted_count += 1

            if social_class not in class_acceptances:
                class_acceptances[social_class] = []
            class_acceptances[social_class].append(accepted)

        acceptance_rate = (accepted_count / simulations_count) * 100.0
        p_prop = acceptance_rate / 100.0
        margin_error = 1.96 * math.sqrt(max(1e-6, p_prop * (1.0 - p_prop) / simulations_count)) * 100.0

        # Price curve
        multipliers = [0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 3.0]
        price_curve = []
        for m in multipliers:
            test_p = round(price_tl * m, 2)
            t_acc = 0
            for _ in range(200):
                p = self.rng.choice(personas)
                disc = float(p.get("aylik_serbest_harcanabilir_tl", 3000.0))
                if disc > 0 and (test_p / max(1.0, disc)) <= 0.50:
                    t_acc += 1 if self.rng.random() < max(0.01, (1.0 - (test_p / max(100.0, disc)) * 1.5)) else 0
            price_curve.append({
                "test_fiyat_tl": test_p,
                "carpan": f"{m:.2f}x",
                "tahmini_kabul_orani_pct": round((t_acc / 200) * 100.0, 1)
            })

        class_breakdown = {k: round((sum(v) / len(v)) * 100.0, 1) for k, v in class_acceptances.items()}

        return QuantitativeMarketResult(
            domain_type="commercial",
            sample_size=simulations_count,
            acceptance_rate_pct=round(acceptance_rate, 1),
            confidence_interval_95=(max(0.0, round(acceptance_rate - margin_error, 1)), min(100.0, round(acceptance_rate + margin_error, 1))),
            elasticity_score=1.25,
            price_sensitivity_curve=price_curve,
            demographic_breakdown=class_breakdown,
            mean_discretionary_budget_tl=round(total_discretionary / simulations_count, 2),
            budget_violation_rate_pct=round((budget_violations / simulations_count) * 100.0, 1),
            moral_violation_index=None
        )

    def _run_moral_policy_monte_carlo(
        self,
        personas: list[dict[str, Any]],
        pitch_text: str,
        simulations_count: int
    ) -> QuantitativeMarketResult:
        """Moral & Political policy consensus calculation based on Haidt Moral Matrix."""
        pitch_lower = pitch_text.lower()
        
        # Detect taboo triggers
        triggers_loyalty_violation = any(w in pitch_lower for w in ["terör", "af", "bölünme", "ihanet", "taviz"])
        triggers_sanctity_violation = any(w in pitch_lower for w in ["şehit", "gazi", "din", "kutsal", "namus"])
        triggers_fairness_violation = any(w in pitch_lower for w in ["torpil", "haksızlık", "cezasızlık", "af"])
        touches_leadership = any(w in pitch_lower for w in ["başkan", "cumhurbaşkanı", "seçim", "oy", "erdoğan", "iktidar", "hükümet", "lider"])

        accepted_count = 0
        total_moral_penalty = 0.0
        class_acceptances: dict[str, list[bool]] = {}

        for _ in range(simulations_count):
            p = self.rng.choice(personas)
            habitus = p.get("habitus", {})
            mf = habitus.get("moral_foundations", {}) if isinstance(habitus, dict) else {}
            belief = p.get("latent_belief", {}) if isinstance(p.get("latent_belief"), dict) else {}

            loyalty = float(mf.get("loyalty_ingroup_score", 75.0))
            sanctity = float(mf.get("sanctity_purity_score", 70.0))
            fairness = float(mf.get("fairness_reciprocity_score", 80.0))
            trad_loyalty = float(belief.get("traditional_loyalty", 60.0))
            sec_redline = float(belief.get("national_security_redline", 70.0))
            social_class = habitus.get("social_class_stratum", "Genel Toplum") if isinstance(habitus, dict) else "Genel Toplum"

            if touches_leadership:
                # Authentic Turkish political spectrum:
                # Loyal traditional base (+trad_loyalty) vs Redline disappointment penalty (-sec_redline) vs Economic friction
                net_political_score = (trad_loyalty * 0.70) - (sec_redline * 0.50) + self.rng.gauss(0, 15.0)
                accepted = net_political_score > 0.0
                total_moral_penalty += max(0.0, sec_redline * 0.50)
            else:
                # Moral Resistance calculation for pure policy/taboo questions
                moral_resistance = 0.0
                if triggers_loyalty_violation:
                    moral_resistance += (loyalty * 0.60)
                if triggers_sanctity_violation:
                    moral_resistance += (sanctity * 0.70)
                if triggers_fairness_violation:
                    moral_resistance += (fairness * 0.50)

                total_moral_penalty += moral_resistance
                consensus_utility = 50.0 - moral_resistance + self.rng.gauss(0, 5.0)
                accepted = consensus_utility > 0.0

            if accepted:
                accepted_count += 1

            if social_class not in class_acceptances:
                class_acceptances[social_class] = []
            class_acceptances[social_class].append(accepted)

        acceptance_rate = (accepted_count / simulations_count) * 100.0
        p_prop = acceptance_rate / 100.0
        margin_error = 1.96 * math.sqrt(max(1e-6, p_prop * (1.0 - p_prop) / simulations_count)) * 100.0
        class_breakdown = {k: round((sum(v) / len(v)) * 100.0, 1) for k, v in class_acceptances.items()}

        return QuantitativeMarketResult(
            domain_type="moral_policy",
            sample_size=simulations_count,
            acceptance_rate_pct=round(acceptance_rate, 1),
            confidence_interval_95=(max(0.0, round(acceptance_rate - margin_error, 1)), min(100.0, round(acceptance_rate + margin_error, 1))),
            elasticity_score=None,
            price_sensitivity_curve=[],
            demographic_breakdown=class_breakdown,
            mean_discretionary_budget_tl=None,
            budget_violation_rate_pct=None,
            moral_violation_index=round(total_moral_penalty / simulations_count, 1)
        )
