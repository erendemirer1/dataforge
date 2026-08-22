"""
DataForge Deep Multi-Agent Focus Group & Psychological Simulation Studio.
Powered by UniversalAIGateway (Zero-Config AI Inference).
Simulates realistic group dynamics, Dual-Process System 1/2 reactions,
Inner Subconscious Thoughts vs. Spoken Dialogue, and Executive Market Intelligence.
"""
from __future__ import annotations

import re
import json
import random
from typing import Any, Optional
from .cognitive_persona import CognitivePersonaBuilder, DeepCognitivePersona
from .utility_engine import EconometricUtilityEngine, QuantitativeMarketResult
from .consistency_auditor import CognitiveConsistencyAuditor
from .conversation_engine import LivingRoundtableEngine
from .llm_gateway import UniversalAIGateway
from ..social.social_radar import SocialRadarEngine
from ..ml.prompt_synthesizer import DynamicPromptEngine


class FocusGroupSimulator:
    """
    Executes deep psychological focus groups with grounded, neuro-sociologically complete personas.
    Zero-config AI execution: Cascades transparently through LLM and causal deliberation.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.persona_builder = CognitivePersonaBuilder(self.rng)
        self.prompt_engine = DynamicPromptEngine(self.rng)
        self.utility_engine = EconometricUtilityEngine(self.rng)
        self.social_radar = SocialRadarEngine(self.rng)
        self.consistency_auditor = CognitiveConsistencyAuditor()
        self.roundtable_engine = LivingRoundtableEngine(self.rng)
        self.ai_gateway = UniversalAIGateway.get_instance()

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

        # 4. Simulate Multi-Agent Focus Group with AI Gateway or Living Causal Roundtable
        qualitative_personas = cognitive_personas
        if len(cognitive_personas) > 8:
            step = len(cognitive_personas) // 6
            qualitative_personas = [cognitive_personas[i * step] for i in range(min(6, len(cognitive_personas)))]

        sim_result = self._simulate_with_ai(qualitative_personas, target_audience, pitch_or_question, api_key)
        if not sim_result:
            sim_result = self.roundtable_engine.generate_organic_roundtable(qualitative_personas, pitch_or_question, api_key)

        # 5. Run Cognitive Consistency Audit
        sim_result = self.consistency_auditor.audit_and_recalibrate(
            simulation_result=sim_result,
            personas_dict=dict_personas,
            pitch_or_topic=pitch_or_question
        )

        # 6. Attach Quantitative Census Output
        sim_result["kantitatif_monte_carlo_raporu"] = monte_carlo_res.to_dict()

        return sim_result

    def _simulate_with_ai(
        self,
        personas: list[DeepCognitivePersona],
        target_audience: str,
        pitch: str,
        api_key: Optional[str] = None
    ) -> Optional[dict[str, Any]]:
        """Simulates authentic inner monologue and spoken dialogue via Universal AI Gateway."""
        personas_json = json.dumps([p.to_dict() for p in personas], ensure_ascii=False, indent=2)

        sys_prompt = (
            "Sen Türkiye sosyolojisini, insanının kalbini, öfkesini, geçim derdini, mizahını ve gururunu "
            "en derinden bilen dahi bir Sosyolog, Antropolog ve Saha Araştırmacısısın.\n"
            f"Sana Türkiye gerçekliğinden {len(personas)} adet capcanlı insan profili veriliyor.\n\n"
            "GÖREVİN:\n"
            "Bu insanların moderatörün ortaya attığı teklif/soru karşısındaki "
            "gerçek tepkilerini bir yuvarlak masada simüle edeceksin.\n\n"
            "KESİN KURALLAR:\n"
            "1. Asla şablon veya tekrar eden cümleler kurma. Her karakterin kendine özgü, mesleğine, yaşadığı ilçeye, gelirine ve hayat şartlarına uygun bir dili olsun.\n"
            "2. Karakterler masada birbirine itiraz etsin, laf atsın veya destek çıksın (Group Dynamics).\n"
            "3. Karakterler sorulan konuya ('" + pitch + "') DOĞRUDAN kendi hayatlarından örnekler vererek cevap versin.\n"
            "4. SADECE aşağıdaki JSON formatında yanıt ver, markdown tırnağı koyma:\n"
            "{\n"
            '  "odak_grubu_tartismasi": [\n'
            '    {\n'
            '      "kisi_id": 1,\n'
            '      "ad_soyad": "Ad Soyad",\n'
            '      "meslek": "Meslek",\n'
            '      "karar": "Kabul Eder / Destekler" | "Kesinlikle Reddeder" | "Kararsız / Çekimser",\n'
            '      "ic_ses_bilincalti": "Karakterin iç sesi...",\n'
            '      "disa_soylenen_soz": "Masada yüksek sesle söylediği söz..."\n'
            '    }\n'
            '  ],\n'
            '  "yonetici_pazar_analiz_raporu": {\n'
            '    "genel_kabul_orani_yuzde": 65.0,\n'
            '    "en_buyuk_3_itiraz_bariyeri": ["Bariyer 1", "Bariyer 2", "Bariyer 3"],\n'
            '    "fiyat_duyarlilik_analizi": "Fiyat ve maliyet hassasiyeti analizi...",\n'
            '    "kutuplasma_indeksi_skoru": "0.75 / 1.0 (Orta-Yüksek Kutuplaşma)",\n'
            '    "what_if_karsi_olgusal_stres_testi": {\n'
            '      "senaryo_1_guvence": "Kabul oranı artışı...",\n'
            '      "senaryo_2_fiyat": "Fiyat artarsa ret oranı...",\n'
            '      "en_hizli_ikna_olacak_segment": "Segment tanımı..."\n'
            '    },\n'
            '    "stratejik_urun_tavsiyesi": "Stratejik tavsiye..."\n'
            '  }\n'
            "}"
        )

        user_content = f"HEDEF KİTLE: {target_audience}\nSUNULAN TEKLİF / SORU: {pitch}\n\nKATILIMCILAR:\n{personas_json}"

        response_text = self.ai_gateway.generate_chat_response(sys_prompt, user_content, api_key=api_key)
        if not response_text:
            return None

        clean_json = response_text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()

        try:
            return json.loads(clean_json)
        except Exception:
            return None
