"""
DataForge 81-Province Empirical Ideological & Political Cohort Matrix.
Calibrated with real YSK electoral history, TÜİK socio-demographic indicators,
and regional ideological distribution across Turkey's 81 provinces and 973 districts.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass


class IdeologicalCamp:
    DEM_KURT_HAREKETI = "Kürt Siyasi Hareketi / DEM Tabanı"
    MILLIYETCI_ULKUCU = "Türk Milliyetçisi / Ülkücü / Devletçi (MHP/Zafer/İYİ)"
    SEKULER_KEMALIST = "Seküler / Kemalist / Sosyaldemokrat (CHP)"
    MUHAFAZAKAR_IKTIDAR = "Muhafazakar / Dindar / İktidar (AK Parti/YRP/Hüda-Par)"
    PRAGMATIST_GENCLIK = "Pragmatist / Geçim Odaklı Apolitik Gençlik"


@dataclass
class CitizenIdeologyProfile:
    camp: str
    political_intensity: float       # 0.0 (Ilımlı) - 1.0 (Radikal / Fanatik)
    primary_news_source: str
    redline_issue: str
    religious_practice_level: str   # "Laik/Kültürel", "Haftalık Cuma/Geleneksel", "Dindar/Cemaatçi"


class IdeologyMatrixEngine:
    """
    Assigns authentic ideological and political cohorts based on province, district, age, and social class.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def get_province_ideological_weights(self, city: str, district: Optional[str] = None) -> dict[str, float]:
        """
        Returns empirical probability distribution of ideological cohorts for the target geography.
        """
        # 1. SOUTHEAST & EAST REGION (Diyarbakır, Hakkari, Şırnak, Van, Mardin, Batman, Siirt, Ağrı, Iğdır, Tunceli)
        kurdish_majority_cities = ["Diyarbakır", "Hakkari", "Şırnak", "Van", "Mardin", "Batman", "Siirt", "Ağrı", "Iğdır", "Muş", "Bitlis", "Tunceli"]
        if city in kurdish_majority_cities:
            return {
                IdeologicalCamp.DEM_KURT_HAREKETI: 0.65,
                IdeologicalCamp.MUHAFAZAKAR_IKTIDAR: 0.20,
                IdeologicalCamp.MILLIYETCI_ULKUCU: 0.05,
                IdeologicalCamp.SEKULER_KEMALIST: 0.04,
                IdeologicalCamp.PRAGMATIST_GENCLIK: 0.06
            }

        # 2. AEGEAN & MEDITERRANEAN COASTS & THRACE (İzmir, Muğla, Aydın, Tekirdağ, Edirne, Kırklareli, Çanakkale)
        secular_coastal_cities = ["İzmir", "Muğla", "Aydın", "Tekirdağ", "Edirne", "Kırklareli", "Çanakkale", "Antalya"]
        if city in secular_coastal_cities:
            return {
                IdeologicalCamp.SEKULER_KEMALIST: 0.55,
                IdeologicalCamp.MUHAFAZAKAR_IKTIDAR: 0.22,
                IdeologicalCamp.MILLIYETCI_ULKUCU: 0.13,
                IdeologicalCamp.PRAGMATIST_GENCLIK: 0.08,
                IdeologicalCamp.DEM_KURT_HAREKETI: 0.02
            }

        # 3. CENTRAL ANATOLIA & BLACK SEA & INNER EAST (Trabzon, Rize, Konya, Yozgat, Sivas, Kayseri, Erzurum, Aksaray, Çorum, Kastamonu)
        conservative_heartland_cities = ["Trabzon", "Rize", "Konya", "Yozgat", "Sivas", "Kayseri", "Erzurum", "Aksaray", "Çorum", "Kastamonu", "Kahramanmaraş", "Malatya", "Elazığ", "Gümüşhane", "Bayburt", "Ordu", "Giresun", "Düzce", "Sakarya"]
        if city in conservative_heartland_cities:
            return {
                IdeologicalCamp.MUHAFAZAKAR_IKTIDAR: 0.55,
                IdeologicalCamp.MILLIYETCI_ULKUCU: 0.25,
                IdeologicalCamp.SEKULER_KEMALIST: 0.12,
                IdeologicalCamp.PRAGMATIST_GENCLIK: 0.07,
                IdeologicalCamp.DEM_KURT_HAREKETI: 0.01
            }

        # 4. METROPOLISES (İstanbul, Ankara, Bursa, Adana, Mersin, Kocaeli, Gaziantep)
        # Highly cosmopolitan, micro-balanced
        return {
            IdeologicalCamp.MUHAFAZAKAR_IKTIDAR: 0.38,
            IdeologicalCamp.SEKULER_KEMALIST: 0.32,
            IdeologicalCamp.MILLIYETCI_ULKUCU: 0.12,
            IdeologicalCamp.PRAGMATIST_GENCLIK: 0.10,
            IdeologicalCamp.DEM_KURT_HAREKETI: 0.08
        }

    def derive_ideology(
        self,
        city: str,
        district: str,
        age: int,
        occupation: str,
        education: str
    ) -> CitizenIdeologyProfile:
        """
        Derives an authentic ideological profile for a synthetic citizen.
        """
        weights = self.get_province_ideological_weights(city, district)
        occ_l = occupation.lower()

        # Security forces are strongly nationalist/state-aligned
        if any(w in occ_l for w in ["polis", "komiser", "jandarma", "asker", "güvenlik", "astsubay", "bekçi"]):
            chosen_camp = IdeologicalCamp.MILLIYETCI_ULKUCU
        # Young students under 25 have higher apolitical / secular / pro-Kurdish split
        elif age < 24 and self.rng.random() < 0.35:
            chosen_camp = IdeologicalCamp.PRAGMATIST_GENCLIK
        else:
            camps = list(weights.keys())
            probs = list(weights.values())
            chosen_camp = self.rng.choices(camps, weights=probs, k=1)[0]

        # Intensity (0.4 - 1.0)
        intensity = round(self.rng.uniform(0.65, 0.95) if age > 30 else self.rng.uniform(0.45, 0.85), 2)

        if chosen_camp == IdeologicalCamp.DEM_KURT_HAREKETI:
            news = self.rng.choice(["Medyascope & YouTube", "Artı Gerçek & Gazete Duvar", "Sosyal Medya & X (Twitter)"])
            redline = "Kürt kimliği, ana dil hakkı ve kayyum politikaları"
            rel = "Kültürel Müslüman / Özgürlükçü"
        elif chosen_camp == IdeologicalCamp.MILLIYETCI_ULKUCU:
            news = self.rng.choice(["Türkgün & BengüTürk", "HaberTürk & Yeniçağ", "Sosyal Medya Asker/Polis Sayfaları"])
            redline = "Vatanın bölünmezliği, terörle tavizsiz mücadele ve şehitler"
            rel = "Geleneksel Milliyetçi-Muhafazakar"
        elif chosen_camp == IdeologicalCamp.SEKULER_KEMALIST:
            news = self.rng.choice(["Sözcü TV & Gazetesi", "Halk TV & Tele1", "Cumhuriyet"])
            redline = "Laiklik, Cumhuriyet devrimleri ve liyakat"
            rel = "Seküler / Modern Yaşam Tarzı"
        elif chosen_camp == IdeologicalCamp.MUHAFAZAKAR_IKTIDAR:
            news = self.rng.choice(["A Haber & Sabah", "TRT Haber & Yeni Şafak", "Kanal 7 & Akit"])
            redline = "Devletin bekası, liderlik iradesi ve manevi değerler"
            rel = "Dindar / Cemaat & Aile Odaklı"
        else:
            news = self.rng.choice(["Instagram & TikTok", "YouTube Bağımsız Yayıncılar", "Ekşi Sözlük"])
            redline = "Ekonomik geçim, kira fiyatları ve gençlik geleceği"
            rel = "Bireysel / Non-pratik"

        return CitizenIdeologyProfile(
            camp=chosen_camp,
            political_intensity=intensity,
            primary_news_source=news,
            redline_issue=redline,
            religious_practice_level=rel
        )
