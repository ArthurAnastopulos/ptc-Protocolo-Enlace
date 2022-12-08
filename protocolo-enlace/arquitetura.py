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
        print("Data do Quadro: ", self.__quadro.data)
        print("Estado da Arquitetura durante recibimento: ", self.__state)
        self.__state(self.__quadro)

    def envia(self, quadro):
        print("envia (Arquitetura)")
        print("Estado da Arquitetura durante envio: ", self.__state)
        self.__quadro = quadro
        self.__filaMsg.put(self.__quadro)

        if self.__quadro.data == "reset":
            self.__state = self.ocioso ##Muda para estado ocioso
            self.__quadro = None #limpa o atributo quadro da arquitetura
        if self.__state == self.ocioso:
            if self.__filaMsg.qsize() > 1:
                self.inferior.envia(self.__filaMsg.get()) # !dataN da Modelagem da MEF
            self.inferior.envia(self.__filaMsgg.get())
            self.__state = self.espera

    def ocioso(self, quadro : Quadro):
        print("ocioso (Arquitetura)")
        self.disable_timeout()

    def espera(self, quadro :  Quadro, tout : bool = False):
        print("espera (Arquitetura)")

    def handle(self):
        print("handle (Arquitetura)")
        pass

    def handle_timeout(self):
        print("handle_timeout (Arquitetura)")
        if self.__state == self.espera:
            self.__state(self.__quadro, True)
