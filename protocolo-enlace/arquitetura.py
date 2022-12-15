import sys
from queue import Queue
from subcamada import Subcamada
from quadro import Quadro

class Arquitetura(Subcamada):
    def __init__(self, tout):
        print("__init__ (Arquitetura)")
        self.__tout = tout
        Subcamada.__init__(self, None, self.__tout)
        self.__sequenciaM = 0
        self.__sequenciaN = 0
        self.__state = self.ocioso
        self.__quadro = None
        self.__filaMsg = Queue() # Fila de Mensagens

    def recebe(self, quadro : Quadro):
        print("recebe (Arquitetura)")
        self.__quadro = quadro
        print("RECEBE timeout habilitado ? : ",self.timeout_enabled)
        print("Data do Quadro: ", self.__quadro.getData())
        print("Tipo do Quadro: ", self.__quadro.getTipoQuadro())
        print("NumSequencia: ", self.__quadro.getNumSequencia())
        print("TipoMsgArq: ", self.__quadro.getTipoMsgArq())
        print("Estado da Arquitetura durante recibimento: ", self.__state)
        self.__state(self.__quadro)
        if(quadro.getTipoMsgArq() == 0) :
            self.__sequenciaM = not self.__sequenciaM

    def envia(self, quadro : Quadro):
        print("envia (Arquitetura)")
        print("Estado da Arquitetura durante envio: ", self.__state)
        print("ENVIA timeout habilitado ? : ",self.timeout_enabled)
        self.__quadro = quadro
        self.__filaMsg.put(self.__quadro)

        if self.__quadro.getData() == "reset":
            print("reset (Arquitetura)")
            self.__state = self.ocioso ##Muda para estado ocioso
            self.__quadro = None #limpa o atributo quadro da arquitetura
        if self.__state == self.ocioso:
            print("Arquitetura envia ocioso")
            if self.__filaMsg.qsize() > 1:
                self.inferior.envia(self.__filaMsg.get()) # !dataN da Modelagem da MEF
                self.__sequenciaN = not self.__sequenciaN
            self.inferior.envia(self.__filaMsg.get())
            self.__state = self.espera

    # 0 - recebe (M)
    # 1 - transmite (_M)
    def ocioso(self, quadro : Quadro):
        print("ocioso (Arquitetura)")
        self.disable_timeout()
        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia == self.__sequenciaM):
            print("--- Data M Recebido ---")
            print("NumSequencia: ", quadro.getNumSequencia, " Sequencia Correta: ", self.__sequenciaM )
            print("TipoMsgArq: ", quadro.getTipoMsgArq)

            ack = Quadro.__init__(tipoMsgArq = 1, numSequencia = quadro.getNumSequencia)
            self.inferior.envia(ack)
            self.superior.recebe(quadro)
            self.__state = self.ocioso

        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia != self.__sequenciaM):
            print("--- Data _M Recebido ---")
            print("Necessario Retransmissão")
            print("Sequencia Recebida: ", quadro.getNumSequencia, " Sequencia Correta: ", self.__sequenciaM)
            print("TipoMsgArq: ", quadro.getTipoMsgArq)

            ack = Quadro.__init__(tipoMsgArq = 1, numSequencia = quadro.getNumSequencia)
            self.inferior.envia(ack)
            self.__state = self.ocioso


    def espera(self, quadro :  Quadro, tout : bool = False):
        print("espera (Arquitetura)")
        if(not self.timeout_enabled):
            print("Caso não tenho")
            self.reload_timeout()
            self.enable_timeout()

        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia == self.__sequenciaM):
            print("--- Data M --- Return ackM ---")
            ack = Quadro(tipoMsgArq = 1, numSequencia = quadro.getNumSequencia)
            self.inferior.envia(ack)
            self.superior.recebe(quadro)
            self.__sequenciaM = not self.__sequenciaM
            self.__state = self.espera

        if (quadro.getTipoMsgArq == 0) and (quadro.getNumSequencia != self.__sequenciaM):
            print("--- Data_M --- Return ack_M ---")
            ack = Quadro(tipoMsgArq = 1, numSequencia = self.__sequenciaM)
            self.inferior.envia(ack)
            self.__state = self.espera

        if (quadro.getTipoMsgArq == 1) and (quadro.getNumSequencia != self.__sequenciaN):
            print(" ----- ack_N ----- Retransmitido")
            self.__quadro.setNumSequencia(numSequencia = not self.__quadro.getNumSequencia)
            self.inferior.envia(self.__quadro)
            self.__state = self.espera
        
        if (quadro.getTipoMsgArq == 1) and (quadro.getNumSequencia == self.__sequenciaN):
            print(" ----- ack N ----- ")
            self.__sequenciaN = not self.__sequenciaN
            self.__state = self.ocioso

        if tout:
            print("----- retransmite -----")
            self.inferior.envia(self.__quadro)
            self.disable_timeout()

    def handle(self):
        print("handle (Arquitetura)")
        pass

    def handle_timeout(self):
        print("handle_timeout (Arquitetura)")
        if self.__state == self.espera:
            self.__state(self.__quadro, True)
