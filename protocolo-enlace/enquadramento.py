#!/usr/bin/python3

from serial import Serial
from subcamada import Subcamada
from quadro import Quadro
from crc import CRC16
import sys

## class Enquadramento(poller.Callback):
class Enquadramento(Subcamada): 

    def __init__(self, port, tout):
        print("Enquadramento (__init__)")
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
        
        ##self.enable()
        ##self.disable_timeout()
        ##sched = poller.Poller()
        self.__state = self.ocioso
        ##sched.adiciona(self)
        ##sched.despache()

      
    def ocioso(self, msg):
        print("Enquadramento (ocioso): ", msg)
        if(msg == b'\x7E'):
            ##self.enable_timeout()
            self.__state = self.prep

    def prep(self, msg):
        print("Enquadramento (prep): ", msg)
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg != b'\x7E'):
            self.__buffer += msg
            self.__state = self.rx

    def esc(self, msg):
        print('Enquadramento (esc):', msg)
        if(msg == b'\x7E' or msg == b'\x7D'):
            self.__buffer.clear()
            self.__state = self.ocioso
            ##self.disable_timeout()
        else:
            self.__buffer += bytes([msg[0] ^ 0x20])
            self.__state = self.rx    

    def rx(self, msg):
        print('Enquadramento (rx): ', msg)
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg == b'\x7E'):
            self.__state = self.ocioso
            ##self.disable_timeout() 
            fcs = CRC16(self.__buffer)
            if fcs.check_crc():
                quadro = self.deserializeBuffer(self.__buffer)
                print("Quadro: ", quadro, "  buffer: ", self.__buffer)
                self.superior.recebe(quadro) #recebe da Subcamada, não do enquadramento (Talvez mudar de nome, para não gerar confusão?)   
                return True
            return False    
        else:
            self.__buffer += msg
        

    def handle(self):
        print('handle(Enquadramento)')
        self.recebe()

    def handle_timeout(self):
        print('handle_timeout(Enquadramento)')
        self.__state = self.ocioso
        self.__buffer.clear()
        ##self.disable_timeout()
    
    def envia(self,quadro):
        print("Enquadramento (envia)")
        dados = bytearray()
        dados += b'\x7E'
        dados += quadro.serialize()
        dados += b'\x7E'
        print("Enq Envia Dados: ", dados)
        self.__serial.write(dados)
        self.__buffer.clear()
    
    def recebe(self):
        print("Enquadramento (recebe)")
        recvMsg = self.__serial.read(1)
        if self.__state(recvMsg):
            print("Frame Msg: ", self.__buffer)
            self.__buffer.clear()    
        
    def deserializeBuffer(self, buff: bytearray):
        print("Enquadramento (deserializeBuffer)")
        tipoMsgArq = (buff[0] & (1 << 7) ) >> 7
        numSequencia = (buff[0] & (1 << 3) ) >> 3
        idProto = buff[2]
        data = buff[3:len(buff)-2]
        return Quadro(tipoMsgArq = tipoMsgArq, numSequencia = numSequencia, idProto = idProto, data = data)