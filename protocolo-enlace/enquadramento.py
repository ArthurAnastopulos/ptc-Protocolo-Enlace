#!/usr/bin/python3

from pypoller import poller
from socket import *
from serial import Serial
from subcamada import Subcamada
from quadro import Quadro
from crc import CRC16
## class Enquadramento(poller.Callback):
class Enquadramento(Subcamada): 

    def __init__(self, port, tout):
        print('__init__')
        self.__port = port
        self.__tout = tout
        self.__serial = Serial(self.__port, 9600, timeout=None )
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
        print("ocioso: ", msg)
        if(msg == b'\x7E'):
            ##self.enable_timeout()
            self.__state = self.prep

    def prep(self, msg):
        print("prep:", msg)
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg != b'\x7E'):
            self.__buffer += msg
            self.__state = self.rx

    def esc(self, msg):
        print('esc:', msg)
        if(msg == b'\x7E' or msg == b'\x7D'):
            self.__buffer.clear()
            self.__state = self.ocioso
            ##self.disable_timeout()
        else:
            self.__buffer += bytes([msg[0] ^ 0x20])
            self.__state = self.rx    

    def rx(self, msg):
        print('rx:', msg)
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg == b'\x7E'):
            self.__state = self.ocioso
            ##self.disable_timeout() 
            fcs = CRC16(self.__buffer)
            if fcs.check_crc():
                quadro = self.deserializeBuffer(self.__buffer)
                self.superior.recebe(quadro) #recebe da Subcamada, não do enquadramento (Talvez mudar de nome, para não gerar confusão?)
                self.__buffer.clear()       
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
        dados = bytearray()
        dados.append( b'\x7E' )
        dados += quadro.serialize()
        dados.appen( b'\x7E' )
        self.__serial.write(dados) 
    
    def recebe(self):
        recvMsg = self.__serial.read(1)
        if self.__state(recvMsg):
            print("Frame Msg: ", self.__buffer)
        
    def deserializeBuffer(self, buff: bytearray):
        tipoQuadro = (buff[0] & (1 << 7) ) >> 7
        numSequencia = (buff[0] & (1 << 3) ) >> 3
        if tipoQuadro == 0: #Se for 0, é Data
            idProto = buff[2]
            data = buff[3:len(buff)-2]
            return Quadro(tipoQuadro = tipoQuadro, numSequencia = numSequencia, idProto = idProto, data = data)
            #fcs é preparado no serialize do Quadro, assim não é necessario aqui
        else: # Se for 1, é ACK
            data[2:len(buff)-2]
            return Quadro(tipoQuadro = tipoQuadro, numSequencia = numSequencia, data = data)
           
