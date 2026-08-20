<div align="center">

# 🔨 DataForge

**Production-grade synthetic data generator with Turkish locale support**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-MVP-orange)](#)

*Startup MVP — Türkiye'nin açık kaynak sentetik veri çerçevesi*

</div>

---

## Özellikler / Features

| 🇬🇧 Feature | 🇹🇷 Özellik |
|---|---|
| 6 built-in schemas | 6 hazır şema |
| Turkish locale (names, cities, TCKN) | Türkçe yerel destek |
| Valid TCKN generation | Geçerli TCKN üretimi |
| UAVT / PTT Geo Database & SQLite | 81 İl, 973 İlçe, Posta Kodlu Adresler |
| Offline Geo Sync (`dataforge sync-geo`) | Çevrimdışı coğrafi veri senkronizasyonu |
| Referential integrity | İlişkisel bütünlük |
| JSON / CSV / SQL / Parquet export | 4 farklı çıktı formatı |
| Rich progress bars & colors | Renkli terminal arayüzü |
| Validation command | Veri doğrulama komutu |
| Interactive schema creator | Etkileşimli şema oluşturucu |

---

## Hızlı Başlangıç / Quick Start

### Kurulum / Installation

```bash
# Depoyu klonla
git clone https://github.com/dataforge/dataforge.git
cd dataforge

# Gereksinimlerle birlikte kur
pip install -e .

# Geliştirme bağımlılıkları ile
pip install -e ".[dev]"
```

### Temel Kullanım / Basic Usage

```bash
# 100 kullanıcı üret (JSON)
dataforge generate --schema users --count 100 --format json

# 500 ürün üret (CSV)
dataforge generate --schema products --count 500 --format csv

# 1000 sipariş üret (SQL)
dataforge generate --schema orders --count 1000 --format sql

# Parquet formatında log üret
dataforge generate --schema logs --count 10000 --format parquet

# Sıkıştırılmış JSON çıktısı
dataforge generate --schema transactions --count 200 --format json --compact

# Belirli dosyaya yaz
dataforge generate --schema employees --count 50 --format csv --output data/employees.csv
```

### İlişkisel Veri Üretimi / Referential Integrity

```yaml
# schema.yaml
relations:
  - users: 1000
  - products: 500
  - orders: 5000
  - transactions: 10000
```

```bash
dataforge generate --schema examples/multi_schema.yaml --format json
# output/ altında users.json, products.json, orders.json, transactions.json oluşturulur
# orders.user_id → gerçek user ID'lerinden biri
# transactions.user_id → gerçek user ID'lerinden biri
```

### Schema Komutları / Schema Commands

```bash
# Hazır şemalara bak
dataforge schema list

# Bir şemanin alanlarını incele
dataforge schema show users
dataforge schema show products

# Etkileşimli şema oluştur
dataforge schema create my_schema
# > Field: username:str
# > Field: age:int
# > Field: (boş bırak Enter'a bas)
# my_schema.yaml oluşturulur
```

### Doğrulama / Validation

```bash
# Genel doğrulama
dataforge validate data/users.json

# Şemaya göre doğrulama (TCKN, fiyat tutarlılığı vb.)
dataforge validate data/users.json --schema users
dataforge validate data/orders.csv --schema orders
dataforge validate data/products.json --schema products
```

### 🌍 Coğrafi Veri & UAVT / PTT Senkronizasyonu

```bash
# Resmi PTT & UAVT coğrafi veritabanını senkronize et (81 İl, 973 İlçe, Mahalleler, Posta Kodları)
dataforge sync-geo

# Yerel coğrafi veritabanı istatistiklerini gör
dataforge geo stats
```


---

## Hazır Şemalar / Built-in Schemas

### 👤 `users`
Türkiye'ye özgü kullanıcı profilleri:
- Geçerli TCKN (11 haneli, algoritma doğrulanmış)
- Türk telefon formatı (05XX XXX XX XX)
- 81 ilden rastgele şehir
- Yaş ile doğum tarihi tutarlılığı

### 🛏️ `products`
E-ticaret ürün katalogu:
- Category → subcategory hiyerarşisi (tutarlı)
- Kategori bazlı gerçekçi fiyat aralıkları
- Her zaman `discount_price < price`
- Unique SKU formatı

### 📦 `orders`
Sipariş kayıtları:
- `total_price = quantity × unit_price` (kesin)
- `updated_at >= created_at` (kesin)
- Gerçekçi status dağılımı (delivered %55)

### 💳 `transactions`
Finansal işlemler:
- UUID formatında transaction_id
- TRY/USD/EUR para birimleri (%75/%15/%10)
- Kategori ile tutarlı Türkçe açıklamalar

### 👥 `employees`
Çalışan kayıtları:
- Departman → pozisyon → maaş hiyerarşisi
- Kurumsal email (sahte Türk şirket domain'leri)
- Referanssal manager_id

### 📝 `logs`
Uygulama logları:
- Gerçekçi seviye dağılımı: INFO %60, DEBUG %20, WARNING %15, ERROR %4, CRITICAL %1
- Seviye ile tutarlı mesaj şablonları
- 20 farklı micro-service ismi

---

## Proje Yapısı / Project Structure

```
dataforge/
├── dataforge/
│   ├── __init__.py          # Versiyon bilgisi
│   ├── cli.py               # Typer CLI, tüm komutlar
│   ├── generators/
│   │   ├── base.py          # Soyut temel sınıf
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── transactions.py
│   │   ├── employees.py
│   │   └── logs.py
│   ├── exporters/
│   │   ├── json_exporter.py
│   │   ├── csv_exporter.py
│   │   ├── sql_exporter.py
│   │   └── parquet_exporter.py
│   ├── schemas/
│   │   ├── schema_manager.py
│   │   └── __init__.py
│   └── utils/
│       ├── tckn.py          # TCKN üretici & doğrulayıcı
│       └── turkish_data.py  # 200+ Türkçe veri
├── examples/
│   ├── multi_schema.yaml
│   └── custom_schema.yaml
├── tests/
│   ├── test_generators.py
│   └── test_tckn.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Geliştirme / Development

```bash
# Bağımlılıkları kur
pip install -e ".[dev]"

# Testleri çalıştır
pytest

# Kapsam raporu ile
pytest --cov=dataforge --cov-report=term-missing

# Linting
ruff check dataforge/
```

---

## Katkıda Bulunma / Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'feat: add my feature'`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request

### Yeni Schema Ekleme / Adding a New Schema

1. `dataforge/generators/` altında yeni bir dosya oluştur (orn. `invoices.py`)
2. `BaseGenerator`'dan miras al, `generate_one()` metodunu implemente et
3. `GENERATOR_MAP`'e ekle (`generators/__init__.py`)
4. `BUILTIN_SCHEMAS`'a açıklama ekle (`schemas/schema_manager.py`)
5. `tests/test_generators.py`'e testleri yaz

---

## Lisans / License

MIT © 2024 DataForge Team

---

<div align="center">

**İstanbul'dan ❤️ ile üretildi**

*Made with ❤️ in Istanbul*

</div>
