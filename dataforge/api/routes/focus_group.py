"""
DataForge Focus Group REST API Route.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from ..schemas import FocusGroupRequest, FocusGroupResponse
from ...cognitive.focus_simulator import FocusGroupSimulator

router = APIRouter(prefix="/focus-group", tags=["Focus Group"])


@router.post(
    "/simulate",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Sentetik Odak Grubu ve Pazar Simülasyonu Çalıştır",
    description="Hedef kitleye sunulan bir teklif veya politika için kalitatif masayı simüle eder ve N=1,000 Monte Carlo ekonometrik pazar raporu üretir."
)
async def simulate_focus_group(req: FocusGroupRequest):
    try:
        simulator = FocusGroupSimulator()
        result = simulator.run_simulation(
            target_audience=req.target_audience,
            pitch_or_question=req.pitch_or_question,
            count=req.count,
            monte_carlo_n=req.monte_carlo_n,
            api_key=req.api_key
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Focus group simulation failed: {str(e)}"
        )
