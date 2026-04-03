"""Kafe Otomasyon Sistemi - Ana CLI arayüzü."""

import os
import sys
from datetime import datetime

from cafe_otomasyon.veritabani import veritabani_olustur
from cafe_otomasyon.menu import (
    kategorileri_listele, urunleri_listele, urun_ekle,
    urun_guncelle, urun_sil, kategori_ekle, urun_ara,
)
from cafe_otomasyon.siparis import (
    masalari_listele, masa_durumu_guncelle, siparis_ac,
    masanin_acik_siparisi, siparis_kalem_ekle, siparis_kalem_sil,
    siparis_detay, siparis_bilgisi, siparis_iptal, masa_tasi,
)
from cafe_otomasyon.kasa import (
    kasa_ac, kasa_durumu, odeme_al, kasa_kapat, gunluk_islemler,
)
from cafe_otomasyon.rapor import (
    gunluk_satis_raporu, aylik_satis_raporu, en_cok_satan_urunler,
    kategori_bazli_rapor, masa_performans_raporu,
)


# ── Yardımcı Fonksiyonlar ───────────────────────────────────────

def temizle():
    os.system("cls" if os.name == "nt" else "clear")


def baslik(metin):
    print(f"\n{'=' * 50}")
    print(f"  {metin}")
    print(f"{'=' * 50}")


def tablo_yazdir(basliklar, satirlar):
    """Basit tablo yazdırma."""
    if not satirlar:
        print("  Kayıt bulunamadı.")
        return

    # Sütun genişliklerini hesapla
    genislikler = [len(str(b)) for b in basliklar]
    for satir in satirlar:
        for i, deger in enumerate(satir):
            genislikler[i] = max(genislikler[i], len(str(deger)))

    # Başlık
    fmt = "  ".join(f"{{:<{g}}}" for g in genislikler)
    print(f"  {fmt.format(*basliklar)}")
    print(f"  {'  '.join('-' * g for g in genislikler)}")

    # Satırlar
    for satir in satirlar:
        print(f"  {fmt.format(*satir)}")


def secim_al(mesaj="Seçiminiz", varsayilan=None):
    try:
        girdi = input(f"\n  {mesaj}: ").strip()
        if not girdi and varsayilan is not None:
            return varsayilan
        return girdi
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def sayi_al(mesaj):
    try:
        return int(secim_al(mesaj))
    except (TypeError, ValueError):
        return None


def ondalik_al(mesaj):
    try:
        return float(secim_al(mesaj))
    except (TypeError, ValueError):
        return None


# ── Ana Menü ─────────────────────────────────────────────────────

def ana_menu():
    while True:
        baslik("KAFE OTOMASYON SİSTEMİ")
        print("""
  1. Masa Yönetimi
  2. Sipariş Yönetimi
  3. Menü Yönetimi
  4. Kasa İşlemleri
  5. Raporlar
  0. Çıkış
        """)
        secim = secim_al("Seçiminiz")

        if secim == "1":
            masa_yonetimi()
        elif secim == "2":
            siparis_yonetimi()
        elif secim == "3":
            menu_yonetimi()
        elif secim == "4":
            kasa_islemleri()
        elif secim == "5":
            raporlar_menu()
        elif secim == "0":
            print("\n  Güle güle! ☕\n")
            sys.exit(0)


# ── Masa Yönetimi ───────────────────────────────────────────────

def masa_yonetimi():
    while True:
        baslik("MASA YÖNETİMİ")
        masalar = masalari_listele()

        durum_simge = {"bos": "🟢", "dolu": "🔴", "rezerve": "🟡"}
        satirlar = []
        for m in masalar:
            simge = durum_simge.get(m["durum"], "⚪")
            satirlar.append((
                m["id"], f"Masa {m['numara']}", m["kapasite"],
                f"{simge} {m['durum'].capitalize()}"
            ))

        tablo_yazdir(["ID", "Masa", "Kapasite", "Durum"], satirlar)

        print("""
  1. Masa durumu değiştir
  2. Yeni masa ekle
  0. Geri
        """)
        secim = secim_al("Seçiminiz")

        if secim == "1":
            masa_id = sayi_al("Masa ID")
            if masa_id:
                print("  Durumlar: bos, dolu, rezerve")
                durum = secim_al("Yeni durum")
                if durum in ("bos", "dolu", "rezerve"):
                    masa_durumu_guncelle(masa_id, durum)
                    print("  ✓ Masa durumu güncellendi.")
        elif secim == "2":
            numara = sayi_al("Masa numarası")
            kapasite = sayi_al("Kapasite (varsayılan 4)") or 4
            if numara:
                try:
                    from cafe_otomasyon.siparis import masa_ekle
                    masa_ekle(numara, kapasite)
                    print("  ✓ Masa eklendi.")
                except Exception as e:
                    print(f"  ✗ Hata: {e}")
        elif secim == "0":
            return


