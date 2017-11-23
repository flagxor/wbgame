#! /usr/bin/env python

import serial
import sys
import time

if len(sys.argv) != 2:
  sys.stderr.write('USAGE: %s <filename>\n' % sys.argv[0])
  sys.exit(1)

data = open(sys.argv[1], 'rb').read()

ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout=1)
ser.write('\x01import os;import sys;')
ser.write('data=sys.stdin.read(%d)\n\x04' % len(data))
ser.write(data)
ser.write('with open("%s", "wb") as fh:\n  fh.write(data)\n\x04' % sys.argv[1])
ser.write('\x02')
ser.write('os.listdir()\r\n')
