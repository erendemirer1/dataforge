"""
DataForge Municipal & Macro-Demographic Synthetic Census Polling Engine.
Simulates high-fidelity municipal and national surveys (N=100 to N=10,000)
with rigorous TÜİK NUTS-2, SEGE district socio-economic calibration,
cross-tabulations (age, gender, district, income, housing), and executive strategic recommendations.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict
from ..engine.profile_builder import ProfileBuilder
from .cognitive_persona import CognitivePersonaBuilder


@dataclass
class CensusPollRequest:
    question_or_policy: str
    city: str = "İstanbul" # "Tümü", "İstanbul", "Ankara", "İzmir", vb.
    district: Optional[str] = "Tümü" # "Kadıköy", "Esenyurt", "Tümü", vb.
    sample_size: int = 1000
    target_demographic: Optional[str] = None # "Tümü", "Kiracılar", "Gençler", "Esnaflar"
    min_age: int = 18
    max_age: int = 80


@dataclass
class CrossTabMetric:
    segment: str
    kabul_yuzde: float
    ret_yuzde: float
    kararsiz_yuzde: float
    orneklem_sayisi: int


@dataclass
class CensusPollReport:
    soru_veya_politika: str
    hedef_bolge: str
    orneklem_buyuklugu: int
    guven_araligi_yuzde_95: str
    hata_payi_yuzde: float
    genel_kabul_yuzde: float
    genel_ret_yuzde: float
    genel_kararsiz_yuzde: float
    ilce_kirilimi: list[CrossTabMetric]
    yas_grubu_kirilimi: list[CrossTabMetric]
    cinsiyet_kirilimi: list[CrossTabMetric]
    gelir_segmenti_kirilimi: list[CrossTabMetric]
    barinma_durumu_kirilimi: list[CrossTabMetric]
    en_guclu_destek_gerekceleri: list[str]
    en_buyuk_toplumsal_direnc_noktalari: list[str]
    belediye_stratejik_aksiyon_plani: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "soru_veya_politika": self.soru_veya_politika,
            "hedef_bolge": self.hedef_bolge,
            "orneklem_buyuklugu": self.orneklem_buyuklugu,
            "guven_araligi_yuzde_95": self.guven_araligi_yuzde_95,
            "hata_payi_yuzde": f"±%{self.hata_payi_yuzde:.2f}",
            "genel_kabul_yuzde": self.genel_kabul_yuzde,
            "genel_ret_yuzde": self.genel_ret_yuzde,
            "genel_kararsiz_yuzde": self.genel_kararsiz_yuzde,
            "ilce_kirilimi": [asdict(x) for x in self.ilce_kirilimi],
            "yas_grubu_kirilimi": [asdict(x) for x in self.yas_grubu_kirilimi],
            "cinsiyet_kirilimi": [asdict(x) for x in self.cinsiyet_kirilimi],
            "gelir_segmenti_kirilimi": [asdict(x) for x in self.gelir_segmenti_kirilimi],
            "barinma_durumu_kirilimi": [asdict(x) for x in self.barinma_durumu_kirilimi],
            "en_guclu_destek_gerekceleri": self.en_guclu_destek_gerekceleri,
            "en_buyuk_toplumsal_direnc_noktalari": self.en_buyuk_toplumsal_direnc_noktalari,
            "belediye_stratejik_aksiyon_plani": self.belediye_stratejik_aksiyon_plani
        }


class MunicipalCensusEngine:
    """
    Simulates high-precision quantitative public opinion polls for cities, municipalities, and institutions.
    """

    ISTANBUL_DISTRICTS = [
        "Kadıköy", "Beşiktaş", "Şişli", "Üsküdar", "Fatih", "Esenyurt", 
        "Bağcılar", "Ümraniye", "Pendik", "Maltepe", "Sarıyer", "Kartal",
        "Küçükçekmece", "Bakırköy", "Zeytinburnu", "Ataşehir", "Başakşehir", "Beylikdüzü"
    ]

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.profile_builder = ProfileBuilder(self.rng)
        self.persona_builder = CognitivePersonaBuilder(self.rng)

    def run_census_poll(
        self,
        question: str,
        city: str = "İstanbul",
        district: Optional[str] = "Tümü",
        sample_size: int = 1000,
        target_demographic: Optional[str] = None
    ) -> CensusPollReport:
        """
        Executes a quantitative synthetic census poll calibrated to Turkey / city demographics.
        """
        q_lower = question.lower()
        
        # Policy domain tags
        is_urban_transform = any(w in q_lower for w in ["kentsel dönüşüm", "deprem", "bina", "imar", "kira yardımı"])
        is_traffic_transport = any(w in q_lower for w in ["ulaşım", "metro", "otobüs", "scooter", "otopark", "yol", "trafik", "taksi", "yayalaştırma"])
        is_social_aid = any(w in q_lower for w in ["yardım", "kart", "burs", "anne", "kreş", "askıda", "halk ekmek"])
        is_tax_fee = any(w in q_lower for w in ["zam", "su faturası", "ücret", "vergi", "harç", "tarife"])

        sample_size = max(100, min(10000, sample_size))
        
        # Cross-tab accumulators
        district_counts: dict[str, dict[str, int]] = {}
        age_counts: dict[str, dict[str, int]] = {
            "18-29 (Genç)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "30-49 (Aktif Çalışan)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "50-64 (Orta Yaş)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "65+ (Emekli)": {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        gender_counts: dict[str, dict[str, int]] = {
            "Kadın": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "Erkek": {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        income_counts: dict[str, dict[str, int]] = {
            "Alt Gelir (<30k)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "Orta Gelir (30k-65k)": {"kabul": 0, "ret": 0, "kararsiz": 0},
            "Üst Gelir (>65k)": {"kabul": 0, "ret": 0, "kararsiz": 0}
        }
        housing_counts: dict[str, dict[str, int]] = {}

        total_kabul = 0
        total_ret = 0
        total_kararsiz = 0

        # Generate sample population
        for i in range(sample_size):
            p = self.profile_builder.build_profile(record_id=i + 1)
            
            # City & District override
            if city and city != "Tümü":
                p["city"] = city
                if city == "İstanbul":
                    if district and district != "Tümü":
                        p["district"] = district
                    else:
                        p["district"] = self.rng.choice(self.ISTANBUL_DISTRICTS)
            
            d_name = p.get("district", "Merkez")
            if d_name not in district_counts:
                district_counts[d_name] = {"kabul": 0, "ret": 0, "kararsiz": 0}

            age = p["age"]
            gender = p["gender"]
            income = p["monthly_income"]
            housing = p.get("housing_status", "Kiracı")
            if housing not in housing_counts:
                housing_counts[housing] = {"kabul": 0, "ret": 0, "kararsiz": 0}
            
            # Mathematical Decision Engine calibrated to sociological variables
            score = 0.0
            
            if is_urban_transform:
                if housing == "Kiracı":
                    score += 20.0 if "kira yardımı" in q_lower else -15.0 # Kiracı tahliye korkusu
                else: # Ev sahibi
                    score += 35.0 # Evini yeniletmek ister
                if d_name in ["Kadıköy", "Beşiktaş", "Bakırköy", "Avcılar"]: # Deprem kaygısı yüksek
                    score += 25.0
                if income < 35000:
                    score -= 20.0 # Ek borçlanma kaygısı

            elif is_traffic_transport:
                if "scooter" in q_lower or "yayalaştırma" in q_lower:
                    if age <= 30:
                        score += 40.0 # Gençler mobilite sever
                    else:
                        score -= 25.0 # Yaşlılar kaldırımda scooter istemez
                    if d_name in ["Kadıköy", "Beşiktaş", "Şişli"]:
                        score += 30.0
                else: # Toplu taşıma / zam
                    if income < 35000:
                        score -= 30.0 if "zam" in q_lower else 35.0

            elif is_social_aid:
                if income < 35000 or housing == "Kiracı":
                    score += 55.0 # Dar gelirli sosyal desteği güçlü destekler
                else:
                    score += 15.0 # Üst gelir de sosyal yardıma prensipte olumlu

            elif is_tax_fee:
                if income < 45000:
                    score -= 50.0 # Zam ve vergiye mutlak ret
                else:
                    score -= 25.0
            else:
                # General Policy
                score += (income / 1000.0) * 0.2
                if age < 35:
                    score += 10.0

            # Noise / Individual idiosyncrasy
            noise = self.rng.gauss(0, 20.0)
            final_eval = score + noise

            if final_eval > 10.0:
                verdict = "kabul"
                total_kabul += 1
            elif final_eval < -10.0:
                verdict = "ret"
                total_ret += 1
            else:
                verdict = "kararsiz"
                total_kararsiz += 1

            # Accumulate
            district_counts[d_name][verdict] += 1

            # Age group
            if age < 30:
                age_counts["18-29 (Genç)"][verdict] += 1
            elif age < 50:
                age_counts["30-49 (Aktif Çalışan)"][verdict] += 1
            elif age < 65:
                age_counts["50-64 (Orta Yaş)"][verdict] += 1
            else:
                age_counts["65+ (Emekli)"][verdict] += 1

            gender_counts[gender][verdict] += 1
            housing_counts[housing][verdict] += 1

            if income < 30000:
                income_counts["Alt Gelir (<30k)"][verdict] += 1
            elif income < 65000:
                income_counts["Orta Gelir (30k-65k)"][verdict] += 1
            else:
                income_counts["Üst Gelir (>65k)"][verdict] += 1

        # Calculate Percentages & Confidence Interval
        kabul_pct = round((total_kabul / sample_size) * 100, 1)
        ret_pct = round((total_ret / sample_size) * 100, 1)
        kararsiz_pct = round((total_kararsiz / sample_size) * 100, 1)
        
        # Standard error for proportion: sqrt(p * (1-p) / N) * 1.96
        p_hat = kabul_pct / 100.0
        margin_of_error = round(1.96 * math.sqrt((p_hat * (1 - p_hat)) / max(1, sample_size)) * 100, 2)
        ci_lower = max(0.0, round(kabul_pct - margin_of_error, 1))
        ci_upper = min(100.0, round(kabul_pct + margin_of_error, 1))
        ci_str = f"%{ci_lower} - %{ci_upper}"

        def build_crosstab_list(d: dict[str, dict[str, int]]) -> list[CrossTabMetric]:
            res = []
            for seg, counts in d.items():
                tot = sum(counts.values())
                if tot > 0:
                    res.append(CrossTabMetric(
                        segment=seg,
                        kabul_yuzde=round((counts["kabul"] / tot) * 100, 1),
                        ret_yuzde=round((counts["ret"] / tot) * 100, 1),
                        kararsiz_yuzde=round((counts["kararsiz"] / tot) * 100, 1),
                        orneklem_sayisi=tot
                    ))
            return res

        # Drivers & Resistance
        if is_urban_transform:
            destek = ["Can güvenliği ve deprem riskini minimize etme arzusu", "Mülk değerinin ve yaşam kalitesinin artması", "Kira yardımlarıyla geçiş sürecinin güvenceye alınması"]
            direnc = ["Kiracıların dönüşüm sonrası bölgeden tahliye edilme ve fahiş kira korkusu", "Mülk sahiplerinin ek inşaat maliyeti ve müteahhit güvensizliği", "Bürokratik süreçlerin ve onayların yıllarca uzaması endişesi"]
            action = "Belediye müteahhit ile vatandaş arasında 'garantör kamu hakemi' olmalı ve kiracılara rezerv konut tahsis güvencesi sunulmalıdır."
        elif is_traffic_transport:
            destek = ["Trafik keşmekeşini azaltma ve toplu ulaşım konforu", "Genç nüfusun mikro-mobilite ve bisiklet/yaya yolu talebi", "Ulaşım maliyetlerinde tasarruf"]
            direnc = ["Kaldırımlarda yaya güvenliğinin tehlikeye girmesi", "Esnafın araçla yük indirme-bindirme zorluğu çekmesi", "Toplu taşıma ücret artışlarına dar gelirlinin mutlak tepkisi"]
            action = "Yayalaştırma projelerinde esnaf için özel lojistik saatleri belirlenmeli, scooter ve mikro araçlar için ayrılmış hız limitli şeritler zorunlu tutulmalıdır."
        elif is_social_aid:
            destek = ["Derin mutfak yoksulluğuna ve dar gelirliye doğrudan nefes aldırma", "Sosyal adaletin ve dayanışmanın güçlenmesi", "Kadın ve çocuk odaklı temel gıda güvencesi"]
            direnc = ["Yardımların partizanlık veya liyakatsiz dağıtılma şüphesi", "Vergilerin etkin kullanılmadığı düşüncesi"]
            action = "Sosyal yardımlar doğrudan açık ve şeffaf dijital kent kartlarına yüklenmeli, mahalle bakkallarıyla entegre edilerek yerel esnaf da desteklenmelidir."
        else:
            destek = ["Hizmet kalitesinin artırılması beklentisi", "Şeffaf ve hesap verebilir belediyecilik vizyonu"]
            direnc = ["Ekonomik külfet ve yaşam alanına müdahale endişesi", "Halkın fikrinin yeterince alınmadığı hissi"]
            action = "Mahalle bazlı katılımcı bütçe toplantıları yapılmalı ve pilot uygulamalarla halkın güveni test edilmelidir."

        target_str = f"{city}" + (f" / {district}" if district and district != "Tümü" else " (Tüm İlçeler)")

        return CensusPollReport(
            soru_veya_politika=question,
            hedef_bolge=target_str,
            orneklem_buyuklugu=sample_size,
            guven_araligi_yuzde_95=ci_str,
            hata_payi_yuzde=margin_of_error,
            genel_kabul_yuzde=kabul_pct,
            genel_ret_yuzde=ret_pct,
            genel_kararsiz_yuzde=kararsiz_pct,
            ilce_kirilimi=build_crosstab_list(district_counts),
            yas_grubu_kirilimi=build_crosstab_list(age_counts),
            cinsiyet_kirilimi=build_crosstab_list(gender_counts),
            gelir_segmenti_kirilimi=build_crosstab_list(income_counts),
            barinma_durumu_kirilimi=build_crosstab_list(housing_counts),
            en_guclu_destek_gerekceleri=destek,
            en_buyuk_toplumsal_direnc_noktalari=direnc,
            belediye_stratejik_aksiyon_plani=action
        )
