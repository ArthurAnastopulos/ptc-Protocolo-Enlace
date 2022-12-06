import sys
from queue import Queue
from subcamada import Subcamada
from quadro import Quadro

class Arquitetura(Subcamada):
    def __init__(self, tout):
        print("__init__ (Arquitetura)")
        self.__tout = tout
        Subcamada.__init__(self, self.__tout)
        self.__state = self.ocioso
        self.__quadro = None
        self.__filaMsg = Queue() # Fila de Mensagens

    def recebe(self, quadro):
        print("recebe (Arquitetura)")
        self.__quadro = quadro

    def envia(self, quadro):
        print("envia (Arquitetura)")
        self.__quadro = quadro

    def ocioso(self, quadro : Quadro):
        print("ocioso (Arquitetura)")

    def espera(self, quadro :  Quadro, tout : bool = False):
        print("espera (Arquitetura)")

    def handle(self):
        print("handle (Arquitetura)")
        pass

    def handle_timeout(self):
        print("handle_timeout (Arquitetura)")
        if self.__state == self.espera:
            self.__state(self.__quadro, True)
