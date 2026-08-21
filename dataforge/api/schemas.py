"""
DataForge API Pydantic Schemas.
Defines strict Request/Response models for the REST API.
"""
from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


# --- Focus Group Schemas ---
class FocusGroupRequest(BaseModel):
    target_audience: str = Field(..., description="Hedef kitle tanımı (örn: 'işsiz yazılımcılar')")
    pitch_or_question: str = Field(..., description="Test edilecek ürün teklifi, soru veya politika")
    count: int = Field(default=6, ge=1, le=1000, description="Kalitatif masa simülasyonu katılımcı sayısı")
    monte_carlo_n: int = Field(default=1000, ge=100, le=10000, description="Kantitatif Monte Carlo örneklem büyüklüğü")


class FocusGroupDiscussionItem(BaseModel):
    ad_soyad: str
    meslek: str
    karar: str
    ic_ses_bilincalti: str
    disa_soylenen_soz: str


class WhatIfStressTest(BaseModel):
    senaryo_1_guvence: Optional[str] = None
    senaryo_2_fiyat: Optional[str] = None
    en_hizli_ikna_olacak_segment: Optional[str] = None


class ExecutiveReport(BaseModel):
    genel_kabul_orani_yuzde: float
    en_buyuk_3_itiraz_bariyeri: list[Any]
    fiyat_duyarlilik_analizi: str
    kutuplasma_indeksi_skoru: Optional[str] = None
    what_if_karsi_olgusal_stres_testi: Optional[WhatIfStressTest] = None
    stratejik_urun_tavsiyesi: str


class MonteCarloReport(BaseModel):
    domain_turu: str
    orneklem_buyuklugu: int
    test_edilen_fiyat_tl: Optional[float] = None
    matematiksel_kabul_orani_yuzde: float
    guven_araligi_yuzde_95: str
    fiyat_esneklik_skoru: Optional[float] = None
    ortalama_serbest_butce_tl: Optional[float] = None
    butce_yetersizlik_orani_yuzde: Optional[float] = None
    ahlaki_direnc_indeksi: Optional[float] = None


class FocusGroupResponse(BaseModel):
    odak_grubu_tartismasi: list[FocusGroupDiscussionItem]
    yonetici_pazar_analiz_raporu: ExecutiveReport
    kantitatif_monte_carlo_raporu: Optional[MonteCarloReport] = None


# --- Synthetic Generation Schemas ---
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Üretilecek profilin tanımı (örn: 'Kadıköy esnafı')")
    count: int = Field(default=10, ge=1, le=1000, description="Üretilecek kişi adedi")
    format: str = Field(default="json", description="Çıktı formatı: json | csv | parquet | sql")


class GenerateResponse(BaseModel):
    count: int
    data: list[dict[str, Any]]
    execution_time_ms: float


# --- Radar Schemas ---
class RadarSyncResponse(BaseModel):
    durum: str
    eklenen_veri_adedi: int
    zaman_damgasi: str
    toplam_hafiza_kaydi: int


class RadarStatusResponse(BaseModel):
    veritabani_konumu: str
    toplam_kayit: int
    kategori_dagilimi: dict[str, int]
    son_guncelleme: str
