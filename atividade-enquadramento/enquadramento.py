#!/usr/bin/python3

from pypoller import poller
from socket import *
from serial import Serial


class Enquadramento(poller.Callback):
 
    def __init__(self, port, timeout):
        self.__port = port
        self.__timeout = timeout
        self.__serial = Serial(self.__port, 9600, self.__timeout)
        poller.Callback.__init__(self, self.__serial, self.__tout)
        self.__buffer = bytearray()
        
        self.enable()
        self.disable_timeout()
        sched = poller.Poller()
        self.__state = self.ocioso
        sched.adiciona(self)
        sched.despache()

      
    def ocioso(self, msg):
        if(msg == b'\x7E'):
            self.enable_timeout()
            self.__state = self.prep

    def prep(self, msg):
        if(msg == b'\x7D'):
            self.__state = self.esc
        if(msg != b'\x7E'):
            self.__buffer.append(msg)
            self.__state = self.rx

    def esc(self, msg):
        if(msg == b'\x7E' or msg == b'\x7D'):
            self.__buffer.clear()
            self.__state = self.ocioso
        else:
            self.__buffer.append(msg^0x20)
            self.__state = self.rx    

    def rx(self, msg):
        if(msg == b'\x7D'):
            self.__state = self.esc

        if(msg == b'\x7E'):
            self.__state = self.ocioso
            return True
        else:
            self.__buffer.append(msg)
        

    def handle(self):
        recvMsg = self._serial.read(1)
        if self.__state(recvMsg):
            print("Frame Msg: ", self.__buffer)

    def timeout(self):
        print('Timeout')
        self.__state = self.ocioso
        self.disable_timeout()
