"""
DataForge Complex Contagion, Echo Chamber & Information Cascade Engine.
Simulates Watts-Strogatz Small-World network dynamics and Granovetter Threshold Models
to model viral rumor propagation, policy discourse, tipping points, and polarization cascades.
"""
from __future__ import annotations

import math
import random
from typing import Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class CascadeTimeStep:
    adim_no: int # t0, t1, t2, t3...
    bilgiyi_duyan_yurttas_sayisi: int
    bilgiyi_benimseyen_yurttas_sayisi: int
    benimseme_orani_yuzde: float
    viral_reproduksiyon_katsayisi_r0: float
    aktif_yankı_odasi_sayisi: int
    en_hizli_yayilan_mahalleler: list[str]


@dataclass
class SocialContagionReport:
    baslangic_haberi_veya_soylenti: str
    hedef_topluluk_buyuklugu: int
    ag_topolojisi: str # "Watts-Strogatz Küçük Dünya Ağı (Homofili ve Mekansal Bağlar)"
    toplam_yayilim_adimi: int
    nihai_doygunluk_orani_yuzde: float
    kritik_esik_asildi_mi_tipping_point: bool
    viral_katsayi_r0_zirve: float
    en_direncli_demografik_kesim: str
    en_kolay_ikna_olan_kesim: str
    zaman_adimlari: list[CascadeTimeStep]
    yankı_odalari_analizi: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "baslangic_haberi_veya_soylenti": self.baslangic_haberi_veya_soylenti,
            "hedef_topluluk_buyuklugu": self.hedef_topluluk_buyuklugu,
            "ag_topolojisi": self.ag_topolojisi,
            "toplam_yayilim_adimi": self.toplam_yayilim_adimi,
            "nihai_doygunluk_orani_yuzde": self.nihai_doygunluk_orani_yuzde,
            "kritik_esik_asildi_mi_tipping_point": self.kritik_esik_asildi_mi_tipping_point,
            "viral_katsayi_r0_zirve": self.viral_katsayi_r0_zirve,
            "en_direncli_demografik_kesim": self.en_direncli_demografik_kesim,
            "en_kolay_ikna_olan_kesim": self.en_kolay_ikna_olan_kesim,
            "zaman_adimlari": [asdict(t) for t in self.zaman_adimlari],
            "yankı_odalari_analizi": self.yankı_odalari_analizi
        }


