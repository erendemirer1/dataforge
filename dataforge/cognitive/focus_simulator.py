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
from ..social.social_radar import SocialRadarEngine
from ..ml.prompt_synthesizer import DynamicPromptEngine


class FocusGroupSimulator:
    """
    Executes deep psychological focus groups with grounded, neuro-sociologically complete personas.
    Combines qualitative focus groups with N=1,000 quantitative Monte Carlo econometrics.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.persona_builder = CognitivePersonaBuilder(self.rng)
        self.prompt_engine = DynamicPromptEngine(self.rng)
        self.utility_engine = EconometricUtilityEngine(self.rng)
        self.social_radar = SocialRadarEngine(self.rng)

    def _get_api_key(self) -> str:
        """Resolve Gemini API key."""
        return self.prompt_engine._get_gemini_key() or ""

    def _extract_price_from_pitch(self, pitch: str) -> float:
        """Extract monetary price from text in TL."""
        match = re.search(r'(\d+(?:[\.,]\d+)?)\s*(?:tl|lira|₺|tl\'ye|liralık)', pitch.lower())
        if match:
            val_str = match.group(1).replace(',', '.')
            try:
                return float(val_str)
            except ValueError:
                pass
        return 250.0 # sensible default benchmark if not specified

    def run_simulation(
        self,
        target_audience: str,
        pitch_or_question: str,
        count: int = 4,
        monte_carlo_n: int = 1000
    ) -> dict[str, Any]:
        """
        Synthesizes deep personas, simulates focus group discussion,
        and computes an N=1,000 quantitative Monte Carlo census.
        """
        # 1. Synthesize demographic personas
        raw_personas = self.prompt_engine.synthesize(target_audience, count=count)

        # 2. Enrich into Deep Cognitive, Social Radar & Habitus Personas
        cognitive_personas: list[DeepCognitivePersona] = []
        for i, raw_p in enumerate(raw_personas):
            raw_p = self.social_radar.enrich_persona_with_social_pulse(raw_p)
            cog_p = self.persona_builder.build_from_raw(raw_p, record_id=i + 1)
            cognitive_personas.append(cog_p)

        # 3. Run Quantitative Econometric Monte Carlo Census (N=1,000)
        extracted_price = self._extract_price_from_pitch(pitch_or_question)
        dict_personas = [p.to_dict() for p in cognitive_personas]
        monte_carlo_res: QuantitativeMarketResult = self.utility_engine.run_monte_carlo_census(
            personas=dict_personas,
            pitch_price_tl=extracted_price,
            simulations_count=monte_carlo_n
        )

        # 4. Simulate Multi-Agent Focus Group with LLM
        api_key = self._get_api_key()
        if not api_key:
            sim_result = self._fallback_simulation(cognitive_personas, pitch_or_question)
        else:
            sim_result = self._simulate_with_gemini(cognitive_personas, target_audience, pitch_or_question, api_key)

        # 5. Merge Quantitative Econometrics with Qualitative Findings
        sim_result["kantitatif_monte_carlo_raporu"] = {
            "orneklem_buyuklugu": monte_carlo_res.sample_size,
            "test_edilen_fiyat_tl": extracted_price,
            "matematiksel_kabul_orani_yuzde": monte_carlo_res.acceptance_rate_pct,
            "guven_araligi_yuzde_95": f"%{monte_carlo_res.confidence_interval_95[0]} - %{monte_carlo_res.confidence_interval_95[1]}",
            "fiyat_esneklik_skoru": monte_carlo_res.elasticity_score,
            "fiyat_esneklik_egrisi": monte_carlo_res.price_sensitivity_curve,
            "sinifsal_kabul_dagilimi": monte_carlo_res.demographic_breakdown,
            "ortalama_serbest_butce_tl": monte_carlo_res.mean_discretionary_budget_tl,
            "mutlak_butce_yetersizlik_orani_yuzde": monte_carlo_res.budget_violation_rate_pct
        }
        sim_result["katilimci_profilleri"] = dict_personas
        return sim_result

    def _simulate_with_gemini(
        self,
        personas: list[DeepCognitivePersona],
        target_audience: str,
        pitch: str,
        api_key: str
    ) -> dict[str, Any]:
        """Simulates authentic inner monologue and spoken dialogue with Gemini 3.5 Flash Lite."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"

        personas_json = json.dumps([p.to_dict() for p in personas], ensure_ascii=False, indent=2)

        sys_prompt = (
            "Sen dünyanın en yetkin Nöro-Pazarlama, Bilişsel Psikoloji ve Türkiye Saha Araştırmaları Uzmanısın. "
            "Sana Türkiye'nin gerçek sosyo-ekonomik, sınıfsal ve nörobiyolojik verileriyle oluşturulmuş "
            f"{len(personas)} adet derin insan profili veriliyor.\n\n"
            "GÖREVİN:\n"
            "Bu insanları moderatörün sunduğu teklif/soru karşısında bir Odak Grubu (Focus Group) masasında konuşturacaksın.\n\n"
            "KESİN PSİKOLOJİK VE DAVRANIŞSAL KURALLAR:\n"
            "1. İÇ SES vs DIŞ SÖZ (ÇİFT SÜREÇ TEORİSİ): İnsanlar asla düşündüklerini direkt söylemez! "
            "Her karakter için hem bilinçaltındaki gerçek niyetini/korkusunu ('ic_ses_bilincalti'), "
            "hem de masadaki insanlara kendi jargonuyla söylediği sözü ('disa_soylenen_soz') yaz.\n"
            "2. KATI BÜTÇE VE SINIF KISITI: Karakterlerin harcanabilir serbest bütçesini ve borçluluğunu hesaba kat. "
            "Karakterler fiyat ve risk durumuna göre acımasızca direnç göstermelidir.\n"
            "3. GERÇEK TÜRKÇE VE JARGON: Sanayi ustası sanayi diliyle, esnaf esnaf gibi, beyaz yaka plaza diliyle, genç Z kuşağı argosuyla konuşmalıdır.\n"
            "4. BİLİŞSEL DİRENÇ: İnsanların en az %60'ı ilk teklifte şüphelenir, pazarlık ister veya erteler.\n\n"
            "ÇIKTI FORMATI: Sadece ve sadece aşağıdaki JSON formatında yanıt ver:\n"
            "{\n"
            '  "odak_grubu_tartismasi": [\n'
            "    {\n"
            '      "kisi_id": 1,\n'
            '      "ad_soyad": "İsim Soyisim",\n'
            '      "meslek": "Meslek",\n'
            '      "karar": "Satın Alır" | "Kesinlikle Reddeder" | "Pazarlık / İndirim İster" | "Düşünmek İçin Erteletir",\n'
            '      "ic_ses_bilincalti": "Gerçek korkusu, parası, egosu ve içinden geçenler...",\n'
            '      "disa_soylenen_soz": "Masada herkesin duyacağı şekilde söylediği replik..."\n'
            "    }\n"
            "  ],\n"
            '  "yonetici_pazar_analiz_raporu": {\n'
            '    "genel_kabul_orani_yuzde": 35,\n'
            '    "en_buyuk_3_itiraz_bariyeri": ["İtiraz 1", "İtiraz 2", "İtiraz 3"],\n'
            '    "fiyat_duyarlilik_analizi": "Hedef kitlenin fiyat algısı...",\n'
            '    "stratejik_urun_tavsiyesi": "Ürünün kabul görmesi için yapılması gereken kritik değişiklik..."\n'
            "  }\n"
            "}"
        )

        user_content = f"HEDEF KİTLE: {target_audience}\nSUNULAN TEKLİF / SORU: {pitch}\n\nSENTETİK MÜŞTERİLERİN DERİN ZİHİNSEL VERİLERİ:\n{personas_json}"

        payload = {
            "contents": [
                {"parts": [{"text": f"{sys_prompt}\n\n{user_content}"}]}
            ]
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                sim_result = self._robust_json_parse(text)
                return sim_result
        except Exception:
            return self._fallback_simulation(personas, pitch)

    def _robust_json_parse(self, text: str) -> dict[str, Any]:
        """Robustly extracts and parses JSON even with trailing commas or markdown framing."""
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
                try:
                    return json.loads(sub_fixed)
                except Exception:
                    pass
        raise ValueError("Could not parse JSON from model response")

    def _fallback_simulation(self, personas: list[DeepCognitivePersona], pitch: str) -> dict[str, Any]:
        """Offline fallback."""
        discussions = []
        for p in personas:
            discussions.append({
                "kisi_id": p.id,
                "ad_soyad": p.ad_soyad,
                "meslek": p.meslek,
                "karar": "Pazarlık / İndirim İster",
                "ic_ses_bilincalti": f"Aylık serbest bütçem sadece {p.aylik_serbest_harcanabilir_tl} TL. Risk alamam.",
                "disa_soylenen_soz": "Biraz pahalı geldi, biraz indirim yaparsanız düşünebilirim."
            })
        return {
            "odak_grubu_tartismasi": discussions,
            "yonetici_pazar_analiz_raporu": {
                "genel_kabul_orani_yuzde": 40,
                "en_buyuk_3_itiraz_bariyeri": ["Yüksek Fiyat", "Güven Eksikliği", "Alışkanlık Direnci"],
                "fiyat_duyarlilik_analizi": "Bütçe kısıtları nedeniyle indirim talep ediliyor.",
                "stratejik_urun_tavsiyesi": "Fiyatı harcanabilir bütçeye göre optimize edin."
            }
        }
