# protocol poller instancia aqui
from subcamada import Subcamada
from enquadramento import Enquadramento
from pypoller import poller
from aplicacao import Aplicacao

class Protocolo(Subcamada):
    def __init__(self, serial, tout):
        self.__serial = serial
        self.__tout = tout
        self.__enq = Enquadramento.__init__(port=self.__serial, tout=self.__tout)
        self.__app = Aplicacao.__init__()

        #Conectar as subcamadas

        # cria o Poller e registra os callbacks
        self.__sched = poller.Poller()
        self.__sched.adiciona(self.__enq)
        self.__sched.adiciona(self.__app)

    def iniciar(self):
        self.__app.iniciar()
        self.__sched.despache()