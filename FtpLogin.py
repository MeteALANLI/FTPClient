import sys, os, os.path, operator
from ftplib import FTP
import Functions
class FTPLogin:
    ftp_fn = Functions.Functions
    print("SDUFTP'ye hoşgeldiniz!")
    ftp = ftp_fn.myLogin(ftp_fn)#İnternet dağında bir tünel açıldı
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
            ftp_fn.myLogin(ftp_fn)
            continue
        elif command == "cikis":  # Programdan çıkma
            sys.exit()
        else:
            print("Invaild command!!Please check you command or type 'yardim' for all commands")
            continue
