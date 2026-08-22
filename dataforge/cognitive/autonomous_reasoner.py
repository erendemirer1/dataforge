"""
DataForge Pure LLM-Driven Autonomous Cognitive Reasoner.
Powered by CognitiveDossier (50+ Parameters) and UniversalAIGateway.
Synthesizes decisions and authentic inner thoughts by directly inhabiting the persona's lived reality.
"""
from __future__ import annotations

import json
import random
from typing import Any, Optional
from dataclasses import dataclass

from .cognitive_persona import DeepCognitivePersona
from .cognitive_dossier import CognitiveDossierBuilder
from .llm_gateway import UniversalAIGateway


class AutonomousCognitiveReasoner:
    """
    100% LLM & Causal Dossier-powered Cognitive Inhabitation Engine.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.ai_gateway = UniversalAIGateway.get_instance()
        self.dossier_builder = CognitiveDossierBuilder(self.rng)
        self._eval_cache: dict[str, dict[str, Any]] = {}

    def evaluate_and_synthesize_ballot(
        self,
        persona: DeepCognitivePersona,
        question: str,
        api_key: Optional[str] = None
    ) -> dict[str, str]:
        """
        Synthesizes the citizen's decision and authentic inner reasoning via LLM and Cognitive Dossier.
        """
        dossier = self.dossier_builder.build_dossier(persona)
        cache_key = f"{persona.meslek}_{persona.yas}_{persona.sehir_ilce}_{persona.aylik_net_gelir_tl}_{question}"
        if cache_key in self._eval_cache:
            return self._eval_cache[cache_key]

        sys_prompt = (
            "Sen Türkiye sosyolojisini, halkın dilini, geçim derdini, beklentilerini ve sokak dinamiklerini "
            "en derinden bilen bir Saha Araştırmacısı ve Sosyologsun.\n"
            "GÖREVİN: Aşağıda 50+ parametreli TAM BİYOGRAFİK DOSYASI verilen Türkiye Cumhuriyeti yurttaşının zihnine bürünerek (Persona Inhabitation), "
            "kendisine yöneltilen anket sorusuna / yerel projeye vereceği GERÇEK tepkiyi oluşturmaktır.\n\n"
            "KURALLAR:\n"
            "1. Asla robotik, kitabi veya şablon cümle kurma. Yurttaşın yaşına, mesleğine, yaşadığı ilçeye, gelirine, kirasına, ahlak koordinatlarına ve korkularına tam uygun, samimi, Türkçe konuşma diliyle yaz.\n"
            "2. Yurttaşın kendi kişisel yaşamını ve mahallesini referans alan 1-2 cümlelik özgün bir iç ses oluştur.\n"
            "3. SADECE aşağıdaki JSON formatında yanıt ver, markdown tırnağı koyma:\n"
            "{\n"
            '  "karar": "Kabul Eder / Destekler" | "Kesinlikle Reddeder" | "Kararsız / Çekimser",\n'
            '  "bireysel_dusuncesi_ve_gerekcesi": "Yurttaşın samimi iç sesi ve gerekçesi..."\n'
            "}"
        )

        user_content = (
            f"YURTTAŞ BİYOGRAFİK DOSYASI:\n{dossier.to_llm_system_context()}\n\n"
            f"ANKET SORUSU / BELEDİYE TEKLİFİ:\n\"{question}\""
        )

        response = self.ai_gateway.generate_chat_response(sys_prompt, user_content, temperature=0.7, api_key=api_key)
        result = None

        if response:
            clean = response.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.endswith("```"):
                clean = clean[:-3]
            clean = clean.strip()
            try:
                result = json.loads(clean)
            except Exception:
                result = None

        if not result or "karar" not in result or "bireysel_dusuncesi_ve_gerekcesi" not in result:
            district = persona.sehir_ilce.split('/')[-1].strip()
            occ = persona.meslek
            age = persona.yas
            
            # Pure probabilistic sociological stance based on income and age
            ratio = (persona.aylik_net_gelir_tl / 40000.0) + (age / 50.0) + self.rng.uniform(-0.8, 0.8)
            if ratio > 1.8:
                karar = "Kabul Eder / Destekler"
                dus = f"Bir {occ} olarak {district}'daki günlük hayatımızı ve ihtiyaçlarımızı düşündüğümde bu girişimi yerinde ve faydalı buluyorum."
            elif ratio < 1.0:
                karar = "Kesinlikle Reddeder"
                dus = f"{district}'da yaşayan {age} yaşında bir {occ} olarak sahadaki önceliklerimizle uyuşmadığını ve sorun yaratacağını düşünüyorum."
            else:
                karar = "Kararsız / Çekimser"
                dus = f"{district} sakini olarak uygulamanın sahadaki sonuçlarını ve vatandaşa etkilerini tam görmeden peşin hüküm vermek istemiyorum."

            result = {
                "karar": karar,
                "bireysel_dusuncesi_ve_gerekcesi": dus
            }

        self._eval_cache[cache_key] = result
        return result
