import machine
import math
import time
import urandom
import wifiboy

WIDTH = 120
HEIGHT = 160
pin0 = machine.Pin(0)
pin5 = machine.Pin(5)
pina0 = machine.ADC(0)
pwm = machine.PWM(machine.Pin(4))

def boxes():
  wifiboy.cls()
  for i in range(100):
    wifiboy.box(
        urandom.getrandbits(8) * WIDTH // 255,
        urandom.getrandbits(8) * HEIGHT // 255,
        urandom.getrandbits(8) * WIDTH // 255,
        urandom.getrandbits(8) * HEIGHT // 255,
        urandom.getrandbits(15))

def lines():
  wifiboy.cls()
  for i in range(100):
    wifiboy.line(
        urandom.getrandbits(8) * WIDTH // 255,
        urandom.getrandbits(8) * HEIGHT // 255,
        urandom.getrandbits(8) * WIDTH // 255,
        urandom.getrandbits(8) * HEIGHT // 255,
        urandom.getrandbits(15))

def keys():
  val = pina0.read()
  if val < 32:
    ret = 4
  elif val < 512:
    ret = 8
  else:
    ret = 0
  if not pin0.value():
    ret += 2
  if not pin5.value():
    ret += 1
  return ret

def testkeys():
  while True:
    print(keys())

def sounds():
  pwm.duty(200)
  for i in range(20):
    pwm.freq(int(220 * math.pow(2, i / 12)))
    time.sleep(0.1)
  pwm.duty(0)

def drawing():
  x = WIDTH // 2
  y = HEIGHT // 2
  while True:
    k = keys()
    if k & 1:
      x += 1
    if k & 8:
      x -= 1
    if k & 4:
      y += 1 
    if k & 2:
      y -= 2
    time.sleep(0.01)
    for i in range(8):
      wifiboy.line(
          60 - x + i, 80 - y, 60 - x + i, 100 - y, i)
    wifiboy.box(x - 3, y - 3, 7, 7, 0x0000)
    wifiboy.box(x - 2, y - 2, 5, 5, 0x7fff)
    if y < 130:
     y += 1
