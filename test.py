import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import subprocess
import time
import datetime

# Pin Definitions:
pirPin = 4
ledPin = 17
sens = MotionSensor(pirPin)

# commands bash
stream = ['bash', './stream.sh']


def setup():
    print("Hello Raspberry")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

    GPIO.setup(ledPin, GPIO.OUT)  # output rf
    GPIO.setup(pirPin, GPIO.IN)

    # Initial state for LEDs:
    print("Testing RF out, Press CTRL+C to exit")


def getDateTimeNow():
    return datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")


def take_picture():
    # commands bash
    arg1 = 'captures/' + str(getDateTimeNow()) + '.jpg'
    capture = ['bash', './capture.sh', arg1]

    print(arg1)
    subprocess.run(capture)


def blink(led):
    GPIO.output(led, 1)  # Turn ON LED
    time.sleep(2)
    GPIO.output(led, 0)  # Turn OFF LED
    time.sleep(0.3)


def motion(led):
    while True:
        sens.wait_for_motion()
        print("You moved")
        blink(led)
        print(getDateTimeNow())
        take_picture()
        # POST
        sens.wait_for_no_motion()


# device status
# capture POST
# if alone stream.
# else capture


try:
    setup()
    motion(ledPin)

except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print("Keyboard interrupt")

except Exception as e:
    print("some error : " + str(e))

finally:
    print("clean up")
    GPIO.cleanup()  # cleanup all GPIO
