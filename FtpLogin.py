from ftplib import FTP
from FTPPackage import FTPFunctions
import sys, os, os.path, operator
#asd
class FTPLogin:
    ftp_fn = FTPFunctions.FTPFunctions
    print("Welcome SDUFTP!")
    host = str(input("Write FTP server adress :"))
    user_n = str(input("Write your username :"))
    user_p = str(input("write your passwd :"))
    if "http://" in host:
        host = host.replace("http://", "")
    try:
        ftp = FTP(host)
    except:
        print("Host name not resolved")
        sys.exit()
    try:
        login = ftp.login(user=user_n, passwd=user_p)
    except:
        print("Username or Password is wrong")
        sys.exit()
    else:
       print(ftp.getwelcome())
    path = ftp.pwd()
    value  = 1
    while value == 1:
        command = str(input("Type a command:"))
        if command == "help":
            print(ftp_fn.getHelp())
            continue
        else:
            print("Invaild command!!Please check you command or type 'help' for all commands")
            continue
