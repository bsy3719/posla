# objectification
# 2018.10.12
# BCODE
import RPi.GPIO as gpio
import time

class UltraSonic(object) :
    def __init__(self) :
        gpio.setmode(gpio.BCM)
        self.trig = 17
        self.echo = 27

        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

    def run(self, server) :
        while(True):
            gpio.output(self.trig, False)
            time.sleep(0.1)

            gpio.output(self.trig, True)
            time.sleep(0.00001)
            gpio.output(self.trig, False)

            while gpio.input(self.echo) == 0:
                pulse_start = time.time()

            while gpio.input(self.echo) == 1:
                pulse_end = time.time()

            distance = round((pulse_end - pulse_start) * 17000, 2)
              
            server.Send_Data(str(int(distance)).encode())

    def __del__(self) :
        gpio.cleanup()
