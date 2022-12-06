from quadro import Quadro
from pypoller import poller

class Subcamada(poller.Callback):
    def __init__(self, * args): ## * args para conseguir enviar os diversos argumentos que serão usados pelo Callback/Handler nas diferentes partes do código
        poller.Callback.__init__(self, *args)
        self.inferior = None
        self.superior = None

    def envia(self, quadro):
        self.inferior.envia(quadro)

    def recebe(self, quadro):
        self.inferior.recebe(quadro)

    def conecta(self, superior):
        self.superior = superior
        superior.inferior = self

        
        