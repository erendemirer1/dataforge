"""
DataForge Persistent Cultural & Economic Memory Store.
Maintains a cumulative, time-series historical SQLite database (~/.dataforge/cultural_memory.db)
of Turkish public sentiment, economic shocks, price trajectories, and legislative debates over time.
Enables personas to reflect cumulative 30/90-day socio-economic memory rather than just instantaneous snapshots.
"""
from __future__ import annotations

import os
import json
import sqlite3
import datetime
from pathlib import Path
from typing import Any, Optional
from ..scrapers.live_feed import LiveCultureScraper


class CulturalMemoryStore:
    """Persistent time-series store for continuous autonomous cultural learning."""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            dataforge_dir = Path.home() / ".dataforge"
            dataforge_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = dataforge_dir / "cultural_memory.db"
        else:
            self.db_path = db_path

        self.scraper = LiveCultureScraper()
        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def _init_database(self) -> None:
        """Initializes tables for time-series memory storage."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pulse_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    source_category TEXT,
                    item_title TEXT,
                    sentiment_tone TEXT,
                    raw_metadata JSON
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS financial_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usd_try REAL,
                    eur_try REAL,
                    policy_rate TEXT,
                    macro_note TEXT
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_pulse_time ON pulse_snapshots(timestamp);
            """)
            conn.commit()

    def sync_live_pulse(self) -> dict[str, Any]:
        """Scrapes all 6 live feeds and archives them persistently with timestamps."""
        snapshot = self.scraper.get_live_cultural_snapshot()
        now = datetime.datetime.now().isoformat()
        inserted_count = 0

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Google Trends
            for trend in snapshot.get("canli_google_trendleri", []):
                cursor.execute(
                    "INSERT INTO pulse_snapshots (timestamp, source_category, item_title, sentiment_tone, raw_metadata) VALUES (?, ?, ?, ?, ?)",
                    (now, "google_trends", trend, "arama_meraki", json.dumps({"type": "search_volume"}))
                )
                inserted_count += 1

            # 2. National News
            for news in snapshot.get("canli_toplumsal_gundem", []):
                cursor.execute(
                    "INSERT INTO pulse_snapshots (timestamp, source_category, item_title, sentiment_tone, raw_metadata) VALUES (?, ?, ?, ?, ?)",
                    (now, "national_news", news, "toplumsal_gundem", json.dumps({"channel": "national_press"}))
                )
                inserted_count += 1

            # 3. Economy & Markets
            for econ in snapshot.get("canli_ekonomi_mansetleri", []):
                cursor.execute(
                    "INSERT INTO pulse_snapshots (timestamp, source_category, item_title, sentiment_tone, raw_metadata) VALUES (?, ?, ?, ?, ?)",
                    (now, "economy", econ, "piyasa_baskisi", json.dumps({"channel": "bloomberg_dunya"}))
                )
                inserted_count += 1

            # 4. Forums & Public Grievances
            for forum in snapshot.get("canli_kamu_ve_forum_gundemi", []):
                cursor.execute(
                    "INSERT INTO pulse_snapshots (timestamp, source_category, item_title, sentiment_tone, raw_metadata) VALUES (?, ?, ?, ?, ?)",
                    (now, "public_forums", forum, "halk_sikayeti", json.dumps({"source": "memurlar_donanimhaber"}))
                )
                inserted_count += 1

            # 5. Legislation & Laws
            for law in snapshot.get("canli_mevzuat_ve_yasa_degisiklikleri", []):
                cursor.execute(
                    "INSERT INTO pulse_snapshots (timestamp, source_category, item_title, sentiment_tone, raw_metadata) VALUES (?, ?, ?, ?, ?)",
                    (now, "legislation", law, "yasal_degisiklik", json.dumps({"source": "resmi_gazete"}))
                )
                inserted_count += 1

            # 6. Financial Rates
            fin = snapshot.get("canli_piyasa_gostergeleri", {})
            cursor.execute(
                "INSERT INTO financial_history (timestamp, usd_try, eur_try, policy_rate, macro_note) VALUES (?, ?, ?, ?, ?)",
                (now, fin.get("canli_usd_try", 38.5), fin.get("canli_eur_try", 41.0), fin.get("politika_faizi", "%50"), fin.get("enflasyon_hissi", "Yuksek"))
            )

            conn.commit()

        return {
            "durum": "Basarili",
            "eklenen_veri_adedi": inserted_count,
            "zaman_damgasi": now,
            "toplam_hafiza_kaydi": self.get_total_memory_count()
        }

    def get_total_memory_count(self) -> int:
        """Returns total historical records stored."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pulse_snapshots")
            return cursor.fetchone()[0]

    def get_recent_cumulative_topics(self, limit: int = 30) -> list[str]:
        """Fetches the most relevant accumulated public topics from persistent storage."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item_title FROM pulse_snapshots ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [r[0] for r in rows] if rows else []

    def get_memory_stats(self) -> dict[str, Any]:
        """Provides status report of the continuous memory store."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT source_category, COUNT(*) FROM pulse_snapshots GROUP BY source_category")
            category_counts = dict(cursor.fetchall())
            cursor.execute("SELECT MAX(timestamp) FROM pulse_snapshots")
            last_sync = cursor.fetchone()[0]

            return {
                "veritabani_konumu": str(self.db_path),
                "toplam_kayit": self.get_total_memory_count(),
                "kategori_dagilimi": category_counts,
                "son_guncelleme": last_sync or "Henuz calistirilamadi"
            }
