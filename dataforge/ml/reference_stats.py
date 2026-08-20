# dataforge/ml/reference_stats.py

# TÜİK 2024 Eğitim Dağılımı (Yaş grubuna ve bölgeye göre)
EDUCATION_BY_AGE = {
    '65+': {'ilkokul': 0.52, 'ortaokul': 0.17, 'lise': 0.18, 'universite': 0.11, 'lisansustu': 0.02},
    '45-64': {'ilkokul': 0.28, 'ortaokul': 0.22, 'lise': 0.30, 'universite': 0.17, 'lisansustu': 0.03},
    '25-44': {'ilkokul': 0.12, 'ortaokul': 0.15, 'lise': 0.35, 'universite': 0.32, 'lisansustu': 0.06},
    '18-24': {'ilkokul': 0.03, 'ortaokul': 0.10, 'lise': 0.42, 'universite': 0.40, 'lisansustu': 0.05},
}

# TÜİK Evlenme Yaşı
AVERAGE_MARRIAGE_AGE = {'M': 27, 'F': 24}

# SGK Asgari Ücret 2025
MINIMUM_WAGE_2025 = 26005.50

# SGK kesinti oranları
SGK_EMPLOYEE_PREMIUM_RATE = 0.14
UNEMPLOYMENT_INSURANCE_RATE = 0.01

# Vergi dilimleri 2025 (Kaba tahmin)
TAX_BRACKETS_2025 = [
    (110000, 0.15),
    (230000, 0.20),
    (870000, 0.27),
    (3000000, 0.35),
    (float('inf'), 0.40)
]

# BTK Pazar Payları (Operatör)
GSM_MARKET_SHARE = {
    'Turkcell': 0.42,
    'Vodafone': 0.30,
    'Türk Telekom': 0.28
}

# Kızılay Kan Grubu Dağılımı
BLOOD_TYPE_DISTRIBUTION = {
    'A+': 0.38, 'O+': 0.30, 'B+': 0.11, 'AB+': 0.05,
    'A-': 0.07, 'O-': 0.05, 'B-': 0.02, 'AB-': 0.02
}

# TÜİK Sigara kullanımı: %28 erkek, %13 kadın
SMOKING_PREVALENCE = {'M': 0.28, 'F': 0.13}

# TÜİK Kronik hastalık (yaşa göre rastgele dağılım olasılıkları)
CHRONIC_DISEASE_PROBS = {
    '18-24': 0.05,
    '25-44': 0.10,
    '45-64': 0.35,
    '65+': 0.65
}

CHRONIC_DISEASES = ['Hipertansiyon', 'Diyabet', 'Kalp Yetmezliği', 'Astım', 'KOAH']

# TÜİK Ev sahipliği: %67.5 genel, İstanbul %52
HOMEOWNER_RATE_GENERAL = 0.675
HOMEOWNER_RATE_IST = 0.52

# Gelir segmentine göre araç markaları
VEHICLE_BRANDS_BY_INCOME = {
    'alt_gelir': ['Fiat', 'Renault', 'Dacia', 'Hyundai', 'Ford'],
    'orta_gelir': ['Volkswagen', 'Toyota', 'Peugeot', 'Honda', 'Skoda', 'Opel'],
    'ust_gelir': ['Mercedes-Benz', 'BMW', 'Audi', 'Volvo', 'Tesla', 'Jeep']
}

# Bölge gelir çarpanları (NUTS-1 / Şehir örnekleri)
REGIONAL_INCOME_MULTIPLIER = {
    'İstanbul': 1.45,
    'Ankara': 1.25,
    'İzmir': 1.25,
    'Antalya': 1.15,
    'Bursa': 1.15,
    'Diyarbakır': 0.75,
    'Van': 0.70,
    'Erzurum': 0.80,
    'Trabzon': 0.90,
}

# BDDK Kredi Kartı Limiti Çarpanı
CC_LIMIT_MULTIPLIER_MIN = 2
CC_LIMIT_MULTIPLIER_MAX = 4

# Yatırım araçları - yaş/gelir koşullu
INVESTMENT_PREFERENCES = {
    'alt_gelir': ['Altın', 'Banka Mevduatı'],
    'orta_gelir': ['Altın', 'Döviz', 'Hisse Senedi', 'Banka Mevduatı'],
    'ust_gelir': ['Hisse Senedi', 'Döviz', 'Eurobond', 'Kripto', 'Gayrimenkul', 'Fon']
}

# Süpermarket tercihleri
SUPERMARKET_BY_INCOME = {
    'alt_gelir': ['BİM', 'A101', 'ŞOK'],
    'orta_gelir': ['Migros', 'CarrefourSA', 'BİM', 'A101'],
    'ust_gelir': ['Macrocenter', 'Migros', 'CarrefourSA Gurme']
}

# Akıllı telefon model-gelir eşleşmesi
SMARTPHONE_OS_BY_INCOME = {
    'alt_gelir': {'Android': 0.90, 'iOS': 0.10},
    'orta_gelir': {'Android': 0.65, 'iOS': 0.35},
    'ust_gelir': {'iOS': 0.85, 'Android': 0.15}
}

# Streaming platform abonelik
STREAMING_PLATFORMS = ['Netflix', 'Spotify', 'YouTube Premium', 'Disney+', 'Amazon Prime', 'Exxen', 'BluTV']

# Sosyal medya kullanım - yaş matrisi
SOCIAL_MEDIA_BY_AGE = {
    '18-24': ['Instagram', 'TikTok', 'X', 'YouTube'],
    '25-44': ['Instagram', 'X', 'LinkedIn', 'YouTube'],
    '45-64': ['Facebook', 'Instagram', 'WhatsApp', 'YouTube'],
    '65+': ['Facebook', 'WhatsApp']
}

# Siyasi/dini eğilim (kaba)
RELIGIOSITY_LEVELS = ['Ateist', 'Agnostik', 'Kültürel', 'Pratik', 'Dindar']

# Tatil tercihleri - gelir
VACATION_TYPES = {
    'alt_gelir': ['Tatil yok', 'Memleket ziyareti', 'Pansiyon'],
    'orta_gelir': ['Yurt içi otel', 'Yazlık', 'Airbnb'],
    'ust_gelir': ['Yurt dışı', 'Yurt içi lüks otel', 'Villa kiralama']
}

# Restoran sıklığı
RESTAURANT_FREQ = {
    'alt_gelir': ['Hiç', 'Ayda 1-2'],
    'orta_gelir': ['Ayda 1-2', 'Haftada 1'],
    'ust_gelir': ['Haftada 2+', 'Haftada 1']
}

CITY_PLATES = {
    'Adana': '01', 'Ankara': '06', 'Antalya': '07', 'Bursa': '16', 
    'Diyarbakır': '21', 'Erzurum': '25', 'İstanbul': '34', 'İzmir': '35', 
    'Trabzon': '61', 'Van': '65'
}

UNIVERSITIES = [
    'Boğaziçi Üniversitesi', 'ODTÜ', 'İTÜ', 'Bilkent Üniversitesi', 'Koç Üniversitesi', 
    'Sabancı Üniversitesi', 'Hacettepe Üniversitesi', 'Ankara Üniversitesi', 
    'Ege Üniversitesi', 'Dokuz Eylül Üniversitesi', 'Marmara Üniversitesi', 
    'Gazi Üniversitesi', 'Anadolu Üniversitesi'
]
