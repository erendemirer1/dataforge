"""
DataForge Municipal & National Census Polling API Route.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from ...cognitive.census_engine import MunicipalCensusEngine

router = APIRouter(prefix="/census", tags=["Census & Municipal Polling"])


class CensusPollApiRequest(BaseModel):
    question: str = Field(..., description="Belediye projesi, politika veya araştırma sorusu")
    city: str = Field(default="İstanbul", description="Hedef Şehir (İstanbul, Ankara, İzmir, Tümü)")
    district: Optional[str] = Field(default="Tümü", description="Hedef İlçe (Kadıköy, Beşiktaş, Esenyurt, Tümü)")
    sample_size: int = Field(default=1000, ge=100, le=10000, description="Örneklem büyüklüğü (100 - 10,000)")
    target_demographic: Optional[str] = Field(default=None, description="Opsiyonel hedef kesit")


@router.post(
    "/poll",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Büyük Ölçekli Sentetik Nüfus & Belediye Anketi Çalıştır",
    description="TÜİK ve SEGE ağırlıklarıyla hedeflenen il/ilçe özelinde N=100 - N=10,000 sentetik nüfus üzerinde kamuoyu araştırması yürütür."
)
async def run_census_poll(req: CensusPollApiRequest):
    try:
        engine = MunicipalCensusEngine()
        report = engine.run_census_poll(
            question=req.question,
            city=req.city,
            district=req.district,
            sample_size=req.sample_size,
            target_demographic=req.target_demographic
        )
        return report.to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Census poll failed: {str(e)}"
        )
