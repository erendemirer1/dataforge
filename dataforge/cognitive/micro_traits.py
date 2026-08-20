"""
DataForge Micro-Trait & Psychological Variance Taxonomy.
Contains empirical psychological micro-traits, subconscious hypocrisies,
and emotional triggers observed across Turkish society.
Zero canned robotic phrases: Ensures personas speak naturally from their own unique lived experience.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class CognitiveMicroTraits:
    # 1. Bilişsel Çelişkiler & Yaşam İkiyüzlülüğü (Subconscious Cognitive Dissonance)
    yasam_celiskisi: str
    
    # 2. Sosyal Medya & Dijital Alt Kültür Kimliği
    dijital_alt_kultur_kimligi: str
    
    # 3. Finansal & Tüketim Psikolojisi Detayı (Micro-Financial Persona)
    alisveris_zaafı: str
    pazarlik_ve_fiyat_tavri: str
    
    # 4. Duygusal Tetikleyiciler & Sinir Uçları (Emotional Pain Points)
    en_tahammul_edemedigi_sey: str
    onaylanma_ve_takdir_kaynagi: str
    
    # 5. Kadercilik & Güvenilirlik Eğilimi (Fatalism vs. Control Locus)
    kontrol_odagi: str


COGNITIVE_DISSONANCES = [
    "Dışarıda lüks 3. nesil kahvecide 180 TL kahve içerken, evde doğal gazı 19 derecede tutma çelişkisi",
    "Sürekli kapitalizm ve tüketim çılgınlığını eleştirip, her yeni telefon modelini taksitle alma zaafı",
    "Göz göre göre kilo alıp diyetisyene para verirken, gece yarısı gizlice sipariş verme",
    "Kendi işinde personeline asgari ücreti çok görüp, dışarıda esnafın pahalılığından şikayet etme",
    "Kul hakkından ve ahlaktan dem vurup, trafikte emniyet şeridine girmeyi 'pratik zeka' sayma",
    "Sürekli yurtdışına gitmekten ve ülkenin bittiğinden bahsedip, köydeki arsayı satmaya asla yanaşmama",
    "Çocuğuna 'kitap oku, telefona bakma' deyip, kendisi günde 6 saat sosyal medyada gezinme",
    "Kredi kartı borcu yüklüyken, 'dünyaya bir kere geldik' diyerek hafta sonu tatile gitme",
    "Resmi işlerde torpili lanetleyip, hastanede sıra beklememek için tanıdık doktor arama refleksi",
    "Tasarruf yapacağım diye pazarda 10 TL için pazarlık edip, arabaya binlerce lira harcama",
    "İşyerinde amirine karşı aşırı itaatkar olup, evde otoriter kesilme",
    "Teknolojiye meraklı görünüp, internet şifresini deftere yazma"
]

DIGITAL_SUBCULTURE_IDENTITIES = [
    "DonanımHaber Sıcak Fırsatçı / Kupon Avcısı (Fiyatın 1 kuruşunun hesabını yapan tüketici)",
    "Ekşi Sözlük Entelektüeli (Her konuyu eleştiren, sorgulayıcı bakış açısı)",
    "LinkedIn Kariyeristi (Sürekli kişisel gelişim ve network odaklı)",
    "Twitter/X Gündem Takipçisi (Haberleri ve toplumsal olayları anlık takip eden)",
    "Instagram Vitrin Kullanıcısı (Sosyal onay ve görsel estetik odaklı)",
    "TikTok Samimi Halk Dili (Halkın içinden, samimi ve dertleşme odaklı)",
    "Memurlar.net Mevzuat Takipçisi (Resmi prosedür, güvence ve kuralcı yaklaşım)",
    "Reddit / Gençlik Topluluğu (Karamsar ama mizahla ayakta kalan Z kuşağı)"
]

SHOPPING_WEAKNESSES = [
    "İndirim görünce hiç ihtiyacı olmayan hırdavat ve kamp malzemeleri alma zaafı",
    "Kredi kartı limitini zorlayıp kozmetik ve kişisel bakım ürünleri stoklama",
    "Piyasa fiyatının altına araba parçası ve alet bulduğunda kaçırmama refleksi",
    "Okumayacağı onlarca kitabı indirimde diye sepete atma zaafı",
    "Kıyafet alırken 'özel günde giyerim' diyerek asla giyilmeyen kıyafetler alma",
    "İndirim marketlerinin aktüel ürünler kataloğunu takip edip elektronik ıvır zıvır alma",
    "Mutfak aletleri ve küçük ev aletlerine bütçe ayırma zaafı"
]

INTOLERABLE_BEHAVIORS = [
    "Karşısındakinin onu 'saf/cahil yerine koyması' ve üstten bakan bir dille konuşması",
    "Verilen sözün tutulmaması, randevuya geç kalınması",
    "Hizmet alırken sonradan gizli maliyet ve ekstra ücret çıkarılması",
    "Torpille hak etmeyen birinin haksız kazanç sağlaması",
    "Sıra beklerken birinin araya kaynak yapması",
    "Emeğinin görmezden gelinmesi ve hiçe sayılması",
    "Fikrinin sorulup sonra dinlenmeden geçiştirilmesi"
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
                DIGITAL_SUBCULTURE_IDENTITIES[7], # Reddit Gençlik
            ])
        elif "esnaf" in occ_lower or "tamir" in occ_lower or "usta" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[5], # TikTok Halk
                DIGITAL_SUBCULTURE_IDENTITIES[0], # DH Sıcak Fırsatçı
            ])
        elif "müdür" in occ_lower or "pazarlama" in occ_lower or "mühendis" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[2], # LinkedIn
                DIGITAL_SUBCULTURE_IDENTITIES[4], # Instagram
                DIGITAL_SUBCULTURE_IDENTITIES[1], # Ekşi
            ])
        elif "memur" in occ_lower or "öğretmen" in occ_lower or "şehit" in occ_lower or "gazi" in occ_lower:
            digital_sub = self.rng.choice([
                DIGITAL_SUBCULTURE_IDENTITIES[6], # Memurlar.net
                DIGITAL_SUBCULTURE_IDENTITIES[3], # Twitter Gündem
            ])
        else:
            digital_sub = self.rng.choice(DIGITAL_SUBCULTURE_IDENTITIES)

        # 2. Control Locus & Fatalism
        if "esnaf" in occ_lower or "girişimci" in occ_lower:
            locus = "İçsel Odaklı ('Ben çalışmazsam kimse bana ekmek vermez')"
        elif "şehit" in occ_lower or "gazi" in occ_lower:
            locus = "Vatan, Onur ve Adalet Odaklı ('Hakkımız ve şehitlerimizin emaneti çiğnenemez')"
        elif "işsiz" in occ_lower or "prekarya" in social_class.lower():
            locus = "Dışsal ve Kırgın ('Torpilin yoksa sistem seni eziyor')"
        elif "beyaz yaka" in social_class.lower():
            locus = "Liyakat ve Adalet Arayışı ('Emeklerimizin karşılığını almak istiyoruz')"
        else:
            locus = "Temkinli & Kurumsal Güvensizlik ('Herkes kendi çıkarını düşünüyor')"

        # 3. Bargaining & Pricing Stance
        if "esnaf" in occ_lower:
            bargaining = "Pazarlıkçı ve Nakit Koruyucu"
        elif "öğrenci" in occ_lower:
            bargaining = "Öğrenci İndirimi ve Burs Hassasiyeti"
        elif "şehit" in occ_lower or "gazi" in occ_lower:
            bargaining = "Maneviyat ve İlke Odaklı (Maddiyattan Önce Onur Gelir)"
        elif "beyaz yaka" in social_class.lower():
            bargaining = "Fiyat / Performans ve Taksit Odaklı"
        else:
            bargaining = "Net ve Şeffaf Fiyat Arayışı"

        return CognitiveMicroTraits(
            yasam_celiskisi=self.rng.choice(COGNITIVE_DISSONANCES),
            dijital_alt_kultur_kimligi=digital_sub,
            alisveris_zaafı=self.rng.choice(SHOPPING_WEAKNESSES),
            pazarlik_ve_fiyat_tavri=bargaining,
            en_tahammul_edemedigi_sey=self.rng.choice(INTOLERABLE_BEHAVIORS),
            onaylanma_ve_takdir_kaynagi="Ailesinin ve toplumun gözünde onurlu ve saygın olmak",
            kontrol_odagi=locus
        )
