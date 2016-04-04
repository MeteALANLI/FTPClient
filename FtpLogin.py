import sys, os, os.path, operator
from ftplib import FTP
import Functions
class FTPLogin:
    ftp_fn = Functions.Functions
    print("SDUFTP'ye hoşgeldiniz!")
    ftp = ftp_fn.myLogin(ftp_fn)#İnternet dağında bir tünel açıldı
    path = ftp.pwd()
    print("K   O   M   U   T   L   A   R\n")
    print("cd       -   Dizin Adı Değiştirme\n")
    print("pwd      -   Dizin Adları\n")
    print("dir      -   Dizinleri Listele\n")
    print("mkd      -   Dosya ekle\n")
    print("get      -   Dosya Al\n")
    print("send     -   Dosya Gönder\n")
    print("close    -   Bağlantıyı kapat\n")
    print("exit     -   Programdan çık\n")
    while True:
        command = str(input("Bir komut giriniz:"))


        if command == "yardim":
            print("cd       -   Dizin Adı Değiştirme\n")
            print("pwd      -   Dizin Yolu\n")
            print("dir      -   Dizinleri Listele\n")
            print("mkd      -   Dosya ekle\n")
            print("get      -   Dosya Al\n")
            print("send     -   Dosya Gönder\n")
            print("delete   -   Dosyayı Sil\n")
            print("close    -   Bağlantıyı kapat\n")
            print("exit     -   Programdan çık\n")

            continue

        elif command.__contains__("cd "):  # Dizin değiştirme
            resp=ftp.pwd()
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Dizin Değiştirelemedi")
            except:
                print("Dizin Başarı ile Değiştirildi.")
            continue


        elif command == "pwd":  # Bulunan dizin ismini verir
            resp=ftp.pwd()
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Dizin Yolu Bulunamadı.")
            except:
                print("Dizin Yolu Bulundu.")


            continue
        elif command == "dir":
            resp=ftp.dir()
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Klasörler Listelenemedi.")
            except:
                print("Klasörler Başarı ile Listelendi.")
            continue


        elif command.__contains__("mkd"):
            mName=command.replace("mkd ","")
            resp=ftp.mkd(mName)
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Klasör Oluşturulamadı.")
            except:
                print("Klasör Başarı ile Oluşturuldu.")

            continue


        elif command.__contains__("delete"):
            dosyaSil=command.replace("delete ","")
            resp=ftp.delete(dosyaSil)
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Klasör Silinemedi.")
            except:
                print("Klasör Başarı ile Silindi.")

            continue


        elif command.__contains__("get"):  # Dosya alma komututur.... alınacakdosya alınansodya adı
            resp=ftp.get()
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Dosya Alınamadı.")
            except:
                print("Dosya Başarı ile Alındı.")
            continue


        elif command == "send":  # Dosya gönderme
            continue


        elif command == "close":  # Ftpden çıkma login ekranına geri götürme
            resp=ftp.close()
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Bağlantıdan Çıkış Yapılamadı.")
            except:
                print("Bağlantıdan Başarı İle Çıkıldı.")
            ftp_fn.myLogin(ftp_fn)
            continue


        elif command == "exit":  # Programdan çıkma
            resp=sys.exit()
            try:
                if resp[:1] == 4 or resp[:1] == 5:
                    print("HATA!:Programdan Çıkılamadı.")
            except:
                print("Programdan Başarı İle Çıkıldı.")
        else:
            print("Yanlış komut girdiniz. Lütfen 'yardim' komutuna giriniz:")

