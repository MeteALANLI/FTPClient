"""Kafe Otomasyon Sistemi - Masa ve sipariş yönetimi."""

from datetime import datetime
from cafe_otomasyon.veritabani import baglanti_al


# ── Masa İşlemleri ──────────────────────────────────────────────

def masalari_listele():
    """Tüm masaları durumlarıyla birlikte döndürür."""
    conn = baglanti_al()
    rows = conn.execute(
        "SELECT * FROM masalar ORDER BY numara"
    ).fetchall()
    conn.close()
    return rows


def masa_durumu_guncelle(masa_id, durum):
    """Masa durumunu günceller (bos/dolu/rezerve)."""
    conn = baglanti_al()
    conn.execute(
        "UPDATE masalar SET durum = ? WHERE id = ?", (durum, masa_id)
    )
    conn.commit()
    conn.close()


def masa_ekle(numara, kapasite=4):
    """Yeni masa ekler."""
    conn = baglanti_al()
    conn.execute(
        "INSERT INTO masalar (numara, kapasite) VALUES (?, ?)",
        (numara, kapasite)
    )
    conn.commit()
    conn.close()


# ── Sipariş İşlemleri ───────────────────────────────────────────

def siparis_ac(masa_id):
    """Masa için yeni sipariş açar ve sipariş ID döndürür."""
    conn = baglanti_al()
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.execute(
        "INSERT INTO siparisler (masa_id, tarih) VALUES (?, ?)",
        (masa_id, tarih)
    )
    siparis_id = c.lastrowid
    conn.execute("UPDATE masalar SET durum = 'dolu' WHERE id = ?", (masa_id,))
    conn.commit()
    conn.close()
    return siparis_id


def masanin_acik_siparisi(masa_id):
    """Masanın açık siparişini döndürür (varsa)."""
    conn = baglanti_al()
    row = conn.execute(
        "SELECT * FROM siparisler WHERE masa_id = ? AND durum = 'acik' "
        "ORDER BY id DESC LIMIT 1",
        (masa_id,)
    ).fetchone()
    conn.close()
    return row


def siparis_kalem_ekle(siparis_id, urun_id, adet=1, not_bilgisi=None):
    """Siparişe ürün ekler."""
    conn = baglanti_al()
    fiyat = conn.execute(
        "SELECT fiyat FROM urunler WHERE id = ?", (urun_id,)
    ).fetchone()

    if not fiyat:
        conn.close()
        return False

    conn.execute(
        "INSERT INTO siparis_kalemleri "
        "(siparis_id, urun_id, adet, birim_fiyat, not_bilgisi) "
        "VALUES (?, ?, ?, ?, ?)",
        (siparis_id, urun_id, adet, fiyat["fiyat"], not_bilgisi)
    )

    # Toplam tutarı güncelle
    toplam = conn.execute(
        "SELECT SUM(adet * birim_fiyat) AS toplam "
        "FROM siparis_kalemleri WHERE siparis_id = ?",
        (siparis_id,)
    ).fetchone()["toplam"]

    conn.execute(
        "UPDATE siparisler SET toplam_tutar = ? WHERE id = ?",
        (toplam, siparis_id)
    )
    conn.commit()
    conn.close()
    return True


def siparis_kalem_sil(kalem_id):
    """Sipariş kalemini siler ve toplamı günceller."""
    conn = baglanti_al()
    kalem = conn.execute(
        "SELECT siparis_id FROM siparis_kalemleri WHERE id = ?", (kalem_id,)
    ).fetchone()

    if not kalem:
        conn.close()
        return False

    siparis_id = kalem["siparis_id"]
    conn.execute("DELETE FROM siparis_kalemleri WHERE id = ?", (kalem_id,))

    toplam = conn.execute(
        "SELECT COALESCE(SUM(adet * birim_fiyat), 0) AS toplam "
        "FROM siparis_kalemleri WHERE siparis_id = ?",
        (siparis_id,)
    ).fetchone()["toplam"]

    conn.execute(
        "UPDATE siparisler SET toplam_tutar = ? WHERE id = ?",
        (toplam, siparis_id)
    )
    conn.commit()
    conn.close()
    return True


def siparis_detay(siparis_id):
    """Siparişin kalemlerini döndürür."""
    conn = baglanti_al()
    rows = conn.execute(
        """
        SELECT sk.id, u.ad AS urun_adi, sk.adet, sk.birim_fiyat,
               (sk.adet * sk.birim_fiyat) AS toplam, sk.not_bilgisi
        FROM siparis_kalemleri sk
        JOIN urunler u ON sk.urun_id = u.id
        WHERE sk.siparis_id = ?
        ORDER BY sk.id
        """,
        (siparis_id,)
    ).fetchall()
    conn.close()
    return rows


def siparis_bilgisi(siparis_id):
    """Sipariş özet bilgisini döndürür."""
    conn = baglanti_al()
    row = conn.execute(
        """
        SELECT s.*, m.numara AS masa_no
        FROM siparisler s
        JOIN masalar m ON s.masa_id = m.id
        WHERE s.id = ?
        """,
        (siparis_id,)
    ).fetchone()
    conn.close()
    return row


def siparis_iptal(siparis_id):
    """Siparişi iptal eder."""
    conn = baglanti_al()
    siparis = conn.execute(
        "SELECT masa_id FROM siparisler WHERE id = ?", (siparis_id,)
    ).fetchone()

    if not siparis:
        conn.close()
        return False

    conn.execute(
        "UPDATE siparisler SET durum = 'iptal' WHERE id = ?", (siparis_id,)
    )
    conn.execute(
        "UPDATE masalar SET durum = 'bos' WHERE id = ?",
        (siparis["masa_id"],)
    )
    conn.commit()
    conn.close()
    return True


def masa_tasi(siparis_id, yeni_masa_id):
    """Siparişi başka masaya taşır."""
    conn = baglanti_al()
    siparis = conn.execute(
        "SELECT masa_id FROM siparisler WHERE id = ? AND durum = 'acik'",
        (siparis_id,)
    ).fetchone()

    if not siparis:
        conn.close()
        return False

    eski_masa_id = siparis["masa_id"]
    conn.execute(
        "UPDATE siparisler SET masa_id = ? WHERE id = ?",
        (yeni_masa_id, siparis_id)
    )
    conn.execute(
        "UPDATE masalar SET durum = 'bos' WHERE id = ?", (eski_masa_id,)
    )
    conn.execute(
        "UPDATE masalar SET durum = 'dolu' WHERE id = ?", (yeni_masa_id,)
    )
    conn.commit()
    conn.close()
    return True
