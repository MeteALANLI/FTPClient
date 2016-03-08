from ftplib import FTP
import FTPFunctions
import sys, os, os.path, operator


class FTPLogin:
    domain="localhost"
    ftp = FTP(domain)
    login  = ftp.login(user='root', passwd='123456')
    print(ftp.getwelcome())
    print(ftp.retrlines('LIST'))
    file = "deneme.txt"
    FTPFunctions.FTPFunctions.upload()
    #ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
    #ftp.retrbinary("RETR " + file ,open(file, 'wb').write)