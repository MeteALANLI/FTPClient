import sys, os, os.path, operator
from ftplib import FTP
import FTPLib
class Functions:

    @classmethod
    def upload(self):
        return
    @classmethod
    def download(self):
        return
    @classmethod
    def getHelp(cls):
        response = "listele\t'Klasörleri listeler'\n" \
                  " gulegule\t'Login Ekranina çıkış verir'\n" \
                  " cikis\t'Programdan çıkmayı sağlar'\n" \
                  " k_gir\t'Belirtilen yola girin\n'" \
                  " k_duzenle\t'Belirtilen yolu duzenle\n'" \
                  " k_kopyala\t'Belirtilen yolu kopyala\n'" \
                  " k_yapistir\t'Belirtilen yolu yapistirir\n'" \
                  " k_sil\t'Belirtilen yolu siler\n'" \
                  " k_zip\t'Belirtilen zip.li yolu acma\n'"
        return response
    def myLogin(self):  # Giriş yaptıran method yanls giris olursa bir daha girmek icin
        while True:
            host = str(input("Server Adresini Giriniz :"))
            if "http://" in host:  # Host Ip adresini almak için taraycidan alinirsa diye http:// silindi
                host = host.replace("http://", "")
            try:
                if not host:
                    continue
                else:
                    ftp = FTP(host)# Baglanti sağlandı ve bir değişkene atıldı.
            except:# Baglantı saglanmazsa olacaklar.
                print("Server Adresi Çözümlenemedi")
                continue
            while True:
                user_n = str(input("Kullanıcı Adını giriniz :"))
                user_p = str(input("Şifrenizi Giriniz :"))
                try:
                    ftp.login(user=user_n, passwd=user_p)  # Giriş burda yapıldı
                    break
                except:
                    print("Kullanıcı adı veya şifre hatalı")
                    continue

            print(ftp.getwelcome())
            break
        return ftp  # Eğer giriş düzgün ise buraya düsüp geriye döndürcek girdiği FTP'yi