# ── Sipariş Yönetimi ────────────────────────────────────────────

def siparis_yonetimi():
    while True:
        baslik("SİPARİŞ YÖNETİMİ")
        print("""
  1. Yeni sipariş aç
  2. Siparişe ürün ekle
  3. Sipariş detayı görüntüle
  4. Sipariş kalemi sil
  5. Sipariş iptal et
  6. Masa taşı
  7. Hızlı sipariş (masa seç → ürün ekle)
  0. Geri
        """)
        secim = secim_al("Seçiminiz")

        if secim == "1":
            yeni_siparis()
        elif secim == "2":
            siparise_urun_ekle()
        elif secim == "3":
            siparis_goruntule()
        elif secim == "4":
            kalem_sil()
        elif secim == "5":
            iptal_et()
        elif secim == "6":
            masa_tasi_isle()
        elif secim == "7":
            hizli_siparis()
        elif secim == "0":
            return


def yeni_siparis():
    # Boş masaları göster
    masalar = masalari_listele()
    bos_masalar = [m for m in masalar if m["durum"] == "bos"]

    if not bos_masalar:
        print("  Boş masa yok!")
        return

    print("\n  Boş Masalar:")
    for m in bos_masalar:
        print(f"    {m['id']}. Masa {m['numara']} (Kapasite: {m['kapasite']})")

    masa_id = sayi_al("Masa ID")
    if masa_id:
        siparis_id = siparis_ac(masa_id)
        print(f"  ✓ Sipariş #{siparis_id} açıldı.")

        ekle = secim_al("Hemen ürün eklemek ister misiniz? (e/h)", "e")
        if ekle.lower() == "e":
            urun_ekle_dongulu(siparis_id)


def urun_ekle_dongulu(siparis_id):
    """Siparişe döngüsel olarak ürün ekler."""
    while True:
        urunler = urunleri_listele()
        kategoriler = kategorileri_listele()

        print("\n  Kategoriler:")
        for k in kategoriler:
            print(f"    {k['id']}. {k['ad']}")

        kat_id = sayi_al("Kategori ID (0=tümü)")

        if kat_id == 0 or kat_id is None:
            secilen_urunler = urunler
        else:
            secilen_urunler = [u for u in urunler if u["kategori_id"] == kat_id] if hasattr(urunler[0], '__getitem__') else urunler

        # Ürünleri filtrele
        filtreli = urunleri_listele(kat_id if kat_id and kat_id > 0 else None)
        satirlar = [(u["id"], u["ad"], u["kategori"], f"{u['fiyat']:.2f} TL") for u in filtreli]
        tablo_yazdir(["ID", "Ürün", "Kategori", "Fiyat"], satirlar)

        urun_id = sayi_al("Ürün ID (0=bitti)")
        if not urun_id or urun_id == 0:
            break

        adet = sayi_al("Adet") or 1
        not_bilgisi = secim_al("Not (boş bırakabilirsiniz)", "")

        if siparis_kalem_ekle(siparis_id, urun_id, adet, not_bilgisi or None):
            print(f"  ✓ {adet} adet ürün eklendi.")
        else:
            print("  ✗ Ürün bulunamadı.")

    # Sipariş özetini göster
    print("\n  Sipariş Özeti:")
    kalemler = siparis_detay(siparis_id)
    satirlar = [(k["urun_adi"], k["adet"], f"{k['birim_fiyat']:.2f}", f"{k['toplam']:.2f}") for k in kalemler]
    tablo_yazdir(["Ürün", "Adet", "Birim Fiyat", "Toplam"], satirlar)

    bilgi = siparis_bilgisi(siparis_id)
    if bilgi:
        print(f"\n  Genel Toplam: {bilgi['toplam_tutar']:.2f} TL")


def siparise_urun_ekle():
    masa_id = sayi_al("Masa ID")
    if not masa_id:
        return

    siparis = masanin_acik_siparisi(masa_id)
    if not siparis:
        print("  Bu masada açık sipariş yok.")
        return

    print(f"  Sipariş #{siparis['id']} - Mevcut tutar: {siparis['toplam_tutar']:.2f} TL")
    urun_ekle_dongulu(siparis["id"])


