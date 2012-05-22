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
    buffer = time()
    buffer_increment = 1
    while not self._halt:
      freq = 440 + 220 * (self.tmp - 15)
      print(freq)
      for i in range(1, 8000 * buffer_increment):
        audio.write(chr(int(sin(freq*i) * 50 + 128)))
      buffer += buffer_increment
      while buffer - time() > buffer_increment * 1.2:
        sleep(buffer_increment / 5)

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

