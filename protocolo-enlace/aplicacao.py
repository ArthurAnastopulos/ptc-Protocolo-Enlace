from subcamada import Subcamada
import sys
from quadro import Quadro
class Aplicacao(Subcamada):
    def __init__(self):
        Subcamada.__init__(self, sys.stdin)


    def recebe(self):
        #mostrar na tela os dados recebidos da subcamada
        print("Recebido:")

    def handle(self):
        dados = sys.stdin.readline()

        #continuar handle aplicação

    def iniciar(self):
        print("Inicia")

    def parar(self):
        print("Para")