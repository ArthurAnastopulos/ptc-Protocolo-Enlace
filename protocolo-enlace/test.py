import sys
from protocolo import Protocolo


try:
  porta = sys.argv[1]
  print("Obteve a porta: " +porta)
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

timeout = 10

proto = Protocolo(serial= porta, tout= timeout)

proto.iniciar()