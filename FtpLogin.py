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
                print(ftp.sda())
            except:
                print("HATA!:Dizin Yolu Bulunamadı.")
            continue

        elif command == "listele":
            continue# şu an çalışmamaktadır
            try:
                resp=ftp.listele()
                print("Başarı ile Listelendi.")
            except:
                print("HATA!: Listelenemedi.")
            continue

        elif command.__contains__("k_ekle"):

            mName=command.replace("k_ekle ","")

            try:
                resp=ftp.k_ekle(mName)
                print("Klasör Başarı ile Oluşturuldu.")
            except:
                print("HATA!:Klasör Oluşturulamadı.")

            continue



        elif command.__contains__("d_sil"):
            dosyaSil=command.replace("d_sil ","")
            try:
                print(ftp.d_sil(dosyaSil))
            except:
                print("HATA!:Dosya Silinemedi.")
            continue

          elif command.__contains__("k_sil"):
            dosyaSil=command.replace("k_sil ","")
            try:
                print(ftp.k_sil(klasorSil))
            except:
                print("HATA!:Klasör Silinemedi.")
            continue


        elif command.__contains__("d_boyut"):
            dosya=command.replace("d_boyut ","")
            try:
                print("Dosya boyutu : ",ftp.d_boyut(dosya))
            except:
                print("HATA!:Dosya boyutu belirsiz.")
            continue


         elif command.__contains__("k_boyut"):
            dosya=command.replace("k_boyut ","")
            try:
                print("Klasör boyutu : ",ftp.k_boyut(klasor))
            except:
                print("HATA!:Dosya boyutu belirsiz.")
            continue


        elif command.__contains__("d_degistir"):
            dosya = command.replace("d_degistir ", "")
            try:
                print("Dosya dizin degisti : ", ftp.d_degistir(dosya))
                print("Suan ki yeriniz : ", ftp.sda())
            except:
                print("HATA!:Dosya adı belirsiz.")
            continue

        elif command.__contains__("d_al"):  # Dosya gönderme
            try:
                resp = ftp_fn.download("deneme.txt", "Desktop", ftp)
                print("Dosya Başarı ile Alındı.")
            except:
                print("HATA!:Dosya Gönderilemedi.")
            continue

        elif command == "d_yukle":  # Dosya gönderme
            try:
                resp=ftp.d_yukle()
                print("Dosya Başarı ile Yüklendi.")
            except:
                print("HATA!:Dosya Yüklenemedi.")
            continue

        elif command == "kapat":  # Ftpden çıkma login ekranına geri götürme
            try:
                resp=ftp.kapat()
                print("Bağlantı Kapatıldı.")
                ftp_fn.myLogin(ftp_fn)
            except:
                print("HATA!:Bağlantıdan Çıkış Yapılamadı.")
            continue

        elif command == "cikis":  # Programdan çıkma
            sys.cikis()
