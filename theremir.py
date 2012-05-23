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
    t = time()
    phase = 0
    while not self._halt:
      freq = 500 + 500 * ( 1 - ( self.tmp - 21 ) / 9 )
      now = time()
      while (t < now + 0.005):
        t = t + 1. / 8000
        phase = ( phase + ( freq * 2 * pi / 8000 ) ) % ( 2 * pi )
        audio.write( chr( int( sin( phase ) * 50 + 128 ) ) )
      sleep(.001)

  def stop(self):
    self._halt = True

class Theremir:

  def __init__(self):
    self.play = None
    self.sensor = None

  def start(self):
    self.play = Play()
    self.play.start()
    self.initIR()

  def stop(self):
    self.play.stop()
    if self.sensor: self.sensor.closePhidget()

  def onChange(self, e):
    self.play.tmp = e.temperature

  def initIR(self):
    try:
      sensor = TemperatureSensor()
      sensor.openPhidget()
      sensor.waitForAttach(2000)
      sensor.setTemperatureChangeTrigger(0, 0.1)
      sensor.setOnTemperatureChangeHandler(self.onChange)
      print('Temperature sensor detected.')
    except PhidgetException:
      print('No temperature sensor detected.')
    except Exception:
      print('Temperature sensor detection failed. Is the Phidgets library not installed?')
    self.sensor = sensor

if __name__ == '__main__':
  t = Theremir()
  t.start()
  sys.stdin.readline()
  t.stop()

