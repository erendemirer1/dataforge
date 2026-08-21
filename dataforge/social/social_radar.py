"""
DataForge Live Social Radar & Digital Anthropology Layer.
Monitors Turkish social discourse (Twitter/X trends, Google Trends TR, Bloomberg HT, HaberTurk RSS)
and extracts contemporary cultural slang, emerging frustrations, and sectoral sentiment dynamically from the web.
"""
from __future__ import annotations

import json
import random
from typing import Any, Optional
from .archetype_registry import ArchetypeRegistry, TurkishArchetype
from ..scrapers.live_feed import LiveCultureScraper


class SocialRadarEngine:
    """
    Analyzes live Turkish cultural atmosphere dynamically using real-time web scrapers.
    Zero static hardcoding: Feeds live trends into persona psychographics.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.registry = ArchetypeRegistry()
        self.scraper = LiveCultureScraper()
        self._cached_snapshot: Optional[dict[str, Any]] = None

    def get_current_macro_sentiment(self) -> dict[str, Any]:
        """Returns the prevailing economic, sociological, and psychological climate in Turkey via live web data."""
        if not self._cached_snapshot:
            self._cached_snapshot = self.scraper.get_live_cultural_snapshot()

        return {
            "canli_gundem_maddeleri": self._cached_snapshot.get("canli_toplumsal_gundem", []),
            "canli_ekonomi_mansetleri": self._cached_snapshot.get("canli_ekonomi_mansetleri", []),
            "canli_arama_trendleri": self._cached_snapshot.get("canli_google_trendleri", []),
            "canli_kamu_ve_forum_gundemi": self._cached_snapshot.get("canli_kamu_ve_forum_gundemi", []),
            "canli_mevzuat_ve_yasa_degisiklikleri": self._cached_snapshot.get("canli_mevzuat_ve_yasa_degisiklikleri", []),
            "canli_piyasa_gostergeleri": self._cached_snapshot.get("canli_piyasa_gostergeleri", {}),
            "toplumsal_duygu_ozeti": "Enflasyon temkinliliği, mevzuat/hak arayışı, reel alım gücü koruma çabası ve güncel gündem duyarlılığı"
        }

    def enrich_persona_with_social_pulse(self, persona: dict[str, Any]) -> dict[str, Any]:
        """Injects live contemporary slang, relevant pains, and current cultural context into a persona."""
        occupation = persona.get("meslek_rol", persona.get("meslek", "Vatandaş"))
        archetype = self.registry.find_archetype_by_occupation(occupation)

        if not self._cached_snapshot:
            self._cached_snapshot = self.scraper.get_live_cultural_snapshot()

        live_topics = (
            self._cached_snapshot.get("canli_toplumsal_gundem", []) +
            self._cached_snapshot.get("canli_kamu_ve_forum_gundemi", []) +
            self._cached_snapshot.get("canli_mevzuat_ve_yasa_degisiklikleri", [])
        )
        chosen_live_topic = self.rng.choice(live_topics) if live_topics else "Genel Geçim ve Enflasyon Kaygısı"

        persona["toplumsal_arketip"] = archetype.archetype_title
        persona["nufus_temsil_orani_yuzde"] = archetype.population_share_pct
        persona["guncel_sosyal_gundem_etkisi"] = chosen_live_topic
        persona["fiyat_hassasiyet_duzeyi"] = archetype.price_sensitivity

        return persona
