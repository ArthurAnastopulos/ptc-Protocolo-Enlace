# protocol poller instancia aqui
from subcamada import Subcamada
from enquadramento import Enquadramento
from pypoller import poller

class Protocolo(poller.Callback):
    def __init__(self):
        Subcamada.__init__()

    def envio(self):
        print("envio")

    def recebe(self):
        print("notifica//recebe")

    def handle(self):
        print("handle")
    