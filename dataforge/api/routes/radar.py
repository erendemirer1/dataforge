"""
DataForge Live Cultural & Social Radar REST API Route.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from ..schemas import RadarSyncResponse, RadarStatusResponse
from ...social.cultural_memory import CulturalMemoryStore
from ...social.social_radar import SocialRadarEngine

router = APIRouter(prefix="/radar", tags=["Live Social Radar"])


@router.get(
    "/pulse",
    status_code=status.HTTP_200_OK,
    summary="Canlı Sosyo-Ekonomik ve Kültürel Nabız",
    description="Türkiye'nin 6 canlı web kaynağından toplanan en güncel trendler, enflasyon manşetleri ve forum gündemini döndürür."
)
async def get_live_pulse():
    try:
        radar = SocialRadarEngine()
        return radar.get_current_macro_sentiment()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch live pulse: {str(e)}"
        )


@router.post(
    "/sync",
    response_model=RadarSyncResponse,
    status_code=status.HTTP_200_OK,
    summary="Canlı Hafıza Senkronizasyonu Tetikle",
    description="Tüm canlı kaynakları tarar ve yerel SQLite kültürel hafıza deposuna yeni kayıtlar ekler."
)
async def trigger_radar_sync():
    try:
        store = CulturalMemoryStore()
        res = store.sync_live_pulse()
        return RadarSyncResponse(**res)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Radar sync failed: {str(e)}"
        )


@router.get(
    "/status",
    response_model=RadarStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Kültürel Hafıza Durumu ve İstatistikleri",
    description="Depolanan toplam hafıza kaydı, kategori dağılımı ve son güncelleme zamanını gösterir."
)
async def get_radar_status():
    try:
        store = CulturalMemoryStore()
        stats = store.get_memory_stats()
        return RadarStatusResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get radar status: {str(e)}"
        )
