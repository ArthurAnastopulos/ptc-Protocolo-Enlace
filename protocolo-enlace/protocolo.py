# protocol poller instancia aqui
from subcamada import Subcamada
from enquadramento import Enquadramento
from pypoller import poller
from aplicacao import Aplicacao
from arquitetura import Arquitetura
import sys

class Protocolo(Subcamada):
    """ Construtor do Protocolo
   
    @param serial: porta serial
    @param tout: timeout
    """
    def __init__(self, serial, tout):
        print("Protocolo (__init__)")
        self.__serial = serial
        self.__tout = tout
        self.__enq = Enquadramento(port=self.__serial, tout=self.__tout)
        self.__app = Aplicacao()
        self.__arq = Arquitetura(tout=self.__tout)
        
        #Conectar as subcamadas
        self.__enq.conecta(self.__arq);
        self.__arq.conecta(self.__app)

        # cria o Poller e registra os callbacks
        self.__sched = poller.Poller()
        self.__sched.adiciona(self.__enq)
        self.__sched.adiciona(self.__app)
        self.__sched.adiciona(self.__arq)

    """ Metodo para iniciar e fazer o despache do protocolo
   
    """
    def iniciar(self):
        print("Protocolo (Despache)")
        self.__app.iniciar()
        self.__sched.despache()
        