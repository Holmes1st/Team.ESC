import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.HIGH)

def beep(i):
    GPIO.output(25, GPIO.LOW)
    time.sleep(i)

    GPIO.output(25, GPIO.HIGH)

def success():
            print "Buzz_Success"
            beep(0.1)
            time.sleep(0.02)
            beep(0.15)

def fail():
            print "Buzz_Fail"
            beep(0.5)
            
def init():
    print "Buzz init"
    GPIO.output(25, GPIO.HIGH)


argv = int(sys.argv[1])

if argv == 1:
    success()
elif argv == 2:
    fail()
elif argv == 0:
    init()

GPIO.cleanup()

