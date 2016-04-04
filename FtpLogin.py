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


        elif command == "pwd":  # Bulunan dizin ismini verir

            try:
                print(ftp.pwd())
            except:
                print("HATA!:Dizin Yolu Bulunamadı.")
            continue

        elif command == "dir":
            continue# şu an çalışmamaktadır
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
            try:
                print(ftp.delete(dosyaSil))
            except:
                print("HATA!:Dosya Silinemedi.")
            continue

        elif command.__contains__("rmd"):
            dosyaSil=command.replace("rmd ","")
            try:
                print(ftp.rmd(dosyaSil))
            except:
                print("HATA!:Klasör Silinemedi.")
            continue

        elif command.__contains__("size"):
            dosya=command.replace("size ","")
            try:
                print("Dosya boyutu : ",ftp.size(dosya))
            except:
                print("HATA!:Dosya boyutu belirsiz.")
            continue

        elif command.__contains__("cwd"):
            dosya = command.replace("cwd ", "")
            try:
                print("Dosya dizin degisti : ", ftp.cwd(dosya))
                print("Suan ki yeriniz : ", ftp.pwd())
            except:
                print("HATA!:Dosya adı belirsiz.")
            continue

        elif command.__contains__("get"):  # Dosya alma komututur.... alınacakdosya alınansodya adı
            continue #suan calismamaktadir
            command=command.replace("get ","")
            try:
                resp=ftp.get(command)
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
                print("Bağlantıdan Başarı İle Çıkıldı.")
                ftp_fn.myLogin(ftp_fn)
            except:
                print("HATA!:Bağlantıdan Çıkış Yapılamadı.")
            continue

        elif command == "exit":  # Programdan çıkma
            sys.exit()
