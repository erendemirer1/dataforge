"""
DataForge Municipal & Macro-Demographic Synthetic Census Polling Engine.
Simulates high-fidelity municipal and national surveys (N=100 to N=10,000)
with rigorous TÜİK NUTS-2, SEGE district socio-economic calibration,
cross-tabulations (age, gender, district, income, housing), individual citizen ballots,
and executive strategic recommendations.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict
from ..engine.profile_builder import ProfileBuilder
from .cognitive_persona import CognitivePersonaBuilder


@dataclass
class CitizenBallot:
    citizen_id: int
    ad_soyad: str
    yas: int
    cinsiyet: str
    sehir_ilce: str
    mahalle: str
    meslek: str
    egitim_durumu: str
    aylik_net_gelir_tl: float
    barinma_durumu: str # "Kiracı", "Ev Sahibi", "Aile Evi", "Lojman"
    karar: str # "Kabul Eder / Destekler", "Kesinlikle Reddeder", "Kararsız / Çekimser"
    bireysel_dusuncesi_ve_gerekcesi: str


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
    bireysel_oylar: list[CitizenBallot]

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
            "belediye_stratejik_aksiyon_plani": self.belediye_stratejik_aksiyon_plani,
            "bireysel_oylar": [asdict(b) for b in self.bireysel_oylar]
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

    def _generate_citizen_thought(
        self,
        q_lower: str,
        verdict: str,
        age: int,
        occupation: str,
        income: float,
        housing: str,
        district: str
    ) -> str:
        """Generates authentic, specific Turkish reasoning for this individual citizen."""
        occ_l = occupation.lower()

        # 1. URBAN TRANSFORMATION & RENT SUPPORT
        if any(w in q_lower for w in ["kentsel dönüşüm", "deprem", "bina", "kira yardımı", "imar"]):
            if verdict == "kabul":
                if housing == "Kiracı":
                    if income < 35000:
                        return f"{district}'de 35 yıllık riskli binada kiracıyım. 20.000 TL kira desteği olmadan başka yere taşınmamız imkansızdı, taşınma ve depozito masraflarını karşılamamız için hayati bir destek."
                    else:
                        return f"Mevcut kira fiyatları uçmuşken dönüşüm sürecinde kiracının korunması binanın tahliyesini hızlandırır, dönüşümün önündeki en büyük tıkanıklığı çözer."
                else: # Ev sahibi
                    if age >= 55:
                        return f"Emekli maaşımla binayı yeniletirken geçici kiralık ev tutmak beni batırırdı. 20.000 TL kira yardımı olursa binanın yıkılıp yapılmasına hemen onay veririm."
                    else:
                        return f"Deprem riski her an kapıda, can güvenliğimiz her şeyden önemli. Kira desteği kiracıların tahliyeyi geciktirmesini önler ve inşaat hemen başlar."
            elif verdict == "ret":
                if housing == "Kiracı":
                    return f"{district}'de 20.000 TL'ye oturulacak 2+1 ev kalmadı ki! Bu para sadece yetersiz bir pansuman, evden çıkarıldıktan sonra geri dönememe korkusu yaşıyoruz."
                else: # Ev sahibi
                    return f"Kira yardımı kiracıya veriliyor ama müteahhit inşaat farkı olarak bizden daire başı 2 milyon TL istiyor! Emekli halimle bu borcu nasıl ödeyeceğim? Asıl finansman sorununa çözüm yok."
            else: # Kararsız
                return f"Fikir kağıt üzerinde güzel ama belediye bu bütçeyi tüm hak sahiplerine 18 ay boyunca aksatmadan ödeyebilecek mi? Müteahhit batarsa ortada kalma riski var."

        # 2. POLITICS & LEADERSHIP
        elif any(w in q_lower for w in ["erdoğan", "tayyip", "başkan", "seçim", "hükümet", "akp", "chp"]):
            if verdict == "kabul":
                return f"Etrafımızdaki jeopolitik krizler ve savaş ortamında devleti maceraya atamayız. Geçim zor ama karşımızda tecrübeli ve kriz yönetebilen bir lider var."
            elif verdict == "ret":
                return f"Pazara çıktığımda iki poşet erzak 1000 lira olmuşken, gençler asgari ücrete mahkumken artık köklü bir değişim ve liyakat şart."
            else:
                return f"Hayat pahalılığı can yakıyor ama muhalefetin de güven veren bir ekonomik programı yok, iki arada bir derede kaldım."

        # 3. TRANSPORT & SCOOTERS
        elif any(w in q_lower for w in ["scooter", "martı", "yayalaştırma", "kaldırım", "trafik", "otopark"]):
            if verdict == "kabul":
                if "yasak" in q_lower:
                    return f"Kaldırımlarda çoluk çocuk yürüyemez olduk, her köşeden hızla fırlıyorlar. Yayaların güvenliği için caddelerden ve kaldırımlardan temizlenmeli."
                else:
                    return f"{district} trafiğinde araba kullanmak imkansız; toplu taşımaya ve mikro mobiliteye yatırım yapılması şart."
            elif verdict == "ret":
                if "yasak" in q_lower:
                    return f"Gençler ve çalışanlar için metroya ulaşmanın en hızlı yolu bu. Yasaklamak yerine bisiklet ve scooter yolları yapılsın."
                else:
                    return f"Trafik yoğunluğunu daha da artırır, esnafın mal indirmesini engeller."
            else:
                return f"Tamamen yasaklamak çağdışı olur ama hız sınırı ve düzgün park alanları zorunlu tutulmalı."

        # 4. NIGHTLIFE & BEER & CAFES
        elif any(w in q_lower for w in ["bira", "bar", "pub", "mekan", "kahve"]):
            if verdict == "kabul":
                return f"{district}'de dışarıda oturup sosyalleşmek ateş pahası oldu. Uygun fiyatlı ve kaliteli bir alternatif olursa her hafta sonu arkadaşlarla gideriz."
            elif verdict == "ret":
                return f"Bu devirde o fiyata kaliteli ürün ve nezih ortam sunulamaz; aşırı kalabalık ve gürültü olur."
            else:
                return f"Fiyat cazip ama mekanın müzik tarzını, ortamını ve hizmet kalitesini görmeden peşin karar veremem."

        # 5. GENERAL MUNICIPAL / PUBLIC POLICY
        else:
            if verdict == "kabul":
                return f"Mevcut şartlar altında kamu yararı taşıyan ve vatandaşın yaşam standardını doğrudan iyileştirecek mantıklı bir adım."
            elif verdict == "ret":
                return f"Bütçe ve uygulama gerçekleriyle uyuşmuyor; yerel halkın gerçek önceliklerine hitap etmeyen yapay bir harcama kalemi."
            else:
                return f"Projenin finansman modeli ve vatandaşa yansıyacak ek külfetler netleşmeden kesin bir kanaat oluşturmak güç."

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
        is_politics = any(w in q_lower for w in ["erdoğan", "tayyip", "başkan", "seçim", "hükümet", "akp", "chp", "aday"])
        is_social_aid = any(w in q_lower for w in ["yardım", "kart", "burs", "anne", "kreş", "askıda", "halk ekmek"])
        is_tax_fee = any(w in q_lower for w in ["zam", "su faturası", "ücret", "vergi", "harç", "tarife"])

        sample_size = max(50, min(10000, sample_size))
        
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
        citizen_ballots: list[CitizenBallot] = []

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
            occupation = p.get("occupation", "Vatandaş")
            if housing not in housing_counts:
                housing_counts[housing] = {"kabul": 0, "ret": 0, "kararsiz": 0}
            
            # Mathematical Decision Engine calibrated to sociological variables with authentic variance
            score = 0.0
            
            if is_urban_transform:
                if housing == "Kiracı":
                    # Tenants support rent aid strongly, but low income fear displacement
                    score += 25.0 if "kira yardımı" in q_lower else -10.0
                else: # Ev sahibi
                    if income < 35000 or age >= 58:
                        # Retired homeowners fear high construction debt to contractors
                        score -= 15.0
                    else:
                        # Wealthier homeowners want earthquake renewal
                        score += 20.0
                if d_name in ["Kadıköy", "Beşiktaş", "Bakırköy", "Avcılar"]:
                    score += 15.0 # High earthquake sensitivity

            elif is_politics:
                # Political cleavage calibrated with Turkish demographic indices
                if income < 32000 or age <= 28:
                    score -= 30.0 # High economic pain & youth discontent
                elif age >= 52 and income >= 35000:
                    score += 25.0 # Traditional stability preference
                else:
                    score += self.rng.uniform(-20.0, 20.0)

            elif is_traffic_transport:
                if "scooter" in q_lower or "yayalaştırma" in q_lower:
                    if age <= 30:
                        score += 35.0 if "yasak" not in q_lower else -35.0
                    else:
                        score += -30.0 if "yasak" not in q_lower else 35.0
                else: # Toplu taşıma / zam
                    if income < 35000:
                        score -= 40.0 if "zam" in q_lower else 30.0

            elif is_social_aid:
                if income < 35000 or housing == "Kiracı":
                    score += 45.0
                else:
                    score += 10.0

            elif is_tax_fee:
                score -= 45.0 if income < 45000 else -20.0

            else:
                score += (income / 2000.0) - 15.0 + self.rng.uniform(-15.0, 15.0)

            # Idiosyncratic Gaussian Noise
            noise = self.rng.gauss(0, 28.0)
            final_eval = score + noise

            if final_eval > 12.0:
                verdict = "kabul"
                karar_str = "Kabul Eder / Destekler"
                total_kabul += 1
            elif final_eval < -12.0:
                verdict = "ret"
                karar_str = "Kesinlikle Reddeder"
                total_ret += 1
            else:
                verdict = "kararsiz"
                karar_str = "Kararsız / Çekimser"
                total_kararsiz += 1

            # Individual citizen rationale in Turkish
            thought = self._generate_citizen_thought(
                q_lower=q_lower,
                verdict=verdict,
                age=age,
                occupation=occupation,
                income=income,
                housing=housing,
                district=d_name
            )

            # Record citizen ballot
            citizen_ballots.append(CitizenBallot(
                citizen_id=i + 1,
                ad_soyad=f"{p['first_name']} {p['last_name']}",
                yas=age,
                cinsiyet=gender,
                sehir_ilce=f"{p['city']} / {d_name}",
                mahalle=p.get("neighborhood", "Merkez Mah."),
                meslek=occupation,
                egitim_durumu=p.get("education_level", "Lise"),
                aylik_net_gelir_tl=income,
                barinma_durumu=housing,
                karar=karar_str,
                bireysel_dusuncesi_ve_gerekcesi=thought
            ))

            # Accumulate cross-tabs
            district_counts[d_name][verdict] += 1

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
        
        p_hat = kabul_pct / 100.0
        margin_of_error = round(1.96 * math.sqrt(max(0.0001, (p_hat * (1 - p_hat)) / max(1, sample_size))) * 100, 2)
        ci_lower = max(0.0, round(kabul_pct - margin_of_error, 1))
        ci_upper = min(100.0, round(kabul_pct + margin_of_error, 1))
        ci_str = f"%{ci_lower} - %{ci_upper}"

        # Build CrossTab Metrics
        def _to_metric_list(d: dict[str, dict[str, int]]) -> list[CrossTabMetric]:
            res = []
            for seg, counts in d.items():
                tot = sum(counts.values())
                if tot == 0:
                    continue
                res.append(CrossTabMetric(
                    segment=seg,
                    kabul_yuzde=round((counts["kabul"] / tot) * 100, 1),
                    ret_yuzde=round((counts["ret"] / tot) * 100, 1),
                    kararsiz_yuzde=round((counts["kararsiz"] / tot) * 100, 1),
                    orneklem_sayisi=tot
                ))
            return res

        district_metrics = _to_metric_list(district_counts)
        age_metrics = _to_metric_list(age_counts)
        gender_metrics = _to_metric_list(gender_counts)
        income_metrics = _to_metric_list(income_counts)
        housing_metrics = _to_metric_list(housing_counts)

        # Strategic Action & Barriers
        if is_urban_transform:
            drivers = [
                "Deprem Riskli Binaların Hızlı Tahliye Edilebilmesi",
                "Kira Artışları Karşısında Kiracıların Mağduriyetinin Önlenmesi",
                "Hak Sahiplerinin Taşınma ve Yerleşme Maliyetlerinin Karşılanması"
            ]
            barriers = [
                "Müteahhit İnşaat Farkı Borçlanma Korkusu (Özellikle Emeklilerde)",
                "Belediye Kira Yardımı Sürekliliğine ve Bütçesine Yönelik Şüpheler",
                "Dönüşüm Sonrası Eski Mahalleye Geri Dönememe ve Ayrışma Kaygısı"
            ]
            action = "Belediye müteahhit ile hak sahipleri arasında 'garantör kamu hakemi' olmalı, sabit gelirli emeklilere sıfır faizli yapım kredisi ve kiracılara rezerv konut tahsis güvencesi sunmalıdır."
        elif is_politics:
            drivers = [
                "Jeopolitik Kriz Ortamında Devlet Liderliği ve İstikrar Arayışı",
                "Savunma Sanayii ve Güvenlik Politikalarına Duyulan Güven",
                "Geleneksel Siyasi Aidiyet ve Taban Sadakati"
            ]
            barriers = [
                "Mutfak Enflasyonu ve Emekli/Sabit Gelirlinin Alım Gücü Kaybı",
                "Liyakat Erozyonu ve Kurumsal Güvensizlik",
                "Genç Kuşakta Gelecek ve İstihdam Umutsuzluğu"
            ]
            action = "Mutfaktaki reel hayat pahalılığına doğrudan can suyu olacak gelir politikaları geliştirilmeli ve gençlere şeffaf kariyer güvencesi verilmelidir."
        elif is_traffic_transport:
            drivers = [
                "Kaldırım ve Yaya Güvenliğinin Sağlanması",
                "Toplu Taşımayla Entegre Trafik Akışının Rahatlatılması",
                "Gürültü ve Düzensiz Park Kirliliğinin Önlenmesi"
            ]
            barriers = [
                "Son Kilometre (Last-Mile) Hızlı Ulaşım Alternatifinin Kısıtlanması",
                "Genç Çalışanlar ve Kuryelerin Zaman Kaybı",
                "Altyapı Yetersizliği ve Özel Şerit Eksikliği"
            ]
            action = "Toptan yasaklama yerine mikro mobilite araçlarına hız limiti (15 km/s) ve zorunlu ayrılmış park cepleri tahsis edilmelidir."
        else:
            drivers = [
                "Halkın Doğrudan Yaşam Standartlarını İyileştirme Potansiyeli",
                "Şeffaf ve Öngörülebilir Kamu Yönetimi",
                "Ekonomik Kolaylık ve Erişilebilirlik"
            ]
            barriers = [
                "Finansman ve Bütçe Yetersizliği Endişesi",
                "Uygulama Sürecinde Bürokratik Tıkanıklıklar",
                "Yerel Katılım ve Ön Danışma Eksikliği"
            ]
            action = "Şeffaf yerel bilgilendirme toplantıları düzenlenmeli ve kademeli pilot uygulama modeli tercih edilmelidir."

        target_area = f"{city}" + (f" ({district})" if district and district != "Tümü" else " (Tüm İlçeler)")

        return CensusPollReport(
            soru_veya_politika=question,
            hedef_bolge=target_area,
            orneklem_buyuklugu=sample_size,
            guven_araligi_yuzde_95=ci_str,
            hata_payi_yuzde=margin_of_error,
            genel_kabul_yuzde=kabul_pct,
            genel_ret_yuzde=ret_pct,
            genel_kararsiz_yuzde=kararsiz_pct,
            ilce_kirilimi=district_metrics,
            yas_grubu_kirilimi=age_metrics,
            cinsiyet_kirilimi=gender_metrics,
            gelir_segmenti_kirilimi=income_metrics,
            barinma_durumu_kirilimi=housing_metrics,
            en_guclu_destek_gerekceleri=drivers,
            en_buyuk_toplumsal_direnc_noktalari=barriers,
            belediye_stratejik_aksiyon_plani=action,
            bireysel_oylar=citizen_ballots
        )
