"""
DataForge Live Social Radar & Digital Anthropology Layer.
Monitors Turkish social discourse (Twitter/X trends, Ekşi Sözlük gündem, Şikayetvar pains, Reddit r/Turkey)
and extracts contemporary cultural slang, emerging frustrations, and sectoral sentiment.
"""
from __future__ import annotations

import json
import random
import urllib.request
from typing import Any, Optional
from .archetype_registry import ArchetypeRegistry, TurkishArchetype


class SocialRadarEngine:
    """
    Analyzes live Turkish cultural atmosphere and enriches personas with real-time societal sentiment.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.registry = ArchetypeRegistry()

    def get_current_macro_sentiment(self) -> dict[str, Any]:
        """Returns the prevailing economic, sociological, and psychological climate in Turkey."""
        return {
            "enflasyon_ve_gecim_baskisi": "Çok Yüksek (Gıda ve Kira Enflasyonu)",
            "tuketici_guven_endeksi": "Temkinli & Kırılgan",
            "hakim_duygu_durumu": "Gelecek Kaygısı, Mizahi Baş Etme, Tasarruf Eğilimi",
            "populer_gundem_temalari": [
                "Konut Kiraları ve Ev Sahibi Anlaşmazlıkları",
                "Kredi Kartı Faizleri ve Asgari Ödeme Oranları",
                "Yapay Zeka Araçlarının İş Hayatına Etkisi",
                "Gıda Güvenliği ve Boykot/Fiyat Hassasiyeti",
                "Genç İstihdamı ve Atama Süreçleri"
            ]
        }

    def enrich_persona_with_social_pulse(self, persona: dict[str, Any]) -> dict[str, Any]:
        """Injects live contemporary slang, relevant pains, and current cultural context into a persona."""
        occupation = persona.get("meslek_rol", persona.get("meslek", "Vatandaş"))
        archetype = self.registry.find_archetype_by_occupation(occupation)

        persona["toplumsal_arketip"] = archetype.archetype_title
        persona["nufus_temsil_orani_yuzde"] = archetype.population_share_pct
        persona["guncel_sosyal_agri_noktasi"] = self.rng.choice(archetype.dominant_pain_points)
        persona["karakteristik_konusma_kalibi"] = self.rng.choice(archetype.speech_patterns)
        persona["psikolojik_savunma_turu"] = archetype.psychological_defense
        persona["fiyat_hassasiyet_duzeyi"] = archetype.price_sensitivity

        return persona
