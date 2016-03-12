import sys, os, os.path, operator
class FTPFunctions:
    def __init__(self, name):
        self.name = name

    def upload(self):
        return
    def download(self):
        return

    @classmethod
    def getHelp(cls):
        response ="listele\t'Klasörleri listeler'\n bye\t'Login Ekranina çıkış verir' \n exit\t'Programdan çıkmayı sağlar' "
        return response