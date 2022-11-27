from subcamada import Subcamada

class Aplicacao(Subcamada):
    def __init__(self):
        Subcamada.__init__(self)

    def recebe(self, dado:Subcamada):
        print('Recebido: ' , dado)

    def handle(self):
        # dados = de onde?
        
        quadro = Quadro(data = dados)      
        print("Enviando: " , quadro)    

