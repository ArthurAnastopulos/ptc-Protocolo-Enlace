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

frame = enquadramento.Enquadramento(porta,10)


sys.exit(0)