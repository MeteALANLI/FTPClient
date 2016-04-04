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
                print("Dizin Başarı ile Değiştirildi.")
            except:
                print("Dizin Değiştirilemedi.")

            continue


        elif command == "pwd":  # Bulunan dizin ismini verir

            try:
                resp=ftp.pwd()
                print("Dizin Yolu Bulundu.")
            except:
                print("HATA!:Dizin Yolu Bulunamadı.")


            continue


        elif command == "dir":

            try:
                resp=ftp.dir()
                print("Klasörler Başarı ile Listelendi.")
            except:
                print("HATA!:Klasörler Listelenemedi.")


            continue


        elif command.__contains__("mkd"):
            mName=command.replace("mkd ","")

            try:
                resp=ftp.mkd(mName)
                print("Klasör Başarı ile Oluşturuldu.")
            except:
                print("HATA!:Klasör Oluşturulamadı.")

            continue


        elif command.__contains__("delete"):
            dosyaSil=command.replace("delete ","")
            resp =""
            try:
                resp=ftp.delete(dosyaSil)
                print("Klasör Başarı ile Silindi.")
            except:
                print("HATA!:Klasör Silinemedi.",resp)


            continue


        elif command.__contains__("get"):  # Dosya alma komututur.... alınacakdosya alınansodya adı

            try:
                resp=ftp.get()
                print("Dosya Başarı ile Alındı.")
            except:
                print("HATA!:Dosya Alınamadı.")
            continue

        elif command == "send":  # Dosya gönderme
            try:
                resp=ftp.send()
                print("Dosya Başarı ile Gönderildi.")
            except:
                print("HATA!:Dosya Gönderilemedi.")


            continue

        elif command == "close":  # Ftpden çıkma login ekranına geri götürme

            try:
                resp=ftp.close()
                ftp_fn.myLogin(ftp_fn)
                print("Bağlantıdan Başarı İle Çıkıldı.")
            except:
                print("HATA!:Bağlantıdan Çıkış Yapılamadı.")


            continue

        elif command == "exit":  # Programdan çıkma

            try:
                sys.exit()
                print("Programdan Başarı İle Çıkıldı.")
            except:
                print("HATA!:Programdan Çıkılamadı.")

            continue

