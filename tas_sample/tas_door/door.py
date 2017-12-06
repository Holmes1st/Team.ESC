import RPi.GPIO as GPIO
import time
import sys

pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
cnt = 0

def On():
    p.ChangeDutyCycle(7)
    print "Door Open"
    time.sleep(1)

def off():
    p.ChangeDutyCycle(2.5)
    print "Door Closed"
    time.sleep(1)

def init():
    p.ChangeDutyCycle(2.5)
    print "Door Check"
    time.sleep(1)
    


argv = int(sys.argv[1])

if argv == 1:
    On()
elif argv == 2:
    off()
elif argv == 0:
    init()

GPIO.cleanup()
