from subcamada import Subcamada
import sys
from quadro import Quadro
class Aplicacao(Subcamada): #Adaptacao
    """ Construtor da Classe Subcamada

    """
    def __init__(self):
        # print("__init__ (Apliacacao)")
        Subcamada.__init__(self, sys.stdin)

    """ Metodo que recebe um quadro na Aplicação de uma subcamada

    @param data: Quadro recebido
    """
    def recebe(self, data : Quadro):
        # print("recebe (Aplicacao)")
        #mostrar na tela os dados recebidos da subcamada
        print("[APP] Recebido: ", data.data)


    """ Metodo handle que dispara ao receber um input do terminal

    """
    def handle(self):
        # print("handle (Aplicacao)")
        dados = sys.stdin.readline()
        if dados.strip() == "##stop":
            self.parar()
        #continuar handle aplicação
        quadro = Quadro(data = dados.strip())
        print("[APP] Enviado: ", quadro.data)
        self.inferior.envia(quadro)


    """ Metodo desenvolvido para ser utilizado internamente como uma flag de stop, assim o usuario pode encerra a aplicação quando desejar 

    """
    def parar(self):
        # print("parar (Aplicacao) - Encerrando Aplicação")
        # stop = Quadro(numSequencia = 0, data = "stop")
        # self.inferior.envia(stop)
        sys.exit()
