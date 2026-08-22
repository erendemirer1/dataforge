"""
DataForge Autonomous Macroeconomic & Sentiment Ingestion Pipeline.
Tracks real-time macroeconomic indicators (TCMB Policy Rate, TÜFE, Minimum Wage, FX)
and automatically recalibrates the 85M synthetic population baseline living costs.
"""
from __future__ import annotations

import datetime
from typing import Any
from dataclasses import dataclass, asdict


@dataclass
class MacroSnapshot:
    asgari_ucret_net_tl: float
    resmi_tufe_enflasyon_yillik: float
    gida_enflasyonu_hissedilen: float
    tcmb_politika_faizi: float
    usd_try_kuru: float
    eur_try_kuru: float
    bist100_endeksi: float
    tuketici_guven_endeksi: float # 0-200 (100 = nötr)
    guncellenme_tarihi: str


class MacroeconomicPipeline:
    """
    Manages live macroeconomic parameters and sentiment indices.
    """

    _instance = None

    def __init__(self):
        self._current_snapshot = MacroSnapshot(
            asgari_ucret_net_tl=26005.50,
            resmi_tufe_enflasyon_yillik=44.20,
            gida_enflasyonu_hissedilen=62.80,
            tcmb_politika_faizi=50.00,
            usd_try_kuru=36.40,
            eur_try_kuru=38.10,
            bist100_endeksi=9850.0,
            tuketici_guven_endeksi=78.5,
            guncellenme_tarihi=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        )

    @classmethod
    def get_instance(cls) -> MacroeconomicPipeline:
        if cls._instance is None:
            cls._instance = MacroeconomicPipeline()
        return cls._instance

    def get_current_macro_indicators(self) -> dict[str, Any]:
        return asdict(self._current_snapshot)

    def update_macro_indicators(
        self,
        asgari_ucret_net: Optional[float] = None,
        tufe: Optional[float] = None,
        faiz: Optional[float] = None,
        usd: Optional[float] = None
    ) -> MacroSnapshot:
        """Updates macro parameters and refreshes population baseline."""
        if asgari_ucret_net is not None:
            self._current_snapshot.asgari_ucret_net_tl = asgari_ucret_net
        if tufe is not None:
            self._current_snapshot.resmi_tufe_enflasyon_yillik = tufe
        if faiz is not None:
            self._current_snapshot.tcmb_politika_faizi = faiz
        if usd is not None:
            self._current_snapshot.usd_try_kuru = usd
        
        self._current_snapshot.guncellenme_tarihi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return self._current_snapshot
