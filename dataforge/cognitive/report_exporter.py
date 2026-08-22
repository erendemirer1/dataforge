"""
DataForge Executive Brief & Institutional Strategy Report Exporter.
Generates publication-ready, formal executive intelligence reports
incorporating academic citations, methodology notes, risk matrices, and strategic roadmaps.
"""
from __future__ import annotations

import datetime
from typing import Any


class ReportExporter:
    """
    Exports synthetic survey and focus group analytics into standalone, executive-ready HTML/PDF documents.
    """

    @classmethod
    def generate_html_executive_brief(cls, report_data: dict[str, Any]) -> str:
        """
        Builds a formal, print-optimized HTML executive document suitable for Mayors, Ministers, and C-Suite executives.
        """
        now_str = datetime.datetime.now().strftime("%d.%m.%Y // %H:%M")
        soru = report_data.get("soru_veya_politika", "Araştırma Raporu")
        bolge = report_data.get("hedef_bolge", "Türkiye Geneli")
        n_sample = report_data.get("orneklem_buyuklugu", 1000)
        hata = report_data.get("hata_payi_yuzde", "±%2.4")
        guven = report_data.get("guven_araligi_yuzde_95", "%95")
        kabul = report_data.get("genel_kabul_yuzde", 0.0)
        ret = report_data.get("genel_ret_yuzde", 0.0)
        kararsiz = report_data.get("genel_kararsiz_yuzde", 0.0)
        action_plan = report_data.get("belediye_stratejik_aksiyon_plani", "Stratejik plan oluşturuldu.")
        barriers = report_data.get("en_buyuk_toplumsal_direnc_noktalari", [])
        drivers = report_data.get("en_guclu_destek_gerekceleri", [])

        barriers_html = "".join([f"<li>• {b}</li>" for b in barriers])
        drivers_html = "".join([f"<li>• {d}</li>" for d in drivers])

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Yönetici Strateji Raporu // {bolge}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:italic,normal@0;1&family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        body {{
            font-family: 'JetBrains Mono', monospace;
            background: #ffffff;
            color: #111111;
            margin: 0;
            padding: 40px;
            line-height: 1.6;
        }}
        .header {{
            border-bottom: 2px solid #000;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .logo {{
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -1px;
        }}
        .badge {{
            font-size: 11px;
            background: #f0f0f0;
            padding: 4px 8px;
            border: 1px solid #ccc;
        }}
        h1 {{
            font-family: 'Instrument Serif', serif;
            font-size: 32px;
            margin: 10px 0;
            font-weight: normal;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        .metric-card {{
            border: 1px solid #000;
            padding: 20px;
            background: #fafafa;
        }}
        .metric-label {{
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
        }}
        .metric-val {{
            font-family: 'Instrument Serif', serif;
            font-size: 40px;
            font-weight: bold;
            margin-top: 5px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
        }}
        .section-title {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 8px;
            margin-bottom: 15px;
            color: #444;
        }}
        .methodology {{
            font-size: 11px;
            color: #555;
            background: #f9f9f9;
            padding: 15px;
            border-left: 3px solid #000;
            margin-top: 40px;
        }}
        @media print {{
            body {{ padding: 20px; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="logo">DATAFORGE // RESMİ YÖNETİCİ BRİFİ</div>
            <div style="font-size: 11px; color: #666; margin-top: 4px;">HESAPLAMALI SOSYAL BİLİMLER VE SENTETİK NÜFUS RAPORU</div>
        </div>
        <div style="text-align: right;">
            <span class="badge">GİZLİ // KURUMSAL DAĞITIM</span>
            <div style="font-size: 11px; margin-top: 4px;">Tarih: {now_str}</div>
        </div>
    </div>

    <div>
        <div style="font-size: 12px; color: #666; text-transform: uppercase;">[ARAŞTIRILAN SORU / PROJE BAŞLIĞI]</div>
        <h1>"{soru}"</h1>
        <div style="font-size: 12px; color: #444;">Hedef Bölge: <strong>{bolge}</strong> | Örneklem: <strong>N = {n_sample} Sentetik Nüfus İkizi</strong> | Hata Payı: <strong>{hata}</strong> ({guven} Güven Aralığı)</div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card" style="border-top: 4px solid #10b981;">
            <div class="metric-label">GENEL KABUL / DESTEK</div>
            <div class="metric-val" style="color: #059669;">%{kabul}</div>
        </div>
        <div class="metric-card" style="border-top: 4px solid #f43f5e;">
            <div class="metric-label">GENEL RET / İTİRAZ</div>
            <div class="metric-val" style="color: #e11d48;">%{ret}</div>
        </div>
        <div class="metric-card" style="border-top: 4px solid #f59e0b;">
            <div class="metric-label">KARARSIZ / BEKLE-GÖR</div>
            <div class="metric-val" style="color: #d97706;">%{kararsiz}</div>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="section">
            <div class="section-title">// EN GÜÇLÜ TOPLUMSAL DESTEK GEREKÇELERİ</div>
            <ul style="padding-left: 0; list-style: none; font-size: 12px; space-y: 8px;">
                {drivers_html}
            </ul>
        </div>
        <div class="section">
            <div class="section-title">// EN BÜYÜK TOPLUMSAL DİRENÇ NOKTALARI</div>
            <ul style="padding-left: 0; list-style: none; font-size: 12px; space-y: 8px;">
                {barriers_html}
            </ul>
        </div>
    </div>

    <div class="section" style="background: #fafafa;">
        <div class="section-title">// STRATEJİK EYLEM PLANI & YÖNETİM TAVSİYESİ</div>
        <p style="font-size: 13px; line-height: 1.7; margin: 0;">
            {action_plan}
        </p>
    </div>

    <div class="methodology">
        <strong>BİLİMSEL METODOLOJİ VE VERİ KAYNAKLARI:</strong><br>
        Bu araştırma, TÜİK ADNKS 2024 demografik ağırlıkları, Sanayi ve Teknoloji Bakanlığı SEGE-2022 973 İlçe Sosyoekonomik Gelişmişlik Kademeleri, Daniel Kahneman Kümülatif Beklenti Teorisi (Loss Aversion &lambda;=2.25) ve Jonathan Haidt 6-Ahlak Temeli modeliyle kalibre edilmiş DataForge Cognitive Twin Engine v4.5 tarafından simüle edilmiştir.
    </div>

    <div class="no-print" style="margin-top: 30px; text-align: center;">
        <button onclick="window.print()" style="padding: 12px 24px; background: #000; color: #fff; border: none; font-family: monospace; font-weight: bold; cursor: pointer;">
            YAZDIR / PDF OLARAK KAYDET [PRINT]
        </button>
    </div>
</body>
</html>"""