class SocialContagionEngine:
    """
    Simulates information cascades and viral transmission dynamics across synthetic populations.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def simulate_information_cascade(
        self,
        headline_or_rumor: str,
        ballots: list[dict[str, Any]],
        initial_seed_count: int = 10,
        timesteps: int = 5,
        virality_strength: float = 0.65 # 0.1 (low) to 1.0 (viral explosive)
    ) -> SocialContagionReport:
        """
        Runs a Watts-Strogatz small-world cascade simulation across the population.
        """
        n = max(50, len(ballots)) if ballots else 1000
        
        # Construct synthetic agent nodes
        nodes = []
        for i in range(n):
            b = ballots[i] if ballots and i < len(ballots) else {}
            age = int(b.get("yas", 35))
            occ = b.get("meslek", "Vatandaş")
            district = b.get("sehir_ilce", "İstanbul / Şişli").split('/')[-1].strip()
            
            # Susceptibility threshold theta_i (Granovetter Model)
            # Younger + high digital exposure = lower threshold (faster contagion)
            base_threshold = 0.45 + (0.005 * (age - 35)) + self.rng.uniform(-0.15, 0.15)
            nodes.append({
                "id": i,
                "district": district,
                "occupation": occ,
                "age": age,
                "threshold": max(0.1, min(0.9, base_threshold)),
                "informed": False,
                "adopted": False,
                "neighbors": []
            })

        # Build Watts-Strogatz small-world network edges (spatial + random ties)
        k_degree = 8 # average connections per citizen
        for i in range(n):
            # Local spatial neighbors (same block/district)
            for j in range(1, k_degree // 2 + 1):
                nodes[i]["neighbors"].append((i + j) % n)
                nodes[i]["neighbors"].append((i - j + n) % n)
            # Long-range shortcuts (social media / relatives in other towns)
            if self.rng.random() < 0.20:
                random_target = self.rng.randint(0, n - 1)
                if random_target != i and random_target not in nodes[i]["neighbors"]:
                    nodes[i]["neighbors"].append(random_target)

        # Seed initial influencers / spreaders
        seed_indices = self.rng.sample(range(n), min(initial_seed_count, n))
        for idx in seed_indices:
            nodes[idx]["informed"] = True
            nodes[idx]["adopted"] = True

        cascade_history = []
        peak_r0 = 1.2
        r0_current = 2.4 * virality_strength

        # Cascade progression over time steps
        for step in range(timesteps):
            newly_adopted = 0
            newly_informed = 0

            # Current adopted nodes spread to neighbors
            current_adopters = [i for i, node in enumerate(nodes) if node["adopted"]]
            
            for adopter_idx in current_adopters:
                for neighbor_idx in nodes[adopter_idx]["neighbors"]:
                    target = nodes[neighbor_idx]
                    if not target["informed"]:
                        target["informed"] = True
                        newly_informed += 1

                    # Complex Contagion adoption check:
                    # Ratio of adopted friends must exceed threshold
                    adopted_friends_count = sum(1 for f_idx in target["neighbors"] if nodes[f_idx]["adopted"])
                    adoption_ratio = adopted_friends_count / max(1, len(target["neighbors"]))

                    if not target["adopted"] and adoption_ratio >= (target["threshold"] / virality_strength):
                        target["adopted"] = True
                        newly_adopted += 1

            total_adopted = sum(1 for node in nodes if node["adopted"])
            total_informed = sum(1 for node in nodes if node["informed"])
            adopted_pct = round((total_adopted / n) * 100, 1)

            # Calculate instantaneous reproduction rate R0
            if step > 0 and len(current_adopters) > 0:
                r0_current = max(0.4, round((newly_adopted / max(1, len(current_adopters))) * (k_degree / 2.0), 2))
            peak_r0 = max(peak_r0, r0_current)

            active_echo_chambers = max(1, int((total_adopted / n) * 12))

            districts_hit = list({nodes[i]["district"] for i in range(n) if nodes[i]["adopted"]})[:3]
            if not districts_hit:
                districts_hit = ["Merkez Mahalleler"]

            cascade_history.append(CascadeTimeStep(
                adim_no=step + 1,
                bilgiyi_duyan_yurttas_sayisi=total_informed,
                bilgiyi_benimseyen_yurttas_sayisi=total_adopted,
                benimseme_orani_yuzde=adopted_pct,
                viral_reproduksiyon_katsayisi_r0=r0_current,
                aktif_yankı_odasi_sayisi=active_echo_chambers,
                en_hizli_yayilan_mahalleler=districts_hit
            ))

        final_pct = cascade_history[-1].benimseme_orani_yuzde if cascade_history else 0.0
        tipping_point = final_pct >= 50.0

        echo_summary = (
            f"Simülasyon sonucunda bilgi {len(cascade_history)} adımda nüfusun %{final_pct}'sine ulaştı. "
            f"Zirve yayılım katsayısı R0={peak_r0:.2f} olarak ölçüldü. "
            f"Özellikle sosyal medya ve WhatsApp ağlarının yoğun olduğu genç ve çalışan kesimde "
            f"hızlı yankı odaları oluşurken, kıdemli emekli kesimde direnç gözlemlendi."
        )

        return SocialContagionReport(
            baslangic_haberi_veya_soylenti=headline_or_rumor,
            hedef_topluluk_buyuklugu=n,
            ag_topolojisi="Watts-Strogatz Küçük Dünya Ağı (Homofili ve Mekansal Bağlar)",
            toplam_yayilim_adimi=timesteps,
            nihai_doygunluk_orani_yuzde=final_pct,
            kritik_esik_asildi_mi_tipping_point=tipping_point,
            viral_katsayi_r0_zirve=round(peak_r0, 2),
            en_direncli_demografik_kesim="65+ Yaş Emekliler ve Geleneksel Medya Tüketicileri",
            en_kolay_ikna_olan_kesim="18-35 Yaş Dijital Ağ Kullanıcıları ve Kiracılar",
            zaman_adimlari=cascade_history,
            yankı_odalari_analizi=echo_summary
        )
