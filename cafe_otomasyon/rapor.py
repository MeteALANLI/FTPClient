"""Kafe Otomasyon Sistemi - Raporlama modülü."""

from cafe_otomasyon.veritabani import baglanti_al


def gunluk_satis_raporu(tarih):
    """Belirli bir günün satış raporunu döndürür."""
    conn = baglanti_al()
    ozet = conn.execute(
        """
        SELECT
            COUNT(*) AS siparis_sayisi,
            COALESCE(SUM(toplam_tutar), 0) AS toplam_gelir,
            COALESCE(SUM(CASE WHEN odeme_turu='nakit' THEN toplam_tutar ELSE 0 END), 0) AS nakit,
            COALESCE(SUM(CASE WHEN odeme_turu='kart' THEN toplam_tutar ELSE 0 END), 0) AS kart
        FROM siparisler
        WHERE durum = 'kapali' AND tarih LIKE ?
        """,
        (f"{tarih}%",)
    ).fetchone()

    urunler = conn.execute(
        """
        SELECT u.ad, SUM(sk.adet) AS toplam_adet,
               SUM(sk.adet * sk.birim_fiyat) AS toplam_tutar
        FROM siparis_kalemleri sk
        JOIN urunler u ON sk.urun_id = u.id
        JOIN siparisler s ON sk.siparis_id = s.id
        WHERE s.durum = 'kapali' AND s.tarih LIKE ?
        GROUP BY u.id
        ORDER BY toplam_adet DESC
        """,
        (f"{tarih}%",)
    ).fetchall()

    conn.close()
    return {"ozet": ozet, "urunler": urunler}


def aylik_satis_raporu(yil, ay):
    """Aylık satış raporunu döndürür."""
    conn = baglanti_al()
    tarih_pattern = f"{yil}-{ay:02d}%"

    gunluk = conn.execute(
        """
        SELECT
            SUBSTR(tarih, 1, 10) AS gun,
            COUNT(*) AS siparis_sayisi,
            SUM(toplam_tutar) AS toplam
        FROM siparisler
        WHERE durum = 'kapali' AND tarih LIKE ?
        GROUP BY gun
        ORDER BY gun
        """,
        (tarih_pattern,)
    ).fetchall()

    genel = conn.execute(
        """
        SELECT
            COUNT(*) AS siparis_sayisi,
            COALESCE(SUM(toplam_tutar), 0) AS toplam_gelir
        FROM siparisler
        WHERE durum = 'kapali' AND tarih LIKE ?
        """,
        (tarih_pattern,)
    ).fetchone()

    conn.close()
    return {"gunluk": gunluk, "genel": genel}


def en_cok_satan_urunler(limit=10):
    """En çok satan ürünleri döndürür."""
    conn = baglanti_al()
    rows = conn.execute(
        """
        SELECT u.ad, k.ad AS kategori, SUM(sk.adet) AS toplam_adet,
               SUM(sk.adet * sk.birim_fiyat) AS toplam_gelir
        FROM siparis_kalemleri sk
        JOIN urunler u ON sk.urun_id = u.id
        JOIN kategoriler k ON u.kategori_id = k.id
        JOIN siparisler s ON sk.siparis_id = s.id
        WHERE s.durum = 'kapali'
        GROUP BY u.id
        ORDER BY toplam_adet DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()
    conn.close()
    return rows


def kategori_bazli_rapor():
    """Kategori bazlı satış raporunu döndürür."""
    conn = baglanti_al()
    rows = conn.execute(
        """
        SELECT k.ad AS kategori, SUM(sk.adet) AS toplam_adet,
               SUM(sk.adet * sk.birim_fiyat) AS toplam_gelir
        FROM siparis_kalemleri sk
        JOIN urunler u ON sk.urun_id = u.id
        JOIN kategoriler k ON u.kategori_id = k.id
        JOIN siparisler s ON sk.siparis_id = s.id
        WHERE s.durum = 'kapali'
        GROUP BY k.id
        ORDER BY toplam_gelir DESC
        """,
    ).fetchall()
    conn.close()
    return rows


def masa_performans_raporu():
    """Masa bazlı performans raporunu döndürür."""
    conn = baglanti_al()
    rows = conn.execute(
        """
        SELECT m.numara AS masa_no,
               COUNT(s.id) AS siparis_sayisi,
               COALESCE(SUM(s.toplam_tutar), 0) AS toplam_gelir,
               COALESCE(AVG(s.toplam_tutar), 0) AS ortalama_tutar
        FROM masalar m
        LEFT JOIN siparisler s ON m.id = s.masa_id AND s.durum = 'kapali'
        GROUP BY m.id
        ORDER BY toplam_gelir DESC
        """,
    ).fetchall()
    conn.close()
    return rows
