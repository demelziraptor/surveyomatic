import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.add_event_detect(17, GPIO.BOTH)
def my_callback():
    GPIO.output(18, GPIO.input(17))
GPIO.add_event_callback(17, my_callback)
