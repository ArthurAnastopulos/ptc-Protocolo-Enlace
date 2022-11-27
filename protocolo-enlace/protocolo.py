# protocol poller instancia aqui
from subcamada import Subcamada
from enquadramento import Enquadramento
from pypoller import poller

class Protocolo(Subcamada):
    def __init__(self):
        Subcamada.__init__(self, self.__serial, self.__tout)

    def envio(self, dados):
        
        self.superior.envia(dados)

        sched = poller.Poller
        sched.adiciona(self)
        sched.despache()

    def recebe(self,dados):
        #mostrar dados que foram recebidos da subcamada inferior
        print('Recebido:', dados)

        sched = poller.Poller
        sched.adiciona(self)
        sched.despache()

    def handle(self,dado):
        self.sequencia = not self.sequencia

        quadro = Enquadramento()      
        self.inferior.envia(quadro)
    