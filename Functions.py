from FTPLib import FTP
class Functions:

    @classmethod
    def upload(self):
        return
    @classmethod
    def download(self):
        return
    @classmethod
    def getHelp(cls):
        response = "K   O   M   U   T   L   A   R\n"\
                  "pwd      -   Dizin Adları\n" \
                  "dir      -   Dizinleri Listele\n" \
                  "mkd      -   Dosya ekle\n" \
                  "get      -   Dosya Al\n" \
                  "send     -   Dosya Gönder\n" \
                  "close    -   Bağlantıyı kapat\n" \
                  "exit     -   Programdan çık\n"\
                  "size     -   Dosya Boyutu\n"\
                  "rmd 'Dosya Adı'     -   Dizini Siler\n"\
                  "cwd 'Dosya Adı'     -   dizinler arası geçiş\n"
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