def siparis_goruntule():
    masa_id = sayi_al("Masa ID")
    if not masa_id:
        return

    siparis = masanin_acik_siparisi(masa_id)
    if not siparis:
        print("  Bu masada açık sipariş yok.")
        return

    baslik(f"Sipariş #{siparis['id']} - Masa {masa_id}")
    kalemler = siparis_detay(siparis["id"])
    satirlar = [
        (k["id"], k["urun_adi"], k["adet"],
         f"{k['birim_fiyat']:.2f}", f"{k['toplam']:.2f}",
         k["not_bilgisi"] or "")
        for k in kalemler
    ]
    tablo_yazdir(["Kalem ID", "Ürün", "Adet", "Birim", "Toplam", "Not"], satirlar)
    print(f"\n  Genel Toplam: {siparis['toplam_tutar']:.2f} TL")


def kalem_sil():
    kalem_id = sayi_al("Silinecek kalem ID")
    if kalem_id:
        if siparis_kalem_sil(kalem_id):
            print("  ✓ Kalem silindi.")
        else:
            print("  ✗ Kalem bulunamadı.")


def iptal_et():
    masa_id = sayi_al("Masa ID")
    if not masa_id:
        return

    siparis = masanin_acik_siparisi(masa_id)
    if not siparis:
        print("  Bu masada açık sipariş yok.")
        return

    onay = secim_al(f"Sipariş #{siparis['id']} iptal edilecek. Emin misiniz? (e/h)")
    if onay and onay.lower() == "e":
        siparis_iptal(siparis["id"])
        print("  ✓ Sipariş iptal edildi.")


def masa_tasi_isle():
    masa_id = sayi_al("Mevcut masa ID")
    if not masa_id:
        return

    siparis = masanin_acik_siparisi(masa_id)
    if not siparis:
        print("  Bu masada açık sipariş yok.")
        return

    yeni_masa_id = sayi_al("Yeni masa ID")
    if yeni_masa_id:
        if masa_tasi(siparis["id"], yeni_masa_id):
            print(f"  ✓ Sipariş masa {yeni_masa_id}'e taşındı.")
        else:
            print("  ✗ Taşıma başarısız.")


def hizli_siparis():
    """Tek adımda masa seç, sipariş aç, ürün ekle."""
    masalar = masalari_listele()
    bos_masalar = [m for m in masalar if m["durum"] == "bos"]
    dolu_masalar = [m for m in masalar if m["durum"] == "dolu"]

    if dolu_masalar:
        print("\n  Dolu Masalar (mevcut siparişe ekle):")
        for m in dolu_masalar:
            print(f"    {m['id']}. Masa {m['numara']}")

    if bos_masalar:
        print("\n  Boş Masalar (yeni sipariş):")
        for m in bos_masalar:
            print(f"    {m['id']}. Masa {m['numara']}")

    masa_id = sayi_al("Masa ID")
    if not masa_id:
        return

    siparis = masanin_acik_siparisi(masa_id)
    if not siparis:
        siparis_id = siparis_ac(masa_id)
        print(f"  ✓ Yeni sipariş #{siparis_id} açıldı.")
    else:
        siparis_id = siparis["id"]
        print(f"  Mevcut sipariş #{siparis_id} kullanılıyor.")

    urun_ekle_dongulu(siparis_id)


# ── Menü Yönetimi ───────────────────────────────────────────────

