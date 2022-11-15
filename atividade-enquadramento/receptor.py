#!/usr/bin/python3

from serial import Serial
import enquadramento
import sys

try:
  porta = sys.argv[1]
  print("Obteve a porta: " +porta)
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

try:
  p = Serial(porta, 9600, timeout=10)
except Exception as e:
  print('Não conseguiu acessar a porta serial', e)
  sys.exit(0)

# recebe até 128 caracteres
msg = p.read(128)
print('Recebeu: ', msg)

FRAME = enquadramento.Enquadramento(porta,10)
FRAME.ocioso(msg)


sys.exit(0)