import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)
if GPIO.input(11):
    print('Input was HIGH')
else:
    print('Input was LOW')
GPIO.add_event_detect(11, GPIO.BOTH)
def my_callback():
    GPIO.output(12, GPIO.input(11))
    print('Hello')
GPIO.add_event_callback(11, my_callback)
