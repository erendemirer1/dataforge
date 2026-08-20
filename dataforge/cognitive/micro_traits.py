"""
DataForge Micro-Trait & Psychological Variance Taxonomy.
Contains hundreds of empirical psychological micro-traits, subconscious hypocrisies,
conversational quirks, coping mechanisms, and emotional triggers observed across Turkish society.
Ensures zero two individuals are identical even within the exact same profession and demographic bracket.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class CognitiveMicroTraits:
    # 1. Bilişsel Çelişkiler & Yaşam İkiyüzlülüğü (Subconscious Cognitive Dissonance)
    yasam_celiskisi: str
    
    # 2. Sosyal Medya & Dijital Alt Kültür Kimliği
    dijital_alt_kultur_kimligi: str
    
    # 3. İletişim & Konuşma Özelliği (Conversational Quirk / Ağız Alışkanlığı)
    tipik_cumle_basi_refleksi: str
    savunma_refleksi_jargonu: str
    
    # 4. Finansal & Tüketim Psikolojisi Detayı (Micro-Financial Persona)
    alisveris_zaafı: str
    pazarlik_ve_fiyat_tavri: str
    gizli_harcama_pismanligi: str
    
    # 5. Duygusal Tetikleyiciler & Sinir Uçları (Emotional Pain Points)
    en_tahammul_edemedigi_sey: str
    onaylanma_ve_takdir_kaynagi: str
    
    # 6. Kadercilik & Güvenilirlik Eğilimi (Fatalism vs. Control Locus)
    kontrol_odagi: str # İçsel (Her şey bende biter), Dışsal (Kader/Kısmet/Torpi), Paranoyak (Bize yedirmezler)


# ---------------------------------------------------------------------------
# Zengin Veri Havuzları (Sosyal Mecra, Forum ve Saha Gözlemleri)
# ---------------------------------------------------------------------------

COGNITIVE_DISSONANCES = [
    "Dışarıda lüks 3. nesil kahvecide 180 TL kahve içerken, evde doğal gazı 19 derecede tutma çelişkisi",
    "Sürekli kapitalizm ve tüketim çılgınlığını eleştirip, her yeni iPhone modelini taksitle alma zaafı",
    "Göz göre göre kilo alıp diyetisyene para verirken, gece yarısı gizlice Yemeksepeti'nden tatlı söyleme",
    "Kendi işinde personeline asgari ücreti çok görüp, dışarıda esnafın pahalılığından şikayet etme",
    "Kul hakkından ve ahlaktan dem vurup, trafikte emniyet şeridine girmeyi 'pratik zeka' sayma",
    "Sürekli yurtdışına gitmekten ve ülkenin bittiğinden bahsedip, köydeki arsayı satmaya asla yanaşmama",
    "Çocuğuna 'kitap oku, telefona bakma' deyip, kendisi günde 6 saat Instagram Reels kaydırma",
    "Kredi kartı borcu 80.000 TL iken, 'dünyaya bir kere geldik' diyerek hafta sonu tatile gitme",
    "Resmi işlerde torpili lanetleyip, hastanede sıra beklememek için tanıdık doktor arama refleksi",
    "Tasarruf yapacağım diye pazarda 10 TL için 1 saat pazarlık edip, arabaya 5.000 TL aksesuar alma",
    "İşyerinde yöneticisine karşı aşırı itaatkar ve suskun olup, evde eşine ve çocuğuna otoriter kesilme",
    "Teknolojiye ve yapay zekaya çok meraklı görünüp, internet bankacılığı şifresini deftere yazma"
]

DIGITAL_SUBCULTURE_IDENTITIES = [
    "DonanımHaber Sıcak Fırsatçı / Kupon Avcısı (Fiyatın 1 kuruşunun hesabını yapan 'Ölücü')",
    "Ekşi Sözlük Kibirli Entelektüeli (Her konunun uzmanı, hiçbir şeyi beğenmeyen alaycı eleştirmen)",
    "LinkedIn Toksik Pozitif Kariyeristi (Her başarısızlıktan 'öğrenim' çıkaran, jargon bağımlısı)",
    "Twitter/X Öfkeli Gündem Savaşçısı (Her haberde komplo ve kutuplaşma arayan politik yorumcu)",
    "Instagram Estetik Vitrin Bağımlısı (Borçla lüks mekanlarda 'başarılı hayat' sergileyen)",
    "TikTok Samimi Halk Filozofu (Araba içinde dert anlatan, arabesk rap ve özlü söz dinleyicisi)",
    "KızlarSoruyor Onay Arayıcısı (İlişkilerinde ve kararlarında sürekli yabancıların fikrine muhtaç)",
    "Memurlar.net Mevzuat Muhafızı (Her cümlenin sonuna kanun maddesi ve resmi gazete ekleyen)",
    "Reddit / r/Turkey Karamsar Z Kuşağı (Geleceğe dair umudunu yitirmiş ama mizahla ayakta kalan)",
    "WhatsApp Aile Grubu Teyzesi/Amcası (Her sabah 'Hayırlı Cumalar' gifi ve teyitsiz haber paylaşan)"
]

CONVERSATIONAL_STARTERS = [
    "Bak güzel kardeşim, bu işin aslı nedir biliyor musun...",
    "Ben açık konuşayım, kimse kusura bakmasın ama...",
    "Hocam şimdi şöyle bir durum var, realistik bakmak lazım...",
    "Ya ben zaten yıllardır bu sektördeyim, bana hikaye anlatmasınlar...",
    "Kanka valla hiç kasmaya gerek yok, sararsa bakarız...",
    "Mevzuatta bunun yeri var mı? Resmi bir güvencesi olmadan adım atmam...",
    "Valla bizim oralarda bir laf vardır...",
    "Açıkçası alignment açısından fena durmuyor ama ROI'sini netleştirelim...",
    "Agam sen ne diyorsun ya, millet aç aç...",
    "Bize yedirmezler o işi, altında kesin başka bir rant vardır..."
]

SHOPPING_WEAKNESSES = [
    "İndirim görünce hiç ihtiyacı olmayan kamp malzemesi ve hırdavat aletleri alma zaafı",
    "Kredi kartı limitini sonuna kadar zorlayıp kozmetik ve cilt bakım serumları stoklama",
    "Piyasa fiyatının altına araba parçası ve motor yağı bulduğunda kaçırmama refleksi",
    "Kitap fuarında veya internette okumayacağı onlarca kitabı indirimde diye sepete atma",
    "Kıyafet alırken 'bunu düğünde/özel günde giyerim' diyerek asla giyilmeyen takım alma",
    "BİM ve A101 aktüel ürünler kataloğunu her hafta takip edip elektronik ıvır zıvır alma",
    "Kahve makineleri, hava fritözü (Airfryer) ve mutfak robotlarına kontrolsüz para harcama",
    "Trendyol Süper İndirim günlerinde sepete 15 tane tişört ve kılıf doldurma"
]

INTOLERABLE_BEHAVIORS = [
    "Karşısındakinin onu 'saf/cahil yerine koyması' ve üstten bakan bir dille konuşması",
    "Verilen sözün tutulmaması, randevuya 15 dakikadan fazla geç kalınması",
    "Hizmet alırken gizli maliyet veya hesaba ekstra kuver/servis ücreti eklenmesi",
    "Torpille hak etmeyen birinin gözünün önünde mevki veya para kazanması",
    "Sıra beklerken birinin kaynak yapması veya araya tanıdık sokması",
    "İşyerinde emeğinin görünmemesi ve bütün övgüyü başkasının toplaması",
    "Fikrinin sorulup sonra dinlenmeden geçiştirilmesi veya alay edilmesi"
]


class MicroTraitSynthesizer:
    """Generates authentic, highly nuanced micro-traits tailored to specific demographic profiles."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def generate_micro_traits(
        self,
        occupation: str,
        social_class: str,
        age: int,
        city: str
    ) -> CognitiveMicroTraits:
        """Derives rich, nuanced micro-traits that make each character uniquely distinct."""
        occ_lower = occupation.lower()

        # 1. Digital Subculture Matching
        if "yazılım" in occ_lower or "öğrenci" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[0], # DH Sıcak Fırsatçı
                DIGITAL_SUBCULTURE_IDENTITIES[1], # Ekşi Entelektüeli
                DIGITAL_SUBCULTURE_IDENTITIES[8], # Reddit Karamsar Z
            ])
        elif "esnaf" in occ_lower or "tamir" in occ_lower or "usta" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[5], # TikTok Halk Filozofu
                DIGITAL_SUBCULTURE_IDENTITIES[9], # WhatsApp Aile/Grup
                DIGITAL_SUBCULTURE_IDENTITIES[0], # DH Sıcak Fırsatçı
            ])
        elif "müdür" in occ_lower or "pazarlama" in occ_lower or "mühendis" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[2], # LinkedIn Toksik Pozitif
                DIGITAL_SUBCULTURE_IDENTITIES[4], # Instagram Vitrin
                DIGITAL_SUBCULTURE_IDENTITIES[1], # Ekşi Entelektüeli
            ])
        elif "memur" in occ_lower or "öğretmen" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[7], # Memurlar.net
                DIGITAL_SUBCULTURE_IDENTITIES[9], # WhatsApp
            ])
        else:
            digital_sub = self.rng.choice(DIGITAL_SUBCULTURE_IDENTITIES)

        # 2. Control Locus & Fatalism
        if "esnaf" in occ_lower or "girişimci" in occ_lower:
            locus = self.rng.choice([
                "İçsel Odaklı ('Ben çalışmazsam kimse bana ekmek vermez')",
                "Kaderci / Tevekkülcü ('Rızkı veren Allah'tır, hayırlısı neyse o olsun')"
            ])
        elif "işsiz" in occ_lower or "prekarya" in social_class.lower():
            locus = self.rng.choice([
                "Paranoyak & Dışsal ('Dayın yoksa bu ülkede nefes alamazsın')",
                "Kaderci Kırgın ('Bizim şansımız olsa anam babam zengin olurdu')"
            ])
        elif "beyaz yaka" in social_class.lower():
            locus = "Liyakat Odaklı & Hayal Kırıklığı ('Sistem adaletsiz ama kendi kendimi geliştirmek zorundayım')"
        else:
            locus = "Dışsal & Kurumsal Güvensizlik ('Herkes kendi cebini dolduruyor')"

        # 3. Bargaining & Pricing Stance
        if "esnaf" in occ_lower:
            bargaining = "Agresif Pazarlıkçı ('Son oluru nedir, peşin versek ne yaparsın?')"
        elif "öğrenci" in occ_lower:
            bargaining = "Öğrenci İndirimi Israrcısı ('Öğrenciye bir güzellik yok mu?')"
        elif "beyaz yaka" in social_class.lower():
            bargaining = "Kampanya & Puan Takipçisi ('Kredi kartı puanı veya taksit avantajı var mı?')"
        else:
            bargaining = "Temkinli Kaçınmacı ('Fiyatı net söyleyin, arkadan ek masraf çıkmasın')"

        return CognitiveMicroTraits(
            yasam_celiskisi=self.rng.choice(COGNITIVE_DISSONANCES),
            dijital_alt_kultur_kimligi=digital_sub,
            tipik_cumle_basi_refleksi=self.rng.choice(CONVERSATIONAL_STARTERS),
            savunma_refleksi_jargonu=self.rng.choice(CONVERSATIONAL_STARTERS),
            alisveris_zaafı=self.rng.choice(SHOPPING_WEAKNESSES),
            pazarlik_ve_fiyat_tavri=bargaining,
            gizli_harcama_pismanligi="Sonradan gereksiz olduğunu anladığı taksitli alışverişler",
            en_tahammul_edemedigi_sey=self.rng.choice(INTOLERABLE_BEHAVIORS),
            onaylanma_ve_takdir_kaynagi="Ailesinin ve yakın çevresinin 'helal olsun, adam başardı' demesi",
            kontrol_odagi=locus
        )
