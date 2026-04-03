"""Kafe Otomasyon Sistemi - Menü yönetimi."""

from cafe_otomasyon.veritabani import baglanti_al


def kategorileri_listele():
    """Tüm kategorileri döndürür."""
    conn = baglanti_al()
    rows = conn.execute("SELECT * FROM kategoriler ORDER BY id").fetchall()
    conn.close()
    return rows


def urunleri_listele(kategori_id=None, sadece_aktif=True):
    """Ürünleri listeler. Kategori filtresi opsiyonel."""
    conn = baglanti_al()
    sql = """
        SELECT u.id, u.ad, k.ad AS kategori, u.fiyat, u.aktif
        FROM urunler u
        JOIN kategoriler k ON u.kategori_id = k.id
    """
    params = []
    kosullar = []

    if kategori_id:
        kosullar.append("u.kategori_id = ?")
        params.append(kategori_id)
    if sadece_aktif:
        kosullar.append("u.aktif = 1")

    if kosullar:
        sql += " WHERE " + " AND ".join(kosullar)

    sql += " ORDER BY k.id, u.ad"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def urun_ekle(ad, kategori_id, fiyat):
    """Yeni ürün ekler."""
    conn = baglanti_al()
    conn.execute(
        "INSERT INTO urunler (ad, kategori_id, fiyat) VALUES (?, ?, ?)",
        (ad, kategori_id, fiyat)
    )
    conn.commit()
    conn.close()


def urun_guncelle(urun_id, ad=None, fiyat=None, aktif=None):
    """Mevcut ürünü günceller."""
    conn = baglanti_al()
    guncellemeler = []
    params = []

    if ad is not None:
        guncellemeler.append("ad = ?")
        params.append(ad)
    if fiyat is not None:
        guncellemeler.append("fiyat = ?")
        params.append(fiyat)
    if aktif is not None:
        guncellemeler.append("aktif = ?")
        params.append(aktif)

    if not guncellemeler:
        conn.close()
        return

    params.append(urun_id)
    sql = f"UPDATE urunler SET {', '.join(guncellemeler)} WHERE id = ?"
    conn.execute(sql, params)
    conn.commit()
    conn.close()


def urun_sil(urun_id):
    """Ürünü pasife alır (soft delete)."""
    urun_guncelle(urun_id, aktif=0)


def kategori_ekle(ad):
    """Yeni kategori ekler."""
    conn = baglanti_al()
    conn.execute("INSERT INTO kategoriler (ad) VALUES (?)", (ad,))
    conn.commit()
    conn.close()


def urun_ara(arama):
    """Ürün adına göre arama yapar."""
    conn = baglanti_al()
    rows = conn.execute(
        """
        SELECT u.id, u.ad, k.ad AS kategori, u.fiyat
        FROM urunler u
        JOIN kategoriler k ON u.kategori_id = k.id
        WHERE u.aktif = 1 AND u.ad LIKE ?
        ORDER BY u.ad
        """,
        (f"%{arama}%",)
    ).fetchall()
    conn.close()
    return rows
