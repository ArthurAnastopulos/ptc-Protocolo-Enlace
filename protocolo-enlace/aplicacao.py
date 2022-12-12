from subcamada import Subcamada
import sys
from quadro import Quadro
class Aplicacao(Subcamada): #Adaptacao
    def __init__(self):
        print("__init__ (Apliacacao)")
        Subcamada.__init__(self, sys.stdin)
        self.__sequencia = 0

    def recebe(self, data : Quadro):
        print("recebe (Aplicacao)")
        #mostrar na tela os dados recebidos da subcamada
        print("Recebido: ", data.getData())

    def handle(self):
        print("handle (Aplicacao)")
        dados = sys.stdin.readline()
        if dados == "stop":
            self.parar()
        #continuar handle aplicação
        self.__sequencia = not self.__sequencia
        quadro = Quadro(tipoMsgArq = 0, numSequencia = self.__sequencia, data = dados)
        print("Enviado: ", quadro.getData())
        self.inferior.envia(quadro)

    def iniciar(self):
        print("iniciar (Aplicacao)")
        inicio = Quadro(numSequencia = self.__sequencia, data = "start")
        self.inferior.envia(inicio)

    def parar(self):
        print("parar (Aplicacao)")
        stop = Quadro(numSequencia = 0, data = "stop")
        self.inferior.envia(stop)