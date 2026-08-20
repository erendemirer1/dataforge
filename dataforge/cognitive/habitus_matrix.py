"""
DataForge Sociological Habitus & Moral Foundations Matrix.
Based on Pierre Bourdieu's Theory of Capital (Economic, Cultural, Social Capital)
and Jonathan Haidt's Moral Foundations Theory tailored to Turkish Sociology.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class MoralFoundations:
    care_vs_harm: float            # Merhamet & Zarar Vermeme (0-100)
    fairness_vs_cheating: float    # Adalet & Kul Hakkı Hassasiyeti (0-100)
    loyalty_vs_betrayal: float     # Sadakat & Hemşehri/Grup Dayanışması (0-100)
    authority_vs_subversion: float # Otoriteye / Hiyerarşiye Saygı (0-100)
    sanctity_vs_degradation: float # Kutsallık / Mahremiyet / Helal-Haram (0-100)
    liberty_vs_oppression: float   # Bireysel Özgürlük & Özerklik (0-100)


@dataclass
class SociologicalHabitus:
    social_class_stratum: str      # Prekarya, Geleneksel Esnaf/KOBİ, Yeni Orta Sınıf (Beyaz Yaka), Üst Burjuvazi
    upbringing_environment: str    # Taşra Muhafazakar, Metropol Seküler, Gecekondu/Varoş, Anadolu Ticaret Ailesi, Memur Ailesi
    cultural_capital_score: float  # Kültürel Sermaye (0-100)
    social_capital_score: float    # Sosyal Ağ Gücü & Nüfuz (0-100)
    economic_capital_score: float  # Mülkiyet & Varlık Gücü (0-100)
    inherited_wealth_status: str   # Sıfırdan Tırnaklarıyla, Aileden Mülklü/Dükkanlı, Miraslı Zengin, Borçlu Aile
    reference_group: str           # Mahalle Cemaati, Plaza Ağı, Hemşehri Derneği, Akademik Çevre, Sanayi Loncası
    consumption_aesthetic: str     # Gösterişçi Tüketim (Veblen), Faydacı/Tasarrufçu, Deneyim/Statü Odaklı, Minimalist Zorunluluk
    moral_foundations: MoralFoundations


class HabitusEngine:
    """Calculates empirical sociological habitus based on city, district tier, education, age, and occupation."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def derive_habitus(
        self,
        city: str,
        district: str,
        occupation: str,
        education_level: str,
        income_tl: float,
        age: int
    ) -> SociologicalHabitus:
        """Derives mutually-coherent sociological habitus and moral values for a Turkish citizen."""
        occ_lower = occupation.lower()
        edu_lower = education_level.lower()

        # 1. Class Stratum Determination
        if any(w in occ_lower for w in ["holding", "yatırımcı", "şirket ortağı", "armatör", "büyükelçi", "ceo", "direktör"]):
            social_class = "Üst Burjuvazi (Elit / Sermaye Sahibi)"
            inherited = self.rng.choices(["Aileden Sanayici/Köklü Zengin", "Miraslı Gayrimenkul Zengini", "Yeni Dönem Girişimci"], weights=[0.5, 0.3, 0.2])[0]
            consumption = "Statü ve Lüks Odaklı (Veblen Tüketimi)"
            cult_cap = round(self.rng.uniform(75, 98), 1)
            soc_cap = round(self.rng.uniform(80, 99), 1)
            econ_cap = round(self.rng.uniform(85, 99), 1)
            upbringing = self.rng.choice(["Metropol Köklü Aile", "Büyükşehir Seküler Üst-Orta"])
            ref_group = "İş Dünyası & Kulüp Ağları (TÜSİAD/Yat Kulüpleri)"

        elif any(w in occ_lower for w in ["yazılım", "mühendis", "doktor", "avukat", "akademisyen", "pazarlama müdürü", "mimar", "finans analisti"]):
            social_class = "Yeni Orta Sınıf (Kentli Beyaz Yaka)"
            inherited = self.rng.choices(["Memur Ailesi Çocuğu", "Anadolu'dan Okumaya Gelmiş", "Aileden Daire Sahibi"], weights=[0.4, 0.35, 0.25])[0]
            consumption = "Deneyim, Kültür ve Marka Odaklı"
            cult_cap = round(self.rng.uniform(70, 92), 1)
            soc_cap = round(self.rng.uniform(55, 80), 1)
            econ_cap = round(self.rng.uniform(45, 75), 1)
            upbringing = self.rng.choice(["Memur / Öğretmen Çocuğu", "Metropol Orta Sınıf", "Anadolu İl Merkezi"])
            ref_group = "Plaza & LinkedIn Çevresi, Üniversite Mezunlar Derneği"

        elif any(w in occ_lower for w in ["bakkal", "kasap", "kuaför", "tamirci", "usta", "taksici", "esnaf", "kuyumcu", "nakliyeci", "muhtar"]):
            social_class = "Geleneksel Küçük Burjuvazi (Esnaf & Zanaatkar)"
            inherited = self.rng.choices(["Babadan Kalma Dükkan/Tezgah", "Çıraklıktan Yetişme", "Köyden Göçle Kurulan İş"], weights=[0.45, 0.35, 0.20])[0]
            consumption = "Faydacı, Nakit Koruyucu ve Dayanıklı Mal Odaklı"
            cult_cap = round(self.rng.uniform(25, 55), 1)
            soc_cap = round(self.rng.uniform(70, 95), 1) # Esnafın sosyal/hemşehri ağı çok güçlüdür
            econ_cap = round(self.rng.uniform(40, 75), 1)
            upbringing = self.rng.choice(["Sanayi / Çarşı Çıraklık Çevresi", "Taşra Muhafazakar Esnaf Ailesi", "Kırsal/Köy Kökenli"])
            ref_group = "Sanayi Sitesi / Esnaf Odası / Hemşehri Derneği / Cami Cemaati"

        elif any(w in occ_lower for w in ["öğretmen", "hemşire", "zabıta", "polis", "memur", "astsubay", "katip"]):
            social_class = "Klasik Kamu Orta Sınıfı (Maaşlı Memur)"
            inherited = self.rng.choices(["Memur Ailesi Geleneği", "Köyden KPSS ile Atanan", "Dar Gelirli İşçi Ailesi"], weights=[0.4, 0.4, 0.2])[0]
            consumption = "Tutumlu, Garanti Odaklı ve Fiyat-Performansçı"
            cult_cap = round(self.rng.uniform(55, 78), 1)
            soc_cap = round(self.rng.uniform(45, 70), 1)
            econ_cap = round(self.rng.uniform(30, 55), 1)
            upbringing = self.rng.choice(["Anadolu Memur Çevresi", "Lojman Kültürü ile Büyüme", "Taşra Kasabası"])
            ref_group = "Kamu Kurumu Çalışma Arkadaşları & Sendika"

        else: # Prekarya / Günübirlik / Hizmet sektörü
            social_class = "Prekarya (Güvencesiz / Esnek Emek)"
            inherited = "Miras Yok / Aileye Maddi Destek Sağlamak Zorunda"
            consumption = "Zorunlu İhtiyaç Odaklı (En Ucuz Market/İndirim)"
            cult_cap = round(self.rng.uniform(20, 50), 1)
            soc_cap = round(self.rng.uniform(30, 60), 1)
            econ_cap = round(self.rng.uniform(10, 35), 1)
            upbringing = self.rng.choice(["Varoş / Gecekondu Çevresi", "Mevsimlik Göç Eden Aile", "Kırsal Köy"])
            ref_group = "Mahalle Kahvehanesi / Akraba Ağı"

        # 2. Moral Foundations Calculation (Jonathan Haidt Dimensions)
        is_conservative_upbringing = "Muhafazakar" in upbringing or "Sanayi" in upbringing or "Taşra" in upbringing
        is_secular_metro = "Metropol Seküler" in upbringing or "Plaza" in ref_group

        if is_conservative_upbringing:
            care = round(self.rng.uniform(55, 80), 1)
            fairness = round(self.rng.uniform(70, 95), 1)  # Kul hakkı çok yüksek
            loyalty = round(self.rng.uniform(75, 98), 1)   # Hemşehri ve millet bağı çok yüksek
            authority = round(self.rng.uniform(75, 95), 1) # Büyüğe ve devlete saygı
            sanctity = round(self.rng.uniform(75, 99), 1)  # Helal-haram ve mahremiyet zirve
            liberty = round(self.rng.uniform(30, 60), 1)   # Bireysel özgürlük arka planda
        elif is_secular_metro:
            care = round(self.rng.uniform(70, 95), 1)      # İnsan hakları ve hayvan hakları yüksek
            fairness = round(self.rng.uniform(75, 95), 1)  # Hukuk ve liyakat odaklı adalet
            loyalty = round(self.rng.uniform(35, 65), 1)   # Grup baskısına direnç
            authority = round(self.rng.uniform(25, 55), 1) # Otoriteyi sorgulama eğilimi
            sanctity = round(self.rng.uniform(20, 50), 1)  # Geleneksel tabular düşük
            liberty = round(self.rng.uniform(80, 99), 1)   # Kişisel özgürlük ve özerklik zirve
        else:
            care = round(self.rng.uniform(60, 85), 1)
            fairness = round(self.rng.uniform(65, 88), 1)
            loyalty = round(self.rng.uniform(60, 85), 1)
            authority = round(self.rng.uniform(55, 80), 1)
            sanctity = round(self.rng.uniform(50, 80), 1)
            liberty = round(self.rng.uniform(50, 80), 1)

        morals = MoralFoundations(
            care_vs_harm=care,
            fairness_vs_cheating=fairness,
            loyalty_vs_betrayal=loyalty,
            authority_vs_subversion=authority,
            sanctity_vs_degradation=sanctity,
            liberty_vs_oppression=liberty
        )

        return SociologicalHabitus(
            social_class_stratum=social_class,
            upbringing_environment=upbringing,
            cultural_capital_score=cult_cap,
            social_capital_score=soc_cap,
            economic_capital_score=econ_cap,
            inherited_wealth_status=inherited,
            reference_group=ref_group,
            consumption_aesthetic=consumption,
            moral_foundations=morals
        )
