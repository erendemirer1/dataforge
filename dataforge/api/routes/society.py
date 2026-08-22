"""
DataForge Synthetic Society OS REST API Routes.
Exposes 1-on-1 Persona Interrogation, Complex Social Contagion, GIS Regional Heatmaps,
Executive Report Exports, and Macroeconomic Pipelines.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, Any
from ...cognitive.interrogation_engine import InterrogationEngine
from ...cognitive.social_contagion import SocialContagionEngine
from ...cognitive.gis_engine import GISEngine
from ...cognitive.report_exporter import ReportExporter
from ...cognitive.macro_pipeline import MacroeconomicPipeline

router = APIRouter(prefix="/society", tags=["Synthetic Society OS"])


class InterrogationApiRequest(BaseModel):
    persona_dict: dict[str, Any] = Field(..., description="Mülakat yapılacak sentetik yurttaşın profili")
    user_question: str = Field(..., description="Araştırmacının sorduğu soru")
    conversation_history: Optional[list[dict[str, str]]] = Field(default=[], description="Geçmiş diyalog mesajları")
    survey_context: Optional[str] = Field(default=None, description="Masadaki anket veya politika bağlamı")


class SocialContagionApiRequest(BaseModel):
    headline_or_rumor: str = Field(..., description="Toplumda yayılacak haber, vaat veya dedikodu")
    ballots: Optional[list[dict[str, Any]]] = Field(default=[], description="Hedef nüfus sandığı")
    virality_strength: float = Field(default=0.65, ge=0.1, le=1.0, description="Viral yayılım gücü (0.1 - 1.0)")


class ExportReportApiRequest(BaseModel):
    report_data: dict[str, Any] = Field(..., description="İhracı yapılacak anket veya odak grubu verisi")


@router.post(
    "/interrogate",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Birebir Ajan Sorgulama & Derin Mülakat",
    description="Herhangi bir sentetik yurttaşla 50+ parametreli dosyasına sadık kalarak çok turlu canlı mülakat yürütür."
)
async def interrogate_persona(req: InterrogationApiRequest):
    try:
        engine = InterrogationEngine()
        resp = engine.conduct_interview_turn(
            persona_dict=req.persona_dict,
            user_question=req.user_question,
            conversation_history=req.conversation_history,
            survey_context=req.survey_context
        )
        return {
            "persona_ad_soyad": resp.persona_ad_soyad,
            "persona_meslek": resp.persona_meslek,
            "persona_sehir_ilce": resp.persona_sehir_ilce,
            "cevap_metni": resp.cevap_metni,
            "bilincalti_refleksi": resp.bilincalti_refleksi,
            "kullanilan_arguman_tipi": resp.kullanilan_arguman_tipi
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interrogation failed: {str(e)}"
        )


@router.post(
    "/contagion",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Sosyal Bulaşım & Yankı Odası Simülatörü",
    description="Watts-Strogatz Küçük Dünya Ağı ve Granovetter eşik modeli ile haberlerin mahalleler arası yayılımını hesaplar."
)
async def simulate_social_contagion(req: SocialContagionApiRequest):
    try:
        engine = SocialContagionEngine()
        result = engine.simulate_information_cascade(
            headline_or_rumor=req.headline_or_rumor,
            ballots=req.ballots,
            virality_strength=req.virality_strength
        )
        return result.to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Contagion simulation failed: {str(e)}"
        )


@router.get(
    "/gis-heatmap",
    response_model=list[dict],
    status_code=status.HTTP_200_OK,
    summary="Türkiye Bölgesel GIS Isı Haritası",
    description="İller ve bölgeler bazında kamuoyu kabul, ret ve kutuplaşma dağılımını döner."
)
async def get_gis_heatmap(base_kabul: float = 45.0, base_ret: float = 40.0):
    engine = GISEngine()
    data = engine.get_turkey_regional_heatmap(base_kabul, base_ret)
    return [
        {
            "plaka_kodu": d.plaka_kodu,
            "il_adi": d.il_adi,
            "nuts2_bolge_kodu": d.nuts2_bolge_kodu,
            "kabul_yuzde": d.kabul_yuzde,
            "ret_yuzde": d.ret_yuzde,
            "kararsiz_yuzde": d.kararsiz_yuzde,
            "kutuplasma_endeksi": d.kutuplasma_endeksi,
            "sege_ortalama_kademe": d.sege_ortalama_kademe,
            "baskın_direnc_faktoru": d.baskın_direnc_faktoru
        }
        for d in data
    ]


@router.post(
    "/export-report",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    summary="Kurumsal Yönetici Raporu (HTML/PDF)",
    description="Bakanlık / Belediye / CEO düzeyinde resmi, yazdırılabilir HTML yönetim brifi üretir."
)
async def export_executive_report(req: ExportReportApiRequest):
    html_content = ReportExporter.generate_html_executive_brief(req.report_data)
    return HTMLResponse(content=html_content)


@router.get(
    "/macro-indicators",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Canlı Makroekonomik Göstergeler",
    description="TCMB faizi, TÜİK TÜFE, asgari ücret ve tüketici güven endeksini döner."
)
async def get_macro_indicators():
    pipeline = MacroeconomicPipeline.get_instance()
    return pipeline.get_current_macro_indicators()
