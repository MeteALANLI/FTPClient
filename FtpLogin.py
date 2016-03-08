from ftplib import FTP
class FTPLogin:
    domain="localhost"
    ftp = FTP(domain)
    login  = ftp.login(user='root', passwd='123456')
    file = "deneme.txt"
    #ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
    ftp.retrbinary("RETR " + file ,open(file, 'wb').write)