def menu_yonetimi():
    while True:
        baslik("MENÜ YÖNETİMİ")
        print("""
  1. Tüm ürünleri listele
  2. Kategoriye göre listele
  3. Ürün ara
  4. Yeni ürün ekle
  5. Ürün güncelle
  6. Ürün sil (pasife al)
  7. Yeni kategori ekle
  0. Geri
        """)
        secim = secim_al("Seçiminiz")

        if secim == "1":
            urunler = urunleri_listele(sadece_aktif=False)
            satirlar = [
                (u["id"], u["ad"], u["kategori"],
                 f"{u['fiyat']:.2f} TL",
                 "Aktif" if u["aktif"] else "Pasif")
                for u in urunler
            ]
            tablo_yazdir(["ID", "Ürün", "Kategori", "Fiyat", "Durum"], satirlar)

        elif secim == "2":
            kategoriler = kategorileri_listele()
            for k in kategoriler:
                print(f"  {k['id']}. {k['ad']}")
            kat_id = sayi_al("Kategori ID")
            if kat_id:
                urunler = urunleri_listele(kat_id)
                satirlar = [
                    (u["id"], u["ad"], f"{u['fiyat']:.2f} TL")
                    for u in urunler
                ]
                tablo_yazdir(["ID", "Ürün", "Fiyat"], satirlar)

        elif secim == "3":
            arama = secim_al("Aranacak ürün adı")
            if arama:
                sonuclar = urun_ara(arama)
                satirlar = [
                    (u["id"], u["ad"], u["kategori"], f"{u['fiyat']:.2f} TL")
                    for u in sonuclar
                ]
                tablo_yazdir(["ID", "Ürün", "Kategori", "Fiyat"], satirlar)

        elif secim == "4":
            ad = secim_al("Ürün adı")
            kategoriler = kategorileri_listele()
            for k in kategoriler:
                print(f"  {k['id']}. {k['ad']}")
            kat_id = sayi_al("Kategori ID")
            fiyat = ondalik_al("Fiyat (TL)")
            if ad and kat_id and fiyat:
                urun_ekle(ad, kat_id, fiyat)
                print("  ✓ Ürün eklendi.")

        elif secim == "5":
            urun_id = sayi_al("Güncellenecek ürün ID")
            if urun_id:
                print("  (Boş bırakırsanız değişmez)")
                ad = secim_al("Yeni ad", "")
                fiyat = secim_al("Yeni fiyat", "")
                urun_guncelle(
                    urun_id,
                    ad=ad if ad else None,
                    fiyat=float(fiyat) if fiyat else None,
                )
                print("  ✓ Ürün güncellendi.")

        elif secim == "6":
            urun_id = sayi_al("Pasife alınacak ürün ID")
            if urun_id:
                urun_sil(urun_id)
                print("  ✓ Ürün pasife alındı.")

        elif secim == "7":
            ad = secim_al("Kategori adı")
            if ad:
                kategori_ekle(ad)
                print("  ✓ Kategori eklendi.")

        elif secim == "0":
            return


# ── Kasa İşlemleri ──────────────────────────────────────────────

def kasa_islemleri():
    while True:
        baslik("KASA İŞLEMLERİ")

        durum = kasa_durumu()
        if durum:
            print(f"""
  Kasa Durumu: {durum['durum'].upper()}
  Açılış Tutarı: {durum['acilis_tutari']:.2f} TL
  Nakit: {durum['toplam_nakit']:.2f} TL
  Kart: {durum['toplam_kart']:.2f} TL
  Toplam Gelir: {durum['toplam_gelir']:.2f} TL
            """)
        else:
            print("\n  Kasa henüz açılmamış.")

        print("""
  1. Kasa aç
  2. Ödeme al
  3. Günlük işlemler
  4. Kasa kapat
  0. Geri
        """)
        secim = secim_al("Seçiminiz")

        if secim == "1":
            tutar = ondalik_al("Açılış tutarı (TL)") or 0
            kasa_id = kasa_ac(tutar)
            print(f"  ✓ Kasa açıldı (ID: {kasa_id}).")

        elif secim == "2":
            odeme_isle()

        elif secim == "3":
            islemler = gunluk_islemler()
            satirlar = [
                (i["id"], f"Masa {i['masa_no']}", f"{i['toplam_tutar']:.2f} TL",
                 i["odeme_turu"], i["tarih"])
                for i in islemler
            ]
            tablo_yazdir(["Sipariş", "Masa", "Tutar", "Ödeme", "Tarih"], satirlar)

        elif secim == "4":
            onay = secim_al("Kasayı kapatmak istediğinize emin misiniz? (e/h)")
            if onay and onay.lower() == "e":
                kasa_kapat()
                print("  ✓ Kasa kapatıldı.")

        elif secim == "0":
            return


