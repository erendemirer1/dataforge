"""
DataForge Continuous Evolutionary Self-Calibration Engine.
Automatically recalibrates synthetic population belief tensors and risk appetites
in response to live macroeconomic shocks and viral social media sentiment pulses.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass
from .living_stream_engine import LivingStreamEngine, SocietalAgitationIndex


@dataclass
class EvolutionaryRecalibrationDelta:
    loss_aversion_shift: float
    institutional_cynicism_shift: float
    discretionary_budget_compression_pct: float
    dominant_polarization_anchor: str
    recalibration_summary: str


class ContinuousSocietalEvolver:
    """
    Dynamically evolves population parameters based on live environmental stream data.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.stream_engine = LivingStreamEngine.get_instance()

    def compute_evolutionary_delta(
        self,
        custom_pulse: Optional[SocietalAgitationIndex] = None
    ) -> EvolutionaryRecalibrationDelta:
        """
        Computes dynamic shifts for all downstream decision engines based on active stream.
        """
        pulse = custom_pulse or self.stream_engine.get_current_pulse()
        agitation = pulse.composite_agitation_score

        # 1. Loss Aversion Shift: High agitation increases Kahneman lambda
        # Base lambda is 2.25; high agitation pushes it up to 2.85
        lambda_shift = (agitation - 50.0) / 100.0 * 0.60

        # 2. Institutional Cynicism Shift: High inflation & polarization increase cynicism
        is_tense = any(w in pulse.social.dominant_public_emotion.lower() for w in ["kutuplaşma", "kaygı", "öfke", "isyan"])
        cynicism_shift = (pulse.macro.tufe_annual_inflation_pct / 50.0) * 0.35 + (0.15 if is_tense else 0.0)

        # 3. Discretionary Budget Compression: High USD/TRY + inflation squeezes free cash
        budget_compression = (pulse.macro.tufe_annual_inflation_pct / 100.0 * 15.0)

        # 4. Polarization Anchor
        anchor = f"Gündem: {pulse.social.active_top_headline} ({pulse.social.dominant_public_emotion})"

        summary = (
            f"Toplumsal Ajitasyon Endeksi: {agitation:.1f}/100 | "
            f"USD/TRY: {pulse.macro.usd_try_rate:.2f} ₺ | "
            f"Enflasyon Baskısı: %{pulse.macro.tufe_annual_inflation_pct:.1f} | "
            f"Baskın Duygu: {pulse.social.dominant_public_emotion}"
        )

        return EvolutionaryRecalibrationDelta(
            loss_aversion_shift=round(lambda_shift, 3),
            institutional_cynicism_shift=round(cynicism_shift, 3),
            discretionary_budget_compression_pct=round(budget_compression, 2),
            dominant_polarization_anchor=anchor,
            recalibration_summary=summary
        )
