#!/usr/bin/python3

from serial import Serial
from subcamada import Subcamada
from quadro import Quadro
from crc import CRC16
import sys

## class Enquadramento(poller.Callback):
class Enquadramento(Subcamada): 

    """ Construtor do Enquadramento 

    @param port: Porta serial
    @param tout: timeout
    """
    def __init__(self, port, tout):
        # print("Enquadramento (__init__)")
        self.__port = port
        self.__tout = tout
        try:
            self.__serial = Serial(self.__port, 9600, timeout=None )
        except:
            print("Porta serial não foi encontrada. Encerrando Programa")
            sys.exit(0)
        Subcamada.__init__(self, self.__serial, self.__tout)
        ##poller.Callback.__init__(self, self.__serial, self.__tout)
        self.__buffer = bytearray()
        
        self.enable()
        ##self.disable_timeout()
        ##sched = poller.Poller()
        self.__state = self.ocioso
        ##sched.adiciona(self)
        ##sched.despache()

    
    """ Estado Ocioso do Enquadramento
   
    @param msg: Mensagem a ser tratada
    """
    def ocioso(self, msg):
        # print("[ENQ] Ociso")
        if(msg == b'\x7E'):
            self.enable_timeout()
            self.__state = self.prep

    """ Estado Preparação do Enquadramento
   
    @param msg: Mensagem a ser tratada
    """
    def prep(self, msg):
        # print("[ENQ] prep")
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg != b'\x7E'):
            self.__buffer += msg
            self.__state = self.rx

    """ Estado Escape do Enquadramento
   
    @param msg: Mensagem a ser tratada
    """
    def esc(self, msg):
        # print("[ENQ] esc")
        if(msg == b'\x7E' or msg == b'\x7D'):
            self.__buffer.clear()
            self.__state = self.ocioso
            self.disable_timeout()
        else:
            self.__buffer += bytes([msg[0] ^ 0x20])
            self.__state = self.rx    

    """ Estado Recepção do Enquadramento
   
    @param msg: Mensagem a ser tratada
    """
    def rx(self, msg):
        # print("[ENQ] rx")
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg == b'\x7E'):
            fcs = CRC16(self.__buffer)
            if fcs.check_crc():
                quadro = self.deserializeBuffer(self.__buffer)
                # print("Quadro: ", quadro, "  buffer: ", self.__buffer)
                self.superior.recebe(quadro) #recebe da Subcamada, não do enquadramento (Talvez mudar de nome, para não gerar confusão?)   
                self.__state = self.ocioso
                self.disable_timeout() 
                return True
            else:
                print("[ENQ] Quadro Corrompido!")
            self.__state = self.ocioso
            self.disable_timeout()        
            return False    
        else:
            self.__buffer += msg
        

    def handle(self):
        # print("[ENQ] handle")
        self.recebe()

    def handle_timeout(self):
        # print('[ENQ] handle_timeout')
        self.__state = self.ocioso
        self.__buffer.clear()
        self.disable_timeout()
    
    """ Metodo que envia um quadrao para a porta serial
   
    @param quadro: quadro a ser enviado
    """
    def envia(self,quadro):
        # print("Enquadramento (envia)")
        dados = bytearray()
        dados += b'\x7E'
        dados += quadro.serialize()
        dados += b'\x7E'
        print("[Enq] Envia Dados: ", dados)
        self.__serial.write(dados)
        self.__state = self.ocioso
        self.__buffer.clear()
    
    """ Metodo que recebe um caracter por vez da porta serial para ser tratado na maquina de estado
   
    """
    def recebe(self):
        # print("Enquadramento (recebe)")
        recvMsg = self.__serial.read(1)
        # print("[ENQ] Recebeu dado da Porta Serial: ", recvMsg)
        if self.__state(recvMsg):
            # if(self.__buffer != b''):
            print("[Enq] Frame Recebido: ", self.__buffer)
            self.__buffer.clear()    
        
    """ Metodo para deserializar um buffer e retornar um quadro
   
   @param buff: buffer
   @return Quadro: Quadro a ser retornado
    """
    def deserializeBuffer(self, buff: bytearray):
        print("[ENQ] Motando Quadro")
        tipoMsgArq = (buff[0] & (1 << 7) ) >> 7
        print("Tipo Msg: ", tipoMsgArq)
        numSequencia = (buff[0] & (1 << 3) ) >> 3
        print("numSequencia: ", numSequencia)
        idProto = buff[2]
        print("idProto: ", idProto)
        data = buff[3:len(buff)-2]
        if tipoMsgArq != 1:
            print("data: ", data)
        return Quadro(tipoMsgArq = tipoMsgArq, numSequencia = numSequencia, idProto = idProto, data = data)