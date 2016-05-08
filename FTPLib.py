
import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT

class Error(Exception): pass # pass hata oluşunca program kapanmaması için.
class error_temp(Error): pass
class error_reply(Error): pass
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
        self.af = self.sock.family
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

    def close(self):
        try:
            file = self.file
            self.file = None
            if file is not None:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock is not None:
                sock.close()

    def quit(self):
        resp = self.sendcommand('QUIT')
        self.close()
        return resp

    def mkd(self, name):
        resp = self.sendcommand('MKD ' + name)
        return resp

    def delete(self, filename):
        resp = self.sendcommand('DELE ' + filename)
        if resp[:3] in {'250', '200'}:
            return resp
        else:
            raise error_perm(resp)

    def cwd(self, name):
        if name == '..':
            try:
                return self.sendcommand('CDUP')
            except error_perm as msg:
                if msg.args[0][:3] != '500':
                    raise
        elif name == '':
            name = '.'
        cmd = 'CWD ' + name
        return self.sendcommand(cmd)

    def rmd(self, name):
        return self.sendcommand('RMD ' + name)

    def size(self, filename):
        resp = self.sendcommand('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            return int(s)

    def pwd(self):
        resp = self.sendcommand('PWD')
        return resp

    def dir(self):
        resp = self.sendcommand('LIST')
        return resp

    def retrbinary(self, cmd, callback, blocksize=8192, rest=None):

        self.sendcommand('TYPE I')

        with self.transfercmd(cmd, rest) as conn:
            while 1:
                data = conn.recv(blocksize)
                if not data:
                    break
                callback(data)
            # shutdown ssl layer
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                conn.unwrap()
        return self.getanswer()

    def makeport(self):
        '''Create a new socket and send a PORT command for it.'''
        err = None
        sock = None
        for res in socket.getaddrinfo(None, 0, self.af, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
                sock.bind(sa)
            except OSError as _:
                err = _
                if sock:
                    sock.close()
                sock = None
                continue
            break
        if sock is None:
            if err is not None:
                raise err
            else:
                raise OSError("getaddrinfo returns an empty list")
        sock.listen(1)
        port = sock.getsockname()[1]  # Get proper port
        host = self.sock.getsockname()[0]  # Get proper host
        if self.af == socket.AF_INET:
            resp = self.sendport(host, port)
        else:
            resp = self.sendport(host, port)
        if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
            sock.settimeout(self.timeout)
        return sock

    def sendport(self, host, port):

        hbytes = host.split('.')
        pbytes = [repr(port // 256), repr(port % 256)]
        bytes = hbytes + pbytes
        cmd = 'PORT ' + ','.join(bytes)
        return self.sendcommand(cmd)

    def ntransfercmd(self, cmd, rest=None):
        size = None
        with self.makeport() as sock:
            if rest is not None:
                self.sendcommand("REST %s" % rest)
            resp = self.sendcommand(cmd)
            # See above.
            if resp[0] == '2':
                resp = self.getanswer()
            if resp[0] != '1':
                raise error_reply(resp)

            conn, sockaddr = sock.accept()
            if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                conn.settimeout(self.timeout)
        return conn, size

    def transfercmd(self, cmd, rest=None):
        return self.ntransfercmd(cmd, rest)[0]


try:
    import ssl
except ImportError:
    _SSLSocket = None
else:
    _SSLSocket = ssl.SSLSocket