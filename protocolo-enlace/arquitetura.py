import sys
from queue import Queue
from subcamada import Subcamada
from quadro import Quadro

class Arquitetura(Subcamada):
    def __init__(self, tout):
        print("__init__ (Arquitetura)")
        self.__tout = tout
        Subcamada.__init__(self, self.__tout)
        self.__sequenciaM = 0
        self.__sequenciaN = 0
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

    # 0 - recebe (M)
    # 1 - transmite (_M)
    def ocioso(self, quadro : Quadro):
        print("ocioso (Arquitetura)")
        self.disable_timeout()
        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia == self.__sequenciaM):
            print("--- Data M Recebido ---")
            print("NumSequencia: ", quadro.getNumSequencia )
            print("TipoMsgArq: ", quadro.getTipoMsgArq)

            ack = Quadro.__init__(tipoMsgArq = 1, numSequencia = quadro.getNumSequencia)
            self.inferior.envia(ack)
            self.superior.recebe(quadro)
            #self.__state = self.ocioso

        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia != self.__sequenciaM):
            print("--- Data _M Recebido ---")
            print("Necessario Retransmissão")
            print("Sequencia Recebida: ", quadro.getNumSequencia, " Sequencia Correta: ", self.__sequenciaM)
            print("TipoMsgArq: ", quadro.getTipoMsgArq)

            ack = Quadro.__init__(tipoMsgArq = 1, numSequencia = quadro.getNumSequencia)
            self.inferior.envia(ack)
            #self__state = self.ocioso


    def espera(self, quadro :  Quadro, tout : bool = False):
        print("espera (Arquitetura)")

        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia == self.__sequenciaM):
            print("--- Data M---")
            ack = Quadro(tipoMsgArq = 1, numSequencia = quadro.getNumSequencia)
            self.inferior.envia(ack)
            self.superior.recebe(quadro)
            self.__sequenciaM = not self.__sequenciaM
            #self__state = self.espera

        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia != self.__sequenciaM):
            print(" ----- ")
            ack = Quadro(tipoMsgArq = 1, numSequencia = self.__sequenciaM)
            self.inferior.envia(ack)

        if (quadro.getTipoMsgArq == 1) and (quadro.getNumSequencia != self.__sequenciaN):
            print(" ----- ")
            self.__quadro.setNumSequencia(numSequencia = self.__quadro.getNumSequencia)
        self.inferior.envia(self.__quadro)
        
        if (quadro.getTipoMsgArq == 1) and (quadro.getNumSequencia == self.__sequenciaN):
            print(" ---- ")
            self.__sequenciaN = not self.__sequenciaN
            self.__state = self.ocioso

        if tout:
            print("retransmite")
            self.inferior.envia(self.__quadro)
            self.disable_timeout()

    def handle(self):
        print("handle (Arquitetura)")
        pass

    def handle_timeout(self):
        print("handle_timeout (Arquitetura)")
        if self.__state == self.espera:
            self.__state(self.__quadro, True)
