from ftplib import FTP
from FTPPackage import FTPFunctions
import sys, os, os.path, operator


def meLogin():  # giriş yaptıran method yanls giris olursa bir daha girmek icin
    while 1:
        host = str(input("Write FTP server adress :"))
        user_n = str(input("Write your username :"))
        user_p = str(input("write your passwd :"))
        if "http://" in host:#Host Ip adresini almak için taraycidan alinirsa diye http:// silindi
            host = host.replace("http://", "")
        try:
            ftp = FTP(host)
        except:
            print("Host name not resolved")
            meLogin()
        try:
            ftp.login(user=user_n, passwd=user_p)#giriş burda yapıldı
        except:
            print("Username or Password is wrong")
            meLogin()
        else:
            print(ftp.getwelcome())
            break
    return ftp#Eğer giriş düzgün ise buraya düsüp geriye döndürcek girdiği FTP'yi


class FTPLogin:
    ftp_fn = FTPFunctions.FTPFunctions
    print("Welcome SDUFTP!")
    ftp = meLogin()
    path = ftp.pwd()
    value = 1
    while value == 1:
        command = str(input("Type a command:"))
        if command == "yardim":
            print(ftp_fn.getHelp())
            continue
        elif command.__contains__("cd"):  # dizin değiştirme
            continue
        elif command == "pwd":  # bulunan dizin ismi
            continue
        elif command.__contains__('get'):  # dosya alma komutu get alınacakdosya alınansodya adı
            print("Get")
            continue
        elif command == "send":  # dosya gönderme
            continue
        elif command == "bye":  # ftpden çıkma login ekranına geri götürme
            ftp.close()
            meLogin()
            continue
        elif command == "exit":  # programdan çıkma
            sys.exit()
        else:
            print("Invaild command!!Please check you command or type 'yardim' for all commands")
            continue
