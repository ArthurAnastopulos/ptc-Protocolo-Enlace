from subcamada import Subcamada
import sys
from quadro import Quadro
class Aplicacao(Subcamada): #Adaptacao
    """ Construtor da Classe Subcamada

    """
    def __init__(self):
        print("__init__ (Apliacacao)")
        Subcamada.__init__(self, sys.stdin)
        self.__sequencia = 0

    """ Metodo que recebe um quadro na Aplicação de uma subcamada

    @param data: Quadro recebido
    """
    def recebe(self, data : Quadro):
        print("recebe (Aplicacao)")
        #mostrar na tela os dados recebidos da subcamada
        print("Recebido: ", data.getData())


    """ Metodo handle que dispara ao receber um input do terminal

    """
    def handle(self):
        print("handle (Aplicacao)")
        dados = sys.stdin.readline()
        if dados.strip() == "stop":
            self.parar()
        #continuar handle aplicação
        self.__sequencia = not self.__sequencia
        quadro = Quadro(tipoMsgArq = 0, numSequencia = self.__sequencia, data = dados)
        print("Enviado: ", quadro.getData())
        self.inferior.envia(quadro)


    """ Metodo desenvolvido para ser utilizado internamente como um flag de start para interface da API do Protocolo

    """
    def iniciar(self):
        print("iniciar (Aplicacao)")
        inicio = Quadro(numSequencia = self.__sequencia, data = "start")
        self.inferior.envia(inicio)


    """ Metodo desenvolvido para ser utilizado internamente como uma flag de stop, assim o usuario pode encerra a aplicação quando desejar 

    """
    def parar(self):
        print("parar (Aplicacao) - Encerrando Aplicação")
        # stop = Quadro(numSequencia = 0, data = "stop")
        # self.inferior.envia(stop)
        sys.exit()
