"""
DataForge Live Cultural & Market Pulse Scraper.
Dynamically fetches real-time public sentiment, trending topics, forum discussions,
and economic concerns directly from live Turkish web feeds (Zero Hardcoding).
"""
from __future__ import annotations

import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Optional


class LiveCultureScraper:
    """Fetches real-time cultural, economic, and subcultural pulse from live web sources."""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def fetch_google_trends_tr(self) -> list[str]:
        """Fetches real-time trending search queries in Turkey."""
        url = "https://trends.google.com/trending/rss?geo=TR"
        trends = []
        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            with urllib.request.urlopen(req, timeout=6) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//item/title"):
                    if item.text:
                        trends.append(item.text.strip())
        except Exception:
            pass
        return trends[:15]

    def fetch_national_news_feed(self) -> list[str]:
        """Fetches real-time hot news & public discussions from TR RSS feeds."""
        urls = [
            "https://www.haberturk.com/rss/manset.xml",
            "https://www.ntv.com.tr/gundem.rss",
            "https://www.sozcu.com.tr/rss/tum-haberler.xml"
        ]
        news = []
        for url in urls:
            try:
                req = urllib.request.Request(url, headers=self.HEADERS)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    root = ET.fromstring(resp.read())
                    for item in root.findall(".//item/title"):
                        if item.text and len(item.text.strip()) > 10:
                            news.append(item.text.strip())
            except Exception:
                continue
            if len(news) >= 15:
                break
        return news[:15]

    def fetch_economic_news_feed(self) -> list[str]:
        """Fetches latest real-time economy & inflation headlines in Turkey."""
        url = "https://www.bloomberght.com/rss"
        headlines = []
        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            with urllib.request.urlopen(req, timeout=6) as resp:
                root = ET.fromstring(resp.read())
                for item in root.findall(".//item/title"):
                    if item.text:
                        headlines.append(item.text.strip())
        except Exception:
            pass
        return headlines[:10]

    def get_live_cultural_snapshot(self) -> dict[str, Any]:
        """Collects an integrated live snapshot of Turkish public discourse."""
        trends = self.fetch_google_trends_tr()
        news = self.fetch_national_news_feed()
        economy = self.fetch_economic_news_feed()

        return {
            "canli_google_trendleri": trends,
            "canli_toplumsal_gundem": news,
            "canli_ekonomi_mansetleri": economy,
            "toplam_toplanan_veri_adedi": len(trends) + len(news) + len(economy)
        }
