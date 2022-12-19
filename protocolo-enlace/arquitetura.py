import sys
from queue import Queue
from subcamada import Subcamada
from quadro import Quadro

class Arquitetura(Subcamada):

    """ Metodo Construtor da Arquitetura

    @param tout: timeout
    """
    def __init__(self, tout):
        # print("__init__ (Arquitetura)")
        self.__tout = tout
        Subcamada.__init__(self, None, self.__tout)
        self.__countRetrans = 0
        self.__sequenciaM = 0
        self.__sequenciaN = 0
        self.__state = self.ocioso
        self.__quadro = None
        self.__filaMsg = Queue() # Fila de Mensagens

    """ Metodo que recebe um quadro de uma subcamada 

    @param quadro: Quadro recebido
    """
    def recebe(self, quadro : Quadro):
        print("[ARQ] Recebeu Quadro")
        self.__quadro = quadro
        # print("RECEBE timeout habilitado ? : ",self.timeout_enabled)
        # print("Data do Quadro: ", self.__quadro.getData())
        # print("Tipo do Quadro: ", self.__quadro.getTipoQuadro())
        # print("NumSequencia: ", self.__quadro.getNumSequencia())
        # print("TipoMsgArq: ", self.__quadro.getTipoMsgArq())
        self.__state(self.__quadro)
        if(quadro.tipoMsgArq == 0) :
            self.__sequenciaM = not self.__sequenciaM

    """ Metodo que envia um quadro para uma subcamada 

    @param quadro: Quadro enviado
    """
    def envia(self, quadro : Quadro):
        # print("envia (Arquitetura)")
        print("[ARQ] Enviou Quadro")
        quadro.numSequencia = self.__sequenciaN
        self.__quadro = quadro
        self.__filaMsg.put(self.__quadro)

        if self.__state == self.ocioso:
            if self.__filaMsg.qsize() > 1:
                self.inferior.envia(self.__filaMsg.get()) # !dataN da Modelagem da MEF
                self.__sequenciaN = not self.__sequenciaN
            self.inferior.envia(self.__filaMsg.get())
            self.reload_timeout()
            self.enable_timeout()
            self.__state = self.espera

    # 0 - recebe (M)
    # 1 - transmite (N)
    """ Estado Ocioso da Arquitetura 

    @param quadro: Quadro a ser tratado pela MEF
    """
    def ocioso(self, quadro : Quadro):
        self.disable_timeout()
        if (quadro.tipoMsgArq == 0) and (quadro.numSequencia == self.__sequenciaM):
            print("[ARQ] Data M Recebido - Estado: Ocioso")
            # print("NumSequencia: ", quadro.getNumSequencia, " Sequencia Correta: ", self.__sequenciaM )
            # print("TipoMsgArq: ", quadro.getTipoMsgArq)

            ack = Quadro(tipoMsgArq = 1, numSequencia = quadro.numSequencia)
            self.inferior.envia(ack)
            self.superior.recebe(self.__quadro)
            self.__state = self.ocioso
            return

        if (quadro.tipoMsgArq == 0) and (quadro.numSequencia != self.__sequenciaM):
            print("[ARQ] Data _M Recebido - Estado: Ocioso")
            print("Necessario Retransmissão")
            # print("Sequencia Recebida: ", quadro.getNumSequencia, " Sequencia Correta: ", self.__sequenciaM)
            # print("TipoMsgArq: ", quadro.getTipoMsgArq)

            ack = Quadro(tipoMsgArq = 1, numSequencia = quadro.numSequencia)
            self.inferior.envia(ack)
            self.__state = self.ocioso
            return

    """ Estado Espera da Arquitetura 

    @param quadro: Quadro a ser tratado pela MEF
    @param tout: timeout para ser utilizado no caso de retransmissão
    """
    def espera(self, quadro :  Quadro, tout : bool = False):
        # print("espera (Arquitetura)")
        if tout:
            print("[ARQ] retransmite - Estado: espera")
            self.inferior.envia(self.__quadro)
            self.disable_timeout()
            return

        if (quadro.tipoMsgArq == 0) and (quadro.numSequencia == self.__sequenciaM):
            print("[ARQ] Data M / Return ackM - Estado: espera")
            ack = Quadro(tipoMsgArq = 1, numSequencia = quadro.numSequencia)
            self.inferior.envia(ack)
            self.superior.recebe(self.__quadro)
            self.__sequenciaM = not self.__sequenciaM
            self.__state = self.espera
            return

        if (quadro.tipoMsgArq == 0) and (quadro.numSequencia != self.__sequenciaM):
            print("[ARQ] Data_M - Return ack_M - Estado: espera")
            ack = Quadro(tipoMsgArq = 1, numSequencia = self.__sequenciaM)
            self.inferior.envia(ack)
            self.__state = self.espera
            return

        if (quadro.tipoMsgArq == 1) and (quadro.numSequencia != self.__sequenciaN):
            print("[ARQ] ack_N - Retransmitido - Estado: espera")
            print("[ARQ] Sequencia do Quadro: ", quadro.numSequencia, " | Sequencia N: ", self.__sequenciaN)
            self.__quadro.numSequencia = not self.__quadro.numSequencia
            self.inferior.envia(self.__quadro)
            self.__state = self.espera
            return
        
        if (quadro.tipoMsgArq == 1) and (quadro.numSequencia == self.__sequenciaN):
            print("[ARQ] ack N - Estado: espera")
            self.__sequenciaN = not self.__sequenciaN
            self.__state = self.ocioso
            return

    def handle(self):
        pass

    def handle_timeout(self):
        # print("handle_timeout (Arquitetura)")
        if self.__state == self.espera:
            self.__state(self.__quadro, True)
