"""
DataForge Deep Multi-Agent Focus Group & Psychological Simulation Studio.
Simulates realistic group dynamics, Dual-Process System 1/2 reactions,
Inner Subconscious Thoughts vs. Spoken Dialogue, and Executive Market Intelligence.
Integrates McFadden Econometric Utility Engine for N=1,000 Monte Carlo statistical census.
"""
from __future__ import annotations

import os
import re
import json
import random
import urllib.request
from typing import Any, Optional
from .cognitive_persona import CognitivePersonaBuilder, DeepCognitivePersona
from .utility_engine import EconometricUtilityEngine, QuantitativeMarketResult
from .consistency_auditor import CognitiveConsistencyAuditor
from .conversation_engine import LivingRoundtableEngine
from ..social.social_radar import SocialRadarEngine
from ..ml.prompt_synthesizer import DynamicPromptEngine


class FocusGroupSimulator:
    """
    Executes deep psychological focus groups with grounded, neuro-sociologically complete personas.
    Combines qualitative focus groups with N=1,000 quantitative Monte Carlo econometrics and Causal Consistency Audits.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.persona_builder = CognitivePersonaBuilder(self.rng)
        self.prompt_engine = DynamicPromptEngine(self.rng)
        self.utility_engine = EconometricUtilityEngine(self.rng)
        self.social_radar = SocialRadarEngine(self.rng)
        self.consistency_auditor = CognitiveConsistencyAuditor()
        self.roundtable_engine = LivingRoundtableEngine(self.rng)

    def _get_api_key(self) -> str:
        """Resolve Gemini API key."""
        return self.prompt_engine._get_gemini_key() or ""

    def _extract_price_from_pitch(self, pitch: str) -> Optional[float]:
        """Extract monetary price from text in TL. Returns None if topic is non-commercial."""
        match = re.search(r'(\d+(?:[\.,]\d+)?)\s*(?:tl|lira|₺|tl\'ye|liralık|bin tl)', pitch.lower())
        if match:
            val_str = match.group(1).replace(',', '.')
            try:
                val = float(val_str)
                if 'bin' in pitch.lower():
                    val *= 1000
                return val
            except ValueError:
                pass
        return None

    def run_simulation(
        self,
        target_audience: str,
        pitch_or_question: str,
        count: int = 4,
        monte_carlo_n: int = 1000,
        api_key: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Synthesizes deep personas, simulates focus group discussion,
        audits consistency against latent belief vectors,
        and computes an N=1,000 quantitative Monte Carlo census.
        """
        # 1. Synthesize demographic qualitative personas (4-8 around the roundtable)
        qual_count = min(count, 8) if count > 8 else count
        raw_personas = self.prompt_engine.synthesize(target_audience, count=qual_count)

        # 2. Enrich into Deep Cognitive, Social Radar, Latent Belief & Habitus Personas
        cognitive_personas: list[DeepCognitivePersona] = []
        for i, raw_p in enumerate(raw_personas):
            raw_p = self.social_radar.enrich_persona_with_social_pulse(raw_p)
            cog_p = self.persona_builder.build_from_raw(raw_p, record_id=i + 1)
            cognitive_personas.append(cog_p)

        # 3. Run Quantitative Econometric / Moral Monte Carlo Census (N=1,000 to N=10,000)
        extracted_price = self._extract_price_from_pitch(pitch_or_question)
        dict_personas = [p.to_dict() for p in cognitive_personas]
        mc_n = max(count, monte_carlo_n)
        monte_carlo_res: QuantitativeMarketResult = self.utility_engine.run_monte_carlo_census(
            personas=dict_personas,
            pitch_text=pitch_or_question,
            pitch_price_tl=extracted_price,
            simulations_count=mc_n
        )

        # 4. Simulate Multi-Agent Focus Group with LLM
        qualitative_personas = cognitive_personas
        if len(cognitive_personas) > 8:
            step = len(cognitive_personas) // 6
            qualitative_personas = [cognitive_personas[i * step] for i in range(min(6, len(cognitive_personas)))]

        effective_key = api_key or self._get_api_key()
        sim_result = None
        if effective_key and not effective_key.startswith("AQ."):
            try:
                sim_result = self._simulate_with_gemini(qualitative_personas, target_audience, pitch_or_question, effective_key)
            except Exception:
                sim_result = None

        if not sim_result:
            sim_result = self._fallback_simulation(qualitative_personas, pitch_or_question)

        # 5. Run Cognitive Consistency Audit
        sim_result = self.consistency_auditor.audit_and_recalibrate(
            simulation_result=sim_result,
            personas_dict=dict_personas,
            pitch_or_topic=pitch_or_question
        )

        # 6. Attach Quantitative Census Output
        sim_result["kantitatif_monte_carlo_raporu"] = monte_carlo_res.to_dict()

        return sim_result

    def _simulate_with_gemini(
        self,
        personas: list[DeepCognitivePersona],
        target_audience: str,
        pitch: str,
        api_key: str
    ) -> dict[str, Any]:
        """Simulates authentic inner monologue and spoken dialogue with Gemini."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"

        personas_json = json.dumps([p.to_dict() for p in personas], ensure_ascii=False, indent=2)

        sys_prompt = (
            "Sen Türkiye toplumunu, insanının kalbini, öfkesini, acısını, çaresizliğini, mizahını ve gururunu "
            "en derinden bilen dahi bir Sosyolog, Antropolog ve Saha Araştırmacısısın. "
            f"Sana Türkiye gerçekliğinden {len(personas)} adet capcanlı insan profili veriliyor.\n\n"
            "GÖREVİN:\n"
            "Bu insanların moderatörün ortaya attığı teklif, soru veya siyasi/toplumsal gelişme karşısındaki "
            "gerçek tepkilerini bir masada simüle edeceksin.\n\n"
            "KESİN KURALLAR:\n"
            "1. Asla şablon veya tekrar eden cümleler kurma. Her karakterin kendine özgü, mesleğine ve travmasına uygun bir sesi olsun.\n"
            "2. Karakterler masada birbirine itiraz etsin, laf atsın veya destek çıksın (Group Dynamics).\n"
            "3. Asla çelişkili ifadeler kurma (Örn: Hükümete kızıp aynı anda destekleme gibi mantık hataları olmasın).\n"
        )

        user_content = f"HEDEF KİTLE: {target_audience}\nSUNULAN TEKLİF / SORU: {pitch}\n\nKATILIMCILAR:\n{personas_json}"

        payload = {
            "contents": [{"parts": [{"text": f"{sys_prompt}\n\n{user_content}"}]}]
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return self._robust_json_parse(text)

    def _robust_json_parse(self, text: str) -> dict[str, Any]:
        """Robustly extracts and parses JSON."""
        clean_text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(clean_text)
        except Exception:
            pass

        start_idx = clean_text.find("{")
        end_idx = clean_text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            sub = clean_text[start_idx:end_idx + 1]
            try:
                return json.loads(sub)
            except Exception:
                sub_fixed = re.sub(r',\s*([}\]])', r'\1', sub)
                return json.loads(sub_fixed)
        raise ValueError("Could not parse JSON from model response")

    def _fallback_simulation(self, personas: list[DeepCognitivePersona], pitch: str) -> dict[str, Any]:
        """
        Delegates to LivingRoundtableEngine to synthesize organic,
        interruption-rich, living multi-agent human dialogue.
        """
        return self.roundtable_engine.generate_organic_roundtable(personas, pitch)
