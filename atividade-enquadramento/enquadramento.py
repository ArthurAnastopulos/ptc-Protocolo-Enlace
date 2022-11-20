#!/usr/bin/python3

from pypoller import poller
from socket import *
from serial import Serial
from subcamada import Subcamada

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
            return True
        else:
            self.__buffer += msg
        

    def handle(self):
        print('handle')
        recvMsg = self.__serial.read(1)
        if self.__state(recvMsg):
            print("Frame Msg: ", self.__buffer)

    def handle_timeout(self):
        print('Timeout')
        self.__state = self.ocioso
        ##self.disable_timeout()
