from FTPLib import FTP
import os
class Functions:

    @classmethod
    def upload(self):
        return
    @classmethod
    def download(cls, filename, path, ftp):
        homefolder = os.environ['userprofile']
        download_path = homefolder + '/' + path
        local_filename = os.path.join(download_path, filename)
        print(local_filename)
        try:
            file = open(local_filename, "wb")
        except:
            print("Dosya oluşturulamadı.")

        try:
            ftp.retrbinary("RETR " + filename, file.write, 8 * 1024)
        except:
            print("Dosya alınamadı")
        file.close()

        return "Dosya alindi"


    @classmethod
    def getHelp(cls):
        response = "K   O   M   U   T   L   A   R\n"\
                  "sda                                      -   Su Anki Klasor\n" \
                  "listele                                  -   Listele\n"\
                  "k_gir 'Klasor Adi'                       -   Klasore Gir\n"\
                  "k_olustur                                -   Klasor Olustur\n"\
                  "d_al                                     -   Dosya Al\n" \
                  "d_yukle                                  -   Dosya Yukle\n" \
                  "d_sil 'Dosya Adi'                        -   Dosya Siler\n"\
                  "boyut                                    -   Boyut\n"\
                  "degistir 'Dosya Adi'  'Dosya Adi'        -   Dosya Adı Degistir\n "\
                  "kapat                                    -   Baglantiyi Kapat\n" \
                  "cikis                                    -   Programdan Cik\n"
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


