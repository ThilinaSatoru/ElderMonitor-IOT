import datetime
import subprocess
import time

import RPi.GPIO as GPIO
import requests
from gpiozero import MotionSensor

# Pin Definitions:
pirPin = 4
ledPin = 17
sens = MotionSensor(pirPin)

# commands bash
stream = ['bash', './bash_stream.sh']
API_URL = 'http://127.0.0.1:8090'
last_file = ''


def api_post_image(image):
    url = API_URL + '/img'
    file = {'file': open(image, 'rb')}
    req = requests.post(url=url, files=file)
    print(req.status_code)
    print(image)


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
    global last_file
    # commands bash
    last_file = 'captures/' + str(getDateTimeNow()) + '.jpg'
    capture = ['bash', './bash_capture.sh', last_file]

    print(last_file)
    subprocess.run(capture)


def blink(led):
    GPIO.output(led, 1)  # Turn ON LED
    time.sleep(2)
    GPIO.output(led, 0)  # Turn OFF LED
    time.sleep(0.3)


def motion(led):
    global last_file
    while True:
        sens.wait_for_motion()
        print("You moved")
        blink(led)
        print(getDateTimeNow())
        take_picture()
        # POST IMAGE
        api_post_image(last_file)
        sens.wait_for_no_motion()


# device status
# capture POST
# if alone stream.
# else capture

if __name__ == '__main__':
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
