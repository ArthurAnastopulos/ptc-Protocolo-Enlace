from enquadramento import Enquadramento
from pypoller import poller

class Subcamada(poller.Callback):
    def __init__(self, serial, tout):
        self.__serial = serial
        self.__tout = tout
        poller.Callback.__init__(self, self.__serial, self.__tout)
        self.inferior = None
        self.superior = None

    def envia(self, quadro):
        self.superior.envia(quadro)

    def recebe(self, quadro):
        self.inferior.recebe(quadro)


    def conecta(self, superior):
        self.superior = superior
        superior.inferior = self

        
        