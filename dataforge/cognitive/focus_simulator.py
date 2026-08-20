"""
DataForge Deep Multi-Agent Focus Group & Psychological Simulation Studio.
Simulates realistic group dynamics, Dual-Process System 1/2 reactions,
Inner Subconscious Thoughts vs. Spoken Dialogue, and Executive Market Intelligence.
"""
from __future__ import annotations

import os
import json
import random
import urllib.request
from typing import Any, Optional
from .cognitive_persona import CognitivePersonaBuilder, DeepCognitivePersona
from ..ml.prompt_synthesizer import DynamicPromptEngine


class FocusGroupSimulator:
    """
    Executes deep psychological focus groups with grounded, neuro-sociologically complete personas.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.persona_builder = CognitivePersonaBuilder(self.rng)
        self.prompt_engine = DynamicPromptEngine(self.rng)

    def _get_api_key(self) -> str:
        """Resolve Gemini API key."""
        return self.prompt_engine._get_gemini_key() or ""

    def run_simulation(
        self,
        target_audience: str,
        pitch_or_question: str,
        count: int = 5
    ) -> dict[str, Any]:
        """
        Synthesizes deep personas and simulates an authentic, multi-agent focus group discussion.
        """
        # 1. Synthesize demographic personas
        raw_personas = self.prompt_engine.synthesize(target_audience, count=count)

        # 2. Enrich into Deep Cognitive & Habitus Personas
        cognitive_personas: list[DeepCognitivePersona] = []
        for i, raw_p in enumerate(raw_personas):
            cog_p = self.persona_builder.build_from_raw(raw_p, record_id=i + 1)
            cognitive_personas.append(cog_p)

        # 3. Simulate Multi-Agent Focus Group with LLM
        api_key = self._get_api_key()
        if not api_key:
            return self._fallback_simulation(cognitive_personas, pitch_or_question)

        return self._simulate_with_gemini(cognitive_personas, target_audience, pitch_or_question, api_key)

    def _simulate_with_gemini(
        self,
        personas: list[DeepCognitivePersona],
        target_audience: str,
        pitch: str,
        api_key: str
    ) -> dict[str, Any]:
        """Simulates authentic inner monologue and spoken dialogue with Gemini 3.5 Flash Lite."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"

        # Format personas context for LLM
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
            "2. KATI BÜTÇE VE SINIF KISITI: Aylık harcanabilir parası 2.000 TL olan bir adam 1.000 TL'lik teklife asla 'alırım' diyemez! Bütçesine göre acımasızca direnç göstermelidir.\n"
            "3. GERÇEK TÜRKÇE VE JARGON: Sanayi ustası sanayi diliyle, esnaf esnaf gibi, beyaz yaka plaza diliyle, köylü kendi şivesiyle konuşmalıdır.\n"
            "4. BİLİŞSEL DİRENÇ: İnsanların en az %60-70'i ilk teklifte şüphelenir, reddeder veya pazarlık ister.\n\n"
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
            '    "fiyat_duyarlilik_analizi": "Hedef kitlenin fiyat algısı ve önerilen ideal fiyat...",\n'
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            clean_text = text.replace("```json", "").replace("```", "").strip()
            sim_result = json.loads(clean_text)

        # Attach deep cognitive profiles to the output
        sim_result["katilimci_profilleri"] = [p.to_dict() for p in personas]
        return sim_result

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
            },
            "katilimci_profilleri": [p.to_dict() for p in personas]
        }
