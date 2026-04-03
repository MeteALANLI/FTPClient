"""Kafe Otomasyon Sistemi - Kasa ve ödeme işlemleri."""

from datetime import datetime
from cafe_otomasyon.veritabani import baglanti_al


def kasa_ac(acilis_tutari=0):
    """Günlük kasayı açar."""
    conn = baglanti_al()
    tarih = datetime.now().strftime("%Y-%m-%d")

    mevcut = conn.execute(
        "SELECT * FROM gunluk_kasa WHERE tarih = ? AND durum = 'acik'",
        (tarih,)
    ).fetchone()

    if mevcut:
        conn.close()
        return mevcut["id"]

    c = conn.execute(
        "INSERT INTO gunluk_kasa (tarih, acilis_tutari) VALUES (?, ?)",
        (tarih, acilis_tutari)
    )
    kasa_id = c.lastrowid
    conn.commit()
    conn.close()
    return kasa_id


def kasa_durumu():
    """Bugünkü kasa durumunu döndürür."""
    conn = baglanti_al()
    tarih = datetime.now().strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT * FROM gunluk_kasa WHERE tarih = ? ORDER BY id DESC LIMIT 1",
        (tarih,)
    ).fetchone()
    conn.close()
    return row


def odeme_al(siparis_id, odeme_turu="nakit"):
    """Sipariş ödemesini alır ve kasayı günceller."""
    conn = baglanti_al()
    siparis = conn.execute(
        "SELECT * FROM siparisler WHERE id = ? AND durum = 'acik'",
        (siparis_id,)
    ).fetchone()

    if not siparis:
        conn.close()
        return None

    tutar = siparis["toplam_tutar"]
    masa_id = siparis["masa_id"]

    # Siparişi kapat
    conn.execute(
        "UPDATE siparisler SET durum = 'kapali', odeme_turu = ? WHERE id = ?",
        (odeme_turu, siparis_id)
    )

    # Masayı boşalt
    conn.execute(
        "UPDATE masalar SET durum = 'bos' WHERE id = ?", (masa_id,)
    )

    # Kasayı güncelle
    tarih = datetime.now().strftime("%Y-%m-%d")
    kasa = conn.execute(
        "SELECT * FROM gunluk_kasa WHERE tarih = ? AND durum = 'acik'",
        (tarih,)
    ).fetchone()

    if kasa:
        if odeme_turu == "nakit":
            conn.execute(
                "UPDATE gunluk_kasa SET toplam_nakit = toplam_nakit + ?, "
                "toplam_gelir = toplam_gelir + ? WHERE id = ?",
                (tutar, tutar, kasa["id"])
            )
        elif odeme_turu == "kart":
            conn.execute(
                "UPDATE gunluk_kasa SET toplam_kart = toplam_kart + ?, "
                "toplam_gelir = toplam_gelir + ? WHERE id = ?",
                (tutar, tutar, kasa["id"])
            )

    conn.commit()
    conn.close()
    return tutar


def kasa_kapat():
    """Günlük kasayı kapatır."""
    conn = baglanti_al()
    tarih = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        "UPDATE gunluk_kasa SET durum = 'kapali' "
        "WHERE tarih = ? AND durum = 'acik'",
        (tarih,)
    )
    conn.commit()
    conn.close()


def gunluk_islemler():
    """Bugünkü kapanan siparişleri listeler."""
    conn = baglanti_al()
    tarih = datetime.now().strftime("%Y-%m-%d")
    rows = conn.execute(
        """
        SELECT s.id, m.numara AS masa_no, s.toplam_tutar,
               s.odeme_turu, s.tarih
        FROM siparisler s
        JOIN masalar m ON s.masa_id = m.id
        WHERE s.durum = 'kapali' AND s.tarih LIKE ?
        ORDER BY s.tarih DESC
        """,
        (f"{tarih}%",)
    ).fetchall()
    conn.close()
    return rows
