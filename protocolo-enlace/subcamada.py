from enquadramento import Enquadramento
from callback import Callback

class Subcamada(Callback):
    def __init__(self, serial, tout):
        self.__serial = serial
        self.__tout = tout
        Callback.__init__(self, self.__serial, self.__tout)
        self.inferior = None
        self.superior = None

    def envia(self, subcamada):
        print('envia')
        self.superior.envia(subcamada)

    def recebe(self, subcamada):
        print('recebe')
        self.superior.recebe(subcamada)

    def conecta(self, lower):
        print('connect')
        self.inferior = lower
        lower.superior = self