import RPi.GPIO as GPIO
from time import sleep


# Define component pins
BUTTON1 = 15
BUTTON2 = 11
BUTTON3 = 16
LED = 12
    
    
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
        print_button_states()
        if not GPIO.input(LED):
            return
        GPIO.output(LED, False) 
        print "You pressed the {colour} button".format(colour = self.button_names[channel])
        sleep(10)
        GPIO.output(LED, True)
         
    def print_button_states(self):
        for button in self.buttons:
            print int(GPIO.input(button))


if __name__ == '__main__':
    Main()
    while True:
        sleep(60)