def odeme_isle():
    """Masadan ödeme alır."""
    # Dolu masaları göster
    masalar = masalari_listele()
    dolu_masalar = [m for m in masalar if m["durum"] == "dolu"]

    if not dolu_masalar:
        print("  Dolu masa yok.")
        return

    print("\n  Dolu Masalar:")
    for m in dolu_masalar:
        siparis = masanin_acik_siparisi(m["id"])
        tutar = siparis["toplam_tutar"] if siparis else 0
        print(f"    Masa {m['numara']} (ID: {m['id']}) - {tutar:.2f} TL")

    masa_id = sayi_al("Masa ID")
    if not masa_id:
        return

    siparis = masanin_acik_siparisi(masa_id)
    if not siparis:
        print("  Bu masada açık sipariş yok.")
        return

    # Sipariş detayını göster
    print(f"\n  Sipariş #{siparis['id']}")
    kalemler = siparis_detay(siparis["id"])
    satirlar = [
        (k["urun_adi"], k["adet"], f"{k['toplam']:.2f} TL")
        for k in kalemler
    ]
    tablo_yazdir(["Ürün", "Adet", "Toplam"], satirlar)
    print(f"\n  TOPLAM: {siparis['toplam_tutar']:.2f} TL")

    print("\n  Ödeme türü:")
    print("  1. Nakit")
    print("  2. Kredi Kartı")
    odeme_sec = secim_al("Seçiminiz")

    odeme_turu = "nakit" if odeme_sec == "1" else "kart"
    tutar = odeme_al(siparis["id"], odeme_turu)

    if tutar is not None:
        print(f"\n  ✓ {tutar:.2f} TL ödeme alındı ({odeme_turu}).")
        print("  Masa boşaltıldı.")
    else:
        print("  ✗ Ödeme alınamadı.")


# ── Raporlar ─────────────────────────────────────────────────────

def raporlar_menu():
    while True:
        baslik("RAPORLAR")
        print("""
  1. Günlük satış raporu
  2. Aylık satış raporu
  3. En çok satan ürünler
  4. Kategori bazlı rapor
  5. Masa performans raporu
  0. Geri
        """)
        secim = secim_al("Seçiminiz")

        if secim == "1":
            tarih = secim_al("Tarih (YYYY-MM-DD)", datetime.now().strftime("%Y-%m-%d"))
            rapor = gunluk_satis_raporu(tarih)
            ozet = rapor["ozet"]
            baslik(f"Günlük Rapor - {tarih}")
            print(f"""
  Sipariş Sayısı: {ozet['siparis_sayisi']}
  Toplam Gelir:   {ozet['toplam_gelir']:.2f} TL
  Nakit:          {ozet['nakit']:.2f} TL
  Kart:           {ozet['kart']:.2f} TL
            """)
            if rapor["urunler"]:
                print("  Ürün Bazlı Detay:")
                satirlar = [
                    (u["ad"], u["toplam_adet"], f"{u['toplam_tutar']:.2f} TL")
                    for u in rapor["urunler"]
                ]
                tablo_yazdir(["Ürün", "Adet", "Toplam"], satirlar)

        elif secim == "2":
            yil = sayi_al("Yıl") or datetime.now().year
            ay = sayi_al("Ay (1-12)") or datetime.now().month
            rapor = aylik_satis_raporu(yil, ay)
            baslik(f"Aylık Rapor - {yil}/{ay:02d}")
            print(f"""
  Toplam Sipariş: {rapor['genel']['siparis_sayisi']}
  Toplam Gelir:   {rapor['genel']['toplam_gelir']:.2f} TL
            """)
            if rapor["gunluk"]:
                satirlar = [
                    (g["gun"], g["siparis_sayisi"], f"{g['toplam']:.2f} TL")
                    for g in rapor["gunluk"]
                ]
                tablo_yazdir(["Gün", "Sipariş", "Toplam"], satirlar)

        elif secim == "3":
            limit = sayi_al("Kaç ürün gösterilsin? (varsayılan 10)") or 10
            urunler = en_cok_satan_urunler(limit)
            satirlar = [
                (u["ad"], u["kategori"], u["toplam_adet"],
                 f"{u['toplam_gelir']:.2f} TL")
                for u in urunler
            ]
            tablo_yazdir(["Ürün", "Kategori", "Adet", "Gelir"], satirlar)

        elif secim == "4":
            raporlar = kategori_bazli_rapor()
            satirlar = [
                (r["kategori"], r["toplam_adet"], f"{r['toplam_gelir']:.2f} TL")
                for r in raporlar
            ]
            tablo_yazdir(["Kategori", "Adet", "Gelir"], satirlar)

        elif secim == "5":
            raporlar = masa_performans_raporu()
            satirlar = [
                (f"Masa {r['masa_no']}", r["siparis_sayisi"],
                 f"{r['toplam_gelir']:.2f} TL",
                 f"{r['ortalama_tutar']:.2f} TL")
                for r in raporlar
            ]
            tablo_yazdir(["Masa", "Sipariş", "Gelir", "Ortalama"], satirlar)

        elif secim == "0":
            return


# ── Giriş Noktası ───────────────────────────────────────────────

def main():
    veritabani_olustur()
    print("\n  Veritabanı hazır.")
    ana_menu()


if __name__ == "__main__":
    main()
