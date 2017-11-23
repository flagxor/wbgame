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

def rgb(col):
  return ((col & 0xe) << 9) + ((col & 0xe0) >> 5) + ((col & 0xe00) >> 4)

grass = rgb(0xad9)

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

def sounds():
  pwm.duty(200)
  for i in range(20):
    pwm.freq(int(220 * math.pow(2, i / 12)))
    time.sleep(0.05)
  pwm.duty(0)

def player():
  r = 0
  room(r)
  x = WIDTH // 2
  y = HEIGHT * 2 // 3
  while True:
    k = keys()
    if k & 1:
      x += 1
    if k & 8:
      x -= 1
    if k & 4:
      y += 1 
    if k & 2:
      y -= 1
    if (k & 1) and (k & 2):
      sounds()
      room(r)
    time.sleep(0.02)
    if x > 115:
      x = 5
      r = 1 - r
      room(r)
    if x < 5:
      x = 115
      r = 1 - r
      room(r)
    wifiboy.box(x - 3, y - 3, 7, 7, grass)
    wifiboy.box(x - 2, y - 2, 5, 5, rgb(0xfff))
    wifiboy.box(x - 2, y - 2, 2, 2, rgb(0x007))
    wifiboy.box(x + 1, y - 2, 2, 2, rgb(0x007))
    wifiboy.box(x, y + 1, 2, 2, rgb(0xf00))

def sign(x, y):
  wifiboy.box(x - 3, y - 20, 7, 20, rgb(0xc92))
  wifiboy.box(x - 15, y - 30, 30, 20, rgb(0xea2))

def house(x, y):
  wifiboy.box(x - 40, y - 30, 80, 30, rgb(0x52a))
  wifiboy.box(x - 8, y - 16, 16, 16, rgb(0x000))
  wifiboy.box(x - 40, y - 70, 80, 40, rgb(0xa8e))
  wifiboy.line(x - 40, y - 30, x + 10, y - 50, rgb(0x000))
  wifiboy.line(x - 40, y - 70, x + 10, y - 50, rgb(0x000))
  wifiboy.line(x + 40, y - 30, x + 10, y - 50, rgb(0x000))
  wifiboy.line(x + 40, y - 70, x + 10, y - 50, rgb(0x000))

def room(r):
  if r == 0:
    wifiboy.cls()
    wifiboy.box(0, 0, WIDTH, HEIGHT, grass)
    house(40, 80)
    sign(90, 150)
  elif r == 1:
    wifiboy.cls()
    wifiboy.box(0, 0, WIDTH, HEIGHT, grass)
    sign(60, 90)

def game():
  player()
