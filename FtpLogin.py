import sys, os, os.path, operator
from ftplib import FTP
import FTPFunctions


def myLogin():  # Giriş yaptıran method yanls giris olursa bir daha girmek icin
    while True:
        host = str(input("Server Adresini Giriniz :"))

        if "http://" in host:  # Host Ip adresini almak için taraycidan alinirsa diye http:// silindi
            host = host.replace("http://", "")
        try:
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


class FTPLogin:
    ftp_fn = FTPFunctions.FTPFunctions
    print("SDUFTP'ye hoşgeldiniz!")
    ftp = myLogin()#İnternet dağında bir tünel açıldı
    path = ftp.pwd()
    while True:
        command = str(input("Bir komut giriniz:"))
        if command == "yardim":
            print(ftp_fn.getHelp())
            continue
        elif command.__contains__("cd "):  # Dizin değiştirme

            continue
        elif command == "pwd":  # Bulunan dizin ismi
            continue
        elif command.__contains__('get'):  # Dosya alma komutu get alınacakdosya alınansodya adı
            continue
        elif command == "send":  # Dosya gönderme
            continue
        elif command == "gulegule":  # Ftpden çıkma login ekranına geri götürme
            ftp.close()
            myLogin()
            continue
        elif command == "cikis":  # Programdan çıkma
            sys.exit()
        else:
            print("Invaild command!!Please check you command or type 'yardim' for all commands")
            continue
