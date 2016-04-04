
import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT

class Error(Exception): pass # pass hata oluşunca program kapanmaması için.
class error_temp(Error): pass
class error_perm(Error): pass

TAKI = '\r\n'#Her FTP Komutundan sonra olması gereken bir takı
B_TAKI = b'\r\n'#binary hali
FTP_PORT = 21#hangi porttan bağlantı olacağı
MAXLINE = 8192#max kaç satır bilgi alınacak

class FTP:
    host = ''
    port = FTP_PORT
    maxline = MAXLINE
    timeout = ''
    command = ''
    sock = None
    file = None
    welcome = None
    encoding = "utf-8"
    is_passive = 0

    def __init__(self,host="",port = 0,user= "",passwd = "",timeout=_GLOBAL_DEFAULT_TIMEOUT):
        self.timeout = timeout # self classtan o anki oluşan nesnedir
        if host:
            self.connect(host)
            if user:
                self.login(user, passwd)
    # init classtan nesne oluşturulduğunda çalışan fonksiyon
    def connect(self, host='', port=0, timeout=-999):
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # soketin oluşturulduğu satır
        self.sock.connect((self.host, self.port))
        self.file = self.sock.makefile("r", encoding=self.encoding) # sokette yapılan işlemlerin yapılacağı dosya
        self.welcome = self.getanswer()
        return self.welcome

    def login(self, user="", passwd=""):
        if not user:
            user = 'anonymous'
        if not passwd:
            passwd = ''
        resp = self.sendcommand('USER ' + user)
        if resp[:1] == '3':
            resp = self.sendcommand('PASS ' + passwd)
        return resp

    def getwelcome(self):
        return self.welcome

    def sendcommand(self, command):   #ftp nin bizden istediği komutları gonderdiğimiz fonksiyon
        self.command = command + TAKI
        self.sock.sendall(self.command.encode(self.encoding))
        return self.getanswer()

    def getanswer(self):
        resp = self.getmultiline()
        c = resp[:1]
        if c in {'1', '2', '3'}:
            return resp
        if c == '4':
            raise error_temp(resp)
        if c == '5':
            raise error_perm(resp)

    def getmultiline(self):
        line = self.getline()
        if line[3:4] == '-':
            code = line[:3]
            while 1:
                nextline = self.getline()
                line = line + ('\n' + nextline)
                if nextline[:3] == code and \
                        nextline[3:4] != '-':
                    break
        return line

    def getline(self):
        line = self.file.readline(self.maxline + 1)
        if line[-2:] == TAKI:
            line = line[:-2]
        elif line[-1:] in TAKI:
            line = line[:-1]
        return line

    def mkd(self, name):
        resp = self.sendcommand('MKD ' + name)
        return resp

    def pwd(self):
        resp = self.sendcommand('PWD')
        return resp

    def dir(self):
        resp = self.sendcommand('LIST')
        return resp
