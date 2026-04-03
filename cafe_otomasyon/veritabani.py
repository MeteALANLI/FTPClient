"""Kafe Otomasyon Sistemi - Veritabanı modelleri ve yönetimi (SQLite)."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "kafe.db")


def baglanti_al():
    """Veritabanı bağlantısı döndürür."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def veritabani_olustur():
    """Tüm tabloları oluşturur ve varsayılan verileri yükler."""
    conn = baglanti_al()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS kategoriler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS urunler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            kategori_id INTEGER NOT NULL,
            fiyat REAL NOT NULL,
            aktif INTEGER DEFAULT 1,
            FOREIGN KEY (kategori_id) REFERENCES kategoriler(id)
        );

        CREATE TABLE IF NOT EXISTS masalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numara INTEGER NOT NULL UNIQUE,
            kapasite INTEGER DEFAULT 4,
            durum TEXT DEFAULT 'bos'  -- bos, dolu, rezerve
        );

        CREATE TABLE IF NOT EXISTS siparisler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            masa_id INTEGER NOT NULL,
            tarih TEXT NOT NULL,
            durum TEXT DEFAULT 'acik',  -- acik, kapali, iptal
            toplam_tutar REAL DEFAULT 0,
            odeme_turu TEXT,  -- nakit, kart, karisik
            FOREIGN KEY (masa_id) REFERENCES masalar(id)
        );

        CREATE TABLE IF NOT EXISTS siparis_kalemleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siparis_id INTEGER NOT NULL,
            urun_id INTEGER NOT NULL,
            adet INTEGER NOT NULL DEFAULT 1,
            birim_fiyat REAL NOT NULL,
            not_bilgisi TEXT,
            FOREIGN KEY (siparis_id) REFERENCES siparisler(id),
            FOREIGN KEY (urun_id) REFERENCES urunler(id)
        );

        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT NOT NULL UNIQUE,
            sifre TEXT NOT NULL,
            rol TEXT DEFAULT 'garson'  -- admin, garson, kasiyer
        );

        CREATE TABLE IF NOT EXISTS gunluk_kasa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT NOT NULL,
            acilis_tutari REAL DEFAULT 0,
            toplam_nakit REAL DEFAULT 0,
            toplam_kart REAL DEFAULT 0,
            toplam_gelir REAL DEFAULT 0,
            durum TEXT DEFAULT 'acik'  -- acik, kapali
        );
    """)

    # Varsayılan verileri yükle (sadece boşsa)
    if c.execute("SELECT COUNT(*) FROM kategoriler").fetchone()[0] == 0:
        kategoriler = [
            "Sıcak İçecekler", "Soğuk İçecekler", "Tatlılar",
            "Atıştırmalıklar", "Kahvaltı", "Ana Yemekler"
        ]
        c.executemany("INSERT INTO kategoriler (ad) VALUES (?)",
                      [(k,) for k in kategoriler])

        urunler = [
            ("Türk Kahvesi", 1, 45.00),
            ("Filtre Kahve", 1, 50.00),
            ("Espresso", 1, 55.00),
            ("Latte", 1, 65.00),
            ("Cappuccino", 1, 65.00),
            ("Americano", 1, 55.00),
            ("Sıcak Çikolata", 1, 60.00),
            ("Çay", 1, 25.00),
            ("Limonata", 2, 45.00),
            ("Portakal Suyu", 2, 50.00),
            ("Ayran", 2, 30.00),
            ("Soğuk Kahve", 2, 70.00),
            ("Smoothie", 2, 75.00),
            ("Su", 2, 10.00),
            ("Cheesecake", 3, 90.00),
            ("Brownie", 3, 75.00),
            ("Tiramisu", 3, 95.00),
            ("Sufle", 3, 85.00),
            ("Waffle", 3, 80.00),
            ("Sandviç", 4, 85.00),
            ("Tost", 4, 65.00),
            ("Poğaça", 4, 35.00),
            ("Kurabiye", 4, 30.00),
            ("Serpme Kahvaltı", 5, 250.00),
            ("Sahanda Yumurta", 5, 75.00),
            ("Menemen", 5, 80.00),
            ("Makarna", 6, 120.00),
            ("Izgara Tavuk", 6, 150.00),
            ("Köfte", 6, 140.00),
        ]
        c.executemany(
            "INSERT INTO urunler (ad, kategori_id, fiyat) VALUES (?, ?, ?)",
            urunler
        )

    if c.execute("SELECT COUNT(*) FROM masalar").fetchone()[0] == 0:
        masalar = [(i, 4) for i in range(1, 16)]
        c.executemany(
            "INSERT INTO masalar (numara, kapasite) VALUES (?, ?)", masalar
        )

    if c.execute("SELECT COUNT(*) FROM kullanicilar").fetchone()[0] == 0:
        c.execute(
            "INSERT INTO kullanicilar (kullanici_adi, sifre, rol) "
            "VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )

    conn.commit()
    conn.close()
