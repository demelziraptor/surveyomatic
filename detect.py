import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


# Define component pins
BUTTON1 = 15
BUTTON2 = 11
BUTTON3 = 16
LED = 12

# Logging control
LOGGING = True
    
    
class Main():

    def __init__(self):
        self.buttons = [BUTTON1, BUTTON2, BUTTON3]
        self.button_names = {BUTTON1: 'green', BUTTON2: 'yellow', BUTTON3: 'red'}
        setup_GPIO()

    def setup_GPIO(self):
        GPIO.cleanup()
        # Set's GPIO pins to BOARD GPIO numbering
        GPIO.setmode(GPIO.BOARD)
        # Setup inputs and outputs
        for button in self.buttons:
            GPIO.setup(button, GPIO.IN)
        GPIO.setup(LED, GPIO.OUT)
        # Set initial LED state
        GPIO.output(LED, True)        
        # Add button callbacks and software debounce to avoid triggering it multiple times a second
        for button in self.buttons:
            GPIO.add_event_detect(button, GPIO.FALLING, callback=self.handle_button_press, bouncetime=5000)
        
    def handle_button_press(self, channel):
        self.print_button_states()
        if not GPIO.input(LED):
            return
        GPIO.output(LED, False)
        button_name = self.button_names[channel]
        self.log_button_press(button_name)
        print "You pressed the {bn} button".format(bn = button_name)
        sleep(10)
        GPIO.output(LED, True)
         
    def print_button_states(self):
        for button in self.buttons:
            print int(GPIO.input(button))
            
    def log_button_press(self, button_name):
        if not LOGGING:
            return
        logfile = "{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1])
        text = "The {bn} button was pressed at {t}".format(bn = button_name, t = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            with open(logfile, 'a') as f:
                f.write(text + '\n')
        except:
            print "Could not open log file for writing"


if __name__ == '__main__':
    try:
        Main()
        while True:
            sleep(60)
    except:
        pass
    finally:
        GPIO.cleanup()
