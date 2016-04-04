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

            try:
                resp=ftp.pwd()
            except:
                print("Dizin Değiştirilemedi.")

            print("Dizin Başarı ile Değiştirildi.")
            continue


        elif command == "pwd":  # Bulunan dizin ismini verir

            try:
                resp=ftp.pwd()

            except:
                print("HATA!:Dizin Yolu Bulunamadı.")

            print("Dizin Yolu Bulundu.")
            continue


        elif command == "dir":

            try:
                resp=ftp.dir()

            except:
                print("HATA!:Klasörler Listelenemedi.")

            print("Klasörler Başarı ile Listelendi.")
            continue


        elif command.__contains__("mkd"):
            mName=command.replace("mkd ","")

            try:
                resp=ftp.mkd(mName)

            except:
                print("HATA!:Klasör Oluşturulamadı.")
            print("Klasör Başarı ile Oluşturuldu.")
            continue


        elif command.__contains__("delete"):
            dosyaSil=command.replace("delete ","")

            try:
                resp=ftp.delete(dosyaSil)

            except:
                print("HATA!:Klasör Silinemedi.")

            print("Klasör Başarı ile Silindi.")
            continue


        elif command.__contains__("get"):  # Dosya alma komututur.... alınacakdosya alınansodya adı

            try:
                resp=ftp.get()

            except:
                print("HATA!:Dosya Alınamadı.")

            print("Dosya Başarı ile Alındı.")
            continue


        elif command == "send":  # Dosya gönderme
            try:
                resp=ftp.send()

            except:
                print("HATA!:Dosya Gönderilemedi.")

            print("Dosya Başarı ile Gönderildi.")
            continue


        elif command == "close":  # Ftpden çıkma login ekranına geri götürme

            try:
                resp=ftp.close()
                ftp_fn.myLogin(ftp_fn)

            except:
                print("HATA!:Bağlantıdan Çıkış Yapılamadı.")

            print("Bağlantıdan Başarı İle Çıkıldı.")
            continue


        elif command == "exit":  # Programdan çıkma

            try:
                resp=sys.exit()

            except:
                print("HATA!:Programdan Çıkılamadı.")

            print("Programdan Başarı İle Çıkıldı.")
            continue
        else:
            print("Yanlış komut girdiniz. Lütfen 'yardim' komutuna giriniz:")

