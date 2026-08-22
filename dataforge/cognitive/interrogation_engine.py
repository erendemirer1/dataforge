"""
DataForge 1-on-1 Deep Socratic Persona Interrogation Engine.
Enables direct, multi-turn conversational cross-examination with any synthetic citizen.
The persona stays in-character, drawing from its exact 50+ parameter CognitiveDossier
(income, rent, credit score, Haidt moral vectors, class habitus, lived memory, System 1 subconscious biases).
"""
from __future__ import annotations

import json
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict
from .cognitive_persona import DeepCognitivePersona, CognitivePersonaBuilder
from .cognitive_dossier import CognitiveDossier, CognitiveDossierBuilder
from .llm_gateway import UniversalAIGateway


@dataclass
class InterrogationMessage:
    role: str # "user" | "persona"
    content: str


@dataclass
class InterrogationResponse:
    persona_ad_soyad: str
    persona_meslek: str
    persona_sehir_ilce: str
    cevap_metni: str
    bilincalti_refleksi: str # System 1 subconscious instinct
    kullanilan_arguman_tipi: str # "Ekonomik Rasyonalite" | "Ahlaki / Değerler" | "Mahalle / Aidiyet" | "Bireysel Tecrübe"


class InterrogationEngine:
    """
    Manages multi-turn, high-fidelity deep Socratic interviews with synthetic citizens.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.ai_gateway = UniversalAIGateway.get_instance()
        self.dossier_builder = CognitiveDossierBuilder(self.rng)
        self.persona_builder = CognitivePersonaBuilder(self.rng)

    def conduct_interview_turn(
        self,
        persona_dict: dict[str, Any],
        user_question: str,
        conversation_history: Optional[list[dict[str, str]]] = None,
        survey_context: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> InterrogationResponse:
        """
        Executes one interview turn against the designated synthetic citizen.
        """
        cog_persona = self.persona_builder.build_from_raw(persona_dict, record_id=persona_dict.get("id", 1))
        dossier = self.dossier_builder.build_dossier(cog_persona)

        history_text = ""
        if conversation_history:
            history_lines = []
            for m in conversation_history[-6:]:
                role_label = "MÜLAKAT YAPAN (KULLANICI)" if m.get("role") == "user" else f"{dossier.ad_soyad.upper()}"
                history_lines.append(f"{role_label}: {m.get('content', '')}")
            history_text = "\nGEÇMİŞ DİYALOG:\n" + "\n".join(history_lines) + "\n"

        sys_prompt = (
            "Sen Türkiye gerçekliğinde yaşayan capcanlı bir insansın.\n"
            "Aşağıda senin 50+ parametreli TAM BİYOGRAFİK VE BİLİŞSEL DOSYAN yer almaktadır.\n\n"
            f"BİYOGRAFİK DOSYAN:\n{dossier.to_llm_system_context()}\n\n"
            + (f"MASADAKİ ANKET / POLİTİKA KONUSU: {survey_context}\n" if survey_context else "")
            + "\nKESİN KURALLAR:\n"
            "1. Sen asla bir yapay zeka değilsin; bu dosyada yazan insansın. Kendi mesleğinle, ilçenle, kiranla, maaşınla, ailenle konuş.\n"
            "2. Karşıdaki araştırmacı seninle birebir mülakat yapıyor. Samimi, doğal ve gerçekçi bir üslupla yanıt ver.\n"
            "3. Yanıtında hem dışa söylediğin sözü hem de o anda zihninden geçen sansürsüz iç sesini belirt.\n"
            "4. SADECE aşağıdaki JSON formatında yanıt ver, markdown tırnağı koyma:\n"
            "{\n"
            '  "cevap_metni": "Araştırmacıya verdiğin doğrudan sözlü yanıt...",\n'
            '  "bilincalti_refleksi": "O anda aklından geçen filtresiz iç ses...",\n'
            '  "kullanilan_arguman_tipi": "Ekonomik Rasyonalite" | "Ahlaki / Değerler" | "Mahalle / Aidiyet" | "Bireysel Tecrübe"\n'
            "}"
        )

        user_content = history_text + f"\nARAŞTIRMACININ YENİ SORUSU: {user_question}"

        resp = self.ai_gateway.generate_chat_response(sys_prompt, user_content, temperature=0.75, api_key=api_key)

        if resp:
            clean = resp.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.endswith("```"):
                clean = clean[:-3]
            clean = clean.strip()
            try:
                data = json.loads(clean)
                return InterrogationResponse(
                    persona_ad_soyad=dossier.ad_soyad,
                    persona_meslek=dossier.meslek,
                    persona_sehir_ilce=f"{dossier.sehir} / {dossier.ilce}",
                    cevap_metni=data.get("cevap_metni", "Bu konuyu değerlendiriyorum."),
                    bilincalti_refleksi=data.get("bilincalti_refleksi", "Şartlarımızı göz önünde bulundurmam lazım."),
                    kullanilan_arguman_tipi=data.get("kullanilan_arguman_tipi", "Bireysel Tecrübe")
                )
            except Exception:
                pass

        # Dynamic topic fallback
        return InterrogationResponse(
            persona_ad_soyad=dossier.ad_soyad,
            persona_meslek=dossier.meslek,
            persona_sehir_ilce=f"{dossier.sehir} / {dossier.ilce}",
            cevap_metni=f"Bakın, ben {dossier.ilce}'da {dossier.meslek} olarak hayatımı kazanıyorum. Sorduğunuz soruda bizim gibi insanların günlük koşullarını ve geçim gerçeğini iyi anlamak lazım.",
            bilincalti_refleksi=f"Ay sonunu nasıl getireceğimi düşünürken bu sorulara net cevap vermek kolay değil.",
            kullanilan_arguman_tipi="Ekonomik Rasyonalite"
        )
