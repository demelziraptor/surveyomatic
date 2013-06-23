import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)
GPIO.add_event_detect(11, GPIO.BOTH)
def my_callback():
    GPIO.output(12, GPIO.input(11))
GPIO.add_event_callback(11, my_callback)
GPIO.cleanup()
