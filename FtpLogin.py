import sys
from Functions import Functions
class FTPLogin:
    ftp_fn = Functions
    print("SDUFTP'ye hoşgeldiniz!")
    ftp = ftp_fn.myLogin(ftp_fn)#İnternet dağında bir tünel açıldı
    path = ftp.pwd()
    print(Functions.getHelp())
    while True:
        command = str(input("Bir komut giriniz:"))

        if command == "yardim":
            print(Functions.getHelp())
            continue

        elif command == "sda":  # Bulunan dizin ismini verir

            try:
                print(ftp.pwd())
            except:
                print("HATA!:Dizin Yolu Bulunamadı.")
            continue

        elif command == "listele":
            continue # şu an çalışmamaktadır
            try:
                resp=ftp.dir()
                print("Başarı ile Listelendi.")
            except:
                print("HATA!: Listelenemedi.")
            continue

        elif command.__contains__("k_olustur"):

            mName=command.replace("k_olustur ","")

            try:
                resp=ftp.mkd(mName)
                print("Klasör Başarı ile Oluşturuldu.")
            except:
                print("HATA!:Klasör Oluşturulamadı.")

            continue


        elif command.__contains__("d_sil"):
            dosyaSil=command.replace("d_sil ","")
            try:
                print(ftp.delete(dosyaSil))
            except:
                print("HATA!:Dosya Silinemedi.")
            continue



        elif command.__contains__("d_boyut"):
            dosya=command.replace("d_boyut ","")
            try:
                print("Dosya boyutu : ",ftp.delete(dosya))
            except:
                print("HATA!:Dosya boyutu belirsiz.")
            continue

        elif command.__contains__("d_degistir"):
            dosya = command.replace("d_degistir ", "")
            try:
                print("Dosya dizin degisti : ", ftp.rename(dosya))
                print("Suan ki yeriniz : ", ftp.pwd())
            except:
                print("HATA!:Dosya adı belirsiz.")
            continue

        elif command.__contains__("d_al"):
            try:
                command = command.replace("d_al ", "")
                command = command.split(" ")
                resp = ftp_fn.download(command[0], command[1], ftp)
                print("Dosya Başarı ile Alındı.")
            except:
                print("HATA!:Dosya Gönderilemedi.")
            continue

        elif command == "d_yukle":
            try:
                resp=ftp_fn.upload()
                print("Dosya Başarı ile Yüklendi.")
            except:
                print("HATA!:Dosya Yüklenemedi.")
            continue

        elif command == "kapat":  # Ftpden çıkma login ekranına geri götürme
            try:
                resp=ftp.close()
                print("Bağlantı Kapatıldı.")
                ftp_fn.myLogin(ftp_fn)
            except:
                print("HATA!:Bağlantıdan Çıkış Yapılamadı.")
            continue

        elif command == "cikis":  # Programdan çıkma
            sys.exit()
