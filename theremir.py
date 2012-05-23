from math import pi, sin
from subprocess import Popen, PIPE
import sys
from threading import Thread
from time import sleep, time

from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.TemperatureSensor import TemperatureSensor

class Play ( Thread ):

  def __init__(self):
    super(Play, self).__init__()
    self._halt = False
    self.tmp = 20

  def run(self):
    audio = Popen('aplay', stdin=PIPE).stdin
    buffer_increment = 1
    #freqs = [523.25,587.33,659.26,698.46,783.99,880.,987.77,1046.5]
    t = time()
    phase = 0
    while not self._halt:
      print(self.tmp)
      freq = 500 + 500 * ( 1 - ( self.tmp - 21 ) / 9 )
      now = time()
      while (t < now + 0.005):
        t = t + 1. / 8000
        phase = ( phase + ( freq * 2 * pi / 8000 ) ) % ( 2 * pi )
        audio.write( chr( int( sin( phase ) * 50 + 128 ) ) )
      sleep(.001)

  def halt(self):
    self._halt = True

play = Play()

def onChange(e):
  play.tmp = e.temperature

def initIR():
  try:
    sensor = TemperatureSensor()
    sensor.openPhidget()
    sensor.waitForAttach(2000)
    sensor.setTemperatureChangeTrigger(0, 0.1)
    sensor.setOnTemperatureChangeHandler(onChange)
    print('Temperature sensor detected.')
  except PhidgetException:
    print('No temperature sensor detected.')
  except Exception:
    print('Temperature sensor detection failed. Is the Phidgets library not installed?')

if __name__ == '__main__':
  initIR()
  play = Play()
  play.daemon = True
  play.start()
  sys.stdin.readline()
  play.halt()

