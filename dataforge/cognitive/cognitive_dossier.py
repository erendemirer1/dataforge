"""
DataForge Academic Cognitive Dossier & Computational Social Science Engine.
Compiles 50+ multidimensional parameters into a unified, institutional-grade
Biographical & Neuro-Sociological Dossier for synthetic personas.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict

from .cognitive_persona import DeepCognitivePersona
from .deep_causal_framework import BourdieuCapitalVector, HaidtMoralProfile, NeuroPsychologicalState


@dataclass
class CognitiveDossier:
    # 1. Kimlik ve Sosyo-Mekansal Çapa
    kisi_id: int
    ad_soyad: str
    yas: int
    cinsiyet: str
    sehir: str
    ilce: str
    mahalle: str
    sege_kademe: int
    ilce_arketipi: str
    
    # 2. Meslek, Eğitim ve Emek Piyasası
    meslek: str
    egitim_seviyesi: str
    calisma_sekli: str # "Ofis", "Uzaktan (Remote)", "Saha", "Vardiyalı"
    
    # 3. Finansal Bilanço & Gelir Tablosu
    aylik_net_gelir_tl: float
    aylik_brut_gelir_tl: float
    vergi_dilimi: str
    sgk_kategorisi: str
    barinma_durumu: str
    aylik_kira_veya_konut_kredisi_tl: float
    aylik_sabit_giderler_tl: float
    aylik_serbest_harcanabilir_nakit_tl: float
    borcluluk_orani_yuzde: float
    findeks_kredi_notu: int
    yatirim_portfoy_tercihi: str
    
    # 4. Pierre Bourdieu 3-Sermaye & Habitus
    ekonomik_sermaye_skoru: float # 0 - 100
    kulturel_sermaye_skoru: float # 0 - 100
    sosyal_sermaye_skoru: float   # 0 - 100
    sembolik_prestij_skoru: float # 0 - 100
    sinif_fraksiyonu: str
    
    # 5. Jonathan Haidt 6-Ahlak Temelleri (Moral Foundations Theory)
    sefqat_zarar_karsitligi: float   # 0 - 100
    adalet_hakkaniyet: float        # 0 - 100
    sadakat_grup_aidiyeti: float    # 0 - 100
    otorite_hiyerarsi: float        # 0 - 100
    kutsallik_muhafazakarlik: float # 0 - 100
    ozgurluk_baski_karsitligi: float# 0 - 100
    
    # 6. Nöro-Psikoloji & Karar Önyargıları (Kahneman & Laibson)
    kayiptan_kacinma_katsayisi_lambda: float # 2.25
    simdiki_zaman_onyargisi_beta: float      # 0.70
    alostatik_stres_kortizol_seviyesi: float # 0 - 100
    statukoculuk_direnci: float              # 0 - 100
    big_five_ocean: dict[str, float]
    
    # 7. Yaşam Dünyası, Günlük Dertler & Konuşma Jargonu
    en_buyuk_gunluk_derdi: str
    gizli_korkusu: str
    sosyal_statu_kaygisi: str
    konusma_ve_jargon_tarzi: str
    son_donemdeki_yasam_olayi: str

    def to_llm_system_context(self) -> str:
        """Renders the dossier into a rich academic persona prompt for LLM cognitive inhabitation."""
        return (
            f"KİMLİK: {self.ad_soyad}, {self.yas} yaşında, {self.cinsiyet}.\n"
            f"COĞRAFYA: {self.sehir} / {self.ilce} ({self.mahalle}) - {self.ilce_arketipi} (SEGE Kademe {self.sege_kademe}).\n"
            f"MESLEK & EĞİTİM: {self.meslek} ({self.egitim_seviyesi}), Çalışma: {self.calisma_sekli}.\n"
            f"FİNANSAL BİLANÇO: Net Maaş: {self.aylik_net_gelir_tl:,.0f} TL/ay (Vergi Dilimi: {self.vergi_dilimi}, {self.sgk_kategorisi}), "
            f"Barınma: {self.barinma_durumu} (Kira/Kredi: {self.aylik_kira_veya_konut_kredisi_tl:,.0f} TL), "
            f"Sabit Gider: {self.aylik_sabit_giderler_tl:,.0f} TL, Serbest Harcanabilir Nakit: {self.aylik_serbest_harcanabilir_nakit_tl:,.0f} TL, "
            f"Borç/Gelir: %{self.borcluluk_orani_yuzde:.0f}, Findeks: {self.findeks_kredi_notu}, Portföy: {self.yatirim_portfoy_tercihi}.\n"
            f"BOURDIEU SINIF HABİTUSU: {self.sinif_fraksiyonu} "
            f"(Ekon: {self.ekonomik_sermaye_skoru:.0f}, Kültür: {self.kulturel_sermaye_skoru:.0f}, Sosyal: {self.sosyal_sermaye_skoru:.0f}, Prestij: {self.sembolik_prestij_skoru:.0f}).\n"
            f"HAIDT AHLAK KOORDİNATLARI: Şefkat: {self.sefqat_zarar_karsitligi:.0f}, Adalet/Liyakat: {self.adalet_hakkaniyet:.0f}, "
            f"Grup Sadakati: {self.sadakat_grup_aidiyeti:.0f}, Otorite: {self.otorite_hiyerarsi:.0f}, Kutsallık: {self.kutsallik_muhafazakarlik:.0f}, Özgürlük: {self.ozgurluk_baski_karsitligi:.0f}.\n"
            f"NÖRO-PSİKOLOJİ: Kayıp Korkusu (Lambda): {self.kayiptan_kacinma_katsayisi_lambda:.2f}, Stres/Kortizol: {self.alostatik_stres_kortizol_seviyesi:.0f}/100, "
            f"Statüko Direnci: {self.statukoculuk_direnci:.0f}/100.\n"
            f"GÜNLÜK DERT & KORKU: {self.en_buyuk_gunluk_derdi}. Gizli Korkusu: {self.gizli_korkusu}. Statü Kaygısı: {self.sosyal_statu_kaygisi}.\n"
            f"SON YAŞAM OLAYI: {self.son_donemdeki_yasam_olayi}.\n"
            f"ÜSLUP & JARGON: {self.konusma_ve_jargon_tarzi}."
        )


class CognitiveDossierBuilder:
    """
    Constructs an institutional-grade Cognitive Dossier for any raw persona.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def build_dossier(self, p: DeepCognitivePersona) -> CognitiveDossier:
        parts = p.sehir_ilce.split('/')
        city = parts[0].strip() if len(parts) > 0 else "İstanbul"
        district = parts[1].strip() if len(parts) > 1 else "Merkez"
        
        income = p.aylik_net_gelir_tl
        fixed = p.aylik_sabit_gider_tl
        discretionary = p.aylik_serbest_harcanabilir_tl
        debt = p.borcluluk_orani * 100.0
        housing = getattr(p, 'barinma_durumu', 'Kiracı')

        # Tax Bracket & Gross calculation based on 2025/2026 Gelir Vergisi Dilimleri
        if income > 100000:
            tax_bracket = "%40 (Üst Dilim)"
            gross_income = income * 1.58
        elif income > 60000:
            tax_bracket = "%27 (Orta-Üst Dilim)"
            gross_income = income * 1.42
        elif income > 35000:
            tax_bracket = "%20 (Orta Dilim)"
            gross_income = income * 1.30
        else:
            tax_bracket = "%15 (Giriş Dilimi)"
            gross_income = income * 1.22

        rent_tl = round(income * 0.32 if housing == "Kiracı" else (income * 0.25 if housing == "Ev Sahibi (Kredili)" else 0.0), 2)

        # SEGE Tier estimation
        high_tier_districts = ["Kadıköy", "Beşiktaş", "Şişli", "Çankaya", "Bakırköy", "Nilüfer", "Muratpaşa", "Karşıyaka", "Konak", "Sarıyer"]
        sege_tier = 1 if district in high_tier_districts else (2 if city in ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"] else 3)
        archetype = "Metropol Gelişmiş İlçe" if sege_tier == 1 else ("Dinamik Şehir Merkezi / Sanayi Koridoru" if sege_tier == 2 else "Gelişmekte Olan İlçe")

        # Investment profile
        if income > 70000:
            portfolio = "Eurobond %35, Fon & BIST %35, Kripto/Döviz %30"
        elif income > 40000:
            portfolio = "Gram Altın %45, BIST Hisse %30, Döviz %25"
        else:
            portfolio = "Fiziki Çeyrek Altın & Vadeli Mevduat"

        # Bourdieu & Haidt extraction
        b = p.bourdieu_capitals or BourdieuCapitalVector(50, 50, 50, 50)
        h = p.haidt_morals or HaidtMoralProfile(50, 50, 50, 50, 50, 50)
        n = p.neuro_psych or NeuroPsychologicalState(2.25, 0.88, 0.70, 45, 50, {"O": 50, "C": 50, "E": 50, "A": 50, "N": 50})

        # Class Fraction naming
        if b.cultural_capital_score > 75 and b.economic_capital_score > 70:
            class_str = "Metropol Üst-Orta Sınıf / Kültürel Elit"
        elif b.economic_capital_score > 70:
            class_str = "Geleneksel Burjuvazi / Ticaret & Mülk Sahibi"
        elif b.cultural_capital_score > 70:
            class_str = "Yeni Orta Sınıf / Beyaz Yaka & Akademik"
        elif income < 35000:
            class_str = "Sabit Gelirli Emekçi / Prekarya"
        else:
            class_str = "Geleneksel Orta Sınıf / Esnaf & Memur"

        # Life event synthesis
        occ_l = p.meslek.lower()
        if "yazılım" in occ_l or "mühendis" in occ_l:
            life_event = "Son dönemde uzaktan çalışma modellerindeki vergilendirme ve vize randevusu bulamama stresi yaşadı."
        elif "gazi" in occ_l or "şehit" in occ_l or "asker" in occ_l:
            life_event = "Son şehitler derneği toplantısında gazilik haklarının ve devlet itibarının korunması tartışmalarına katıldı."
        elif "esnaf" in occ_l or "usta" in occ_l or "şoför" in occ_l:
            life_event = "Dükkan kirasındaki artış ve çırak/usta bulma zorluğu nedeniyle nakit akışını dengelemeye çalışıyor."
        elif "öğretmen" in occ_l or "memur" in occ_l:
            life_event = "Maaş artışının enflasyon ve market sepeti karşısında erimesi nedeniyle ek ders/bütçe planı yaptı."
        else:
            life_event = "Son aylarda artan faturalar ve temel gıda fiyatları karşısında hane bütçesini kısmak zorunda kaldı."

        return CognitiveDossier(
            kisi_id=p.id,
            ad_soyad=p.ad_soyad,
            yas=p.yas,
            cinsiyet=p.cinsiyet,
            sehir=city,
            ilce=district,
            mahalle=getattr(p, 'mahalle', 'Merkez Mah.'),
            sege_kademe=sege_tier,
            ilce_arketipi=archetype,
            meslek=p.meslek,
            egitim_seviyesi=p.egitim_durumu,
            calisma_sekli="Uzaktan (Remote)" if any(w in occ_l for w in ["yazılım", "tasarım", "çevirmen"]) else ("Saha" if any(w in occ_l for w in ["şoför", "kurye", "usta"]) else "Ofis"),
            aylik_net_gelir_tl=income,
            aylik_brut_gelir_tl=round(gross_income, 2),
            vergi_dilimi=tax_bracket,
            sgk_kategorisi="4A (Özel Sektör)" if "Memur" not in p.meslek else "4C (Kamu Emekli Sandığı)",
            barinma_durumu=housing,
            aylik_kira_veya_konut_kredisi_tl=rent_tl,
            aylik_sabit_giderler_tl=fixed,
            aylik_serbest_harcanabilir_nakit_tl=discretionary,
            borcluluk_orani_yuzde=round(debt, 1),
            findeks_kredi_notu=int(1100 + (b.economic_capital_score * 7.5)),
            yatirim_portfoy_tercihi=portfolio,
            ekonomik_sermaye_skoru=b.economic_capital_score,
            kulturel_sermaye_skoru=b.cultural_capital_score,
            sosyal_sermaye_skoru=b.social_capital_score,
            sembolik_prestij_skoru=b.symbolic_prestige_score,
            sinif_fraksiyonu=class_str,
            sefqat_zarar_karsitligi=h.care_harm,
            adalet_hakkaniyet=h.fairness_cheating,
            sadakat_grup_aidiyeti=h.loyalty_betrayal,
            otorite_hiyerarsi=h.authority_subversion,
            kutsallik_muhafazakarlik=h.sanctity_degradation,
            ozgurluk_baski_karsitligi=h.liberty_oppression,
            kayiptan_kacinma_katsayisi_lambda=n.loss_aversion_lambda,
            simdiki_zaman_onyargisi_beta=n.present_bias_beta,
            alostatik_stres_kortizol_seviyesi=n.cortisol_stress_level,
            statukoculuk_direnci=n.status_quo_inertia,
            big_five_ocean=n.big_five_ocean,
            en_buyuk_gunluk_derdi=p.en_buyuk_gunluk_derdi or "Geçim ve enflasyon baskısı",
            gizli_korkusu=p.gizli_korkusu or "Gelecek güvencesini kaybetmek",
            sosyal_statu_kaygisi=p.sosyal_statu_kaygisi or "Toplum içinde itibar kaybetmek",
            konusma_ve_jargon_tarzi=p.konusma_ve_jargon_tarzi or "Doğal sokak ve meslek Türkçesi",
            son_donemdeki_yasam_olayi=life_event
        )
