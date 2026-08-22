"""
DataForge Counterfactual Stress Test & Calibration REST API Route.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Any
from ...cognitive.counterfactual_engine import CounterfactualStressEngine
from ...cognitive.self_calibration import SelfCalibrationEngine

router = APIRouter(prefix="/counterfactual", tags=["Counterfactual & Calibration"])


class CounterfactualShockRequest(BaseModel):
    current_ballots: list[dict[str, Any]] = Field(default=[], description="Mevcut anket sandık kayıtları")
    delta_asgari_ucret_pct: float = Field(default=0.0, description="Asgari ücret değişim yüzdesi (+%30, -%10)")
    delta_enflasyon_pct: float = Field(default=0.0, description="Enflasyon sepet değişim yüzdesi (+%40)")
    delta_kira_pct: float = Field(default=0.0, description="Kira artış değişim yüzdesi (+%50)")


@router.post(
    "/simulate-shock",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Canlı Makroekonomik What-If Stres Testi",
    description="Asgari ücret, enflasyon ve kira şoklarını mevcut nüfusun nakit akışına ve oy tercihlerine uygular."
)
async def simulate_counterfactual_shock(req: CounterfactualShockRequest):
    try:
        engine = CounterfactualStressEngine()
        result = engine.apply_macroeconomic_shock(
            current_ballots=req.current_ballots,
            delta_asgari_ucret_pct=req.delta_asgari_ucret_pct,
            delta_enflasyon_pct=req.delta_enflasyon_pct,
            delta_kira_pct=req.delta_kira_pct
        )
        return result.to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Counterfactual simulation failed: {str(e)}"
        )


@router.get(
    "/calibration-health",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Model Kalibrasyon ve Bayesian Öğrenme Sağlığı",
    description="Modelin KL-Diverjansını ve resmi anketlerle arasındaki yakınsama skorunu döner."
)
async def get_calibration_health():
    calib = SelfCalibrationEngine()
    return calib.get_global_engine_health()
