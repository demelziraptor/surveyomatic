import RPi.GPIO as GPIO
from time import sleep


# Define component pins
BUTTON1 = 15
BUTTON2 = 11
BUTTON3 = 16
LED = 12
    
    
class Main():

    def __init__(self):
        setup_GPIO()

    def setup_GPIO(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)  # Set's GPIO pins to BOARD GPIO numbering
        # Set our input pins to be an input, with internal pullup resistor on
        GPIO.setup(BUTTON1, GPIO.IN)
        GPIO.setup(BUTTON2, GPIO.IN)
        GPIO.setup(BUTTON3, GPIO.IN)
        # Set our output pin to be an output
        GPIO.setup(LED, GPIO.OUT)
        GPIO.output(LED, True)        
        # Add button callbacks and software debounce to avoid triggering it multiple times a second
        GPIO.add_event_detect(BUTTON1, GPIO.FALLING, callback=B1A, bouncetime=5000) 
        GPIO.add_event_detect(BUTTON2, GPIO.FALLING, callback=B2A, bouncetime=5000)
        GPIO.add_event_detect(BUTTON3, GPIO.FALLING, callback=B3A, bouncetime=5000)
        
    def B1A(self, channel):
        print (int(GPIO.input(BUTTON1)))
        print (int(GPIO.input(BUTTON2)))
        print (int(GPIO.input(BUTTON3)))
        if ( int(GPIO.input(BUTTON2)) < 1 or int(GPIO.input(BUTTON3)) < 1 ):
            return
        else:
            GPIO.output(LED, False)
            print ('Button 1')
            sleep(0)
            GPIO.output(LED, True)
        
    def B2A(self, channel):
        print (int(GPIO.input(BUTTON1)))
        print (int(GPIO.input(BUTTON2)))
        print (int(GPIO.input(BUTTON3)))
        if ( int(GPIO.input(BUTTON1)) < 1 or int(GPIO.input(BUTTON3)) < 1 ):
            return
        else:
            GPIO.output(LED, False)
            print ('Button 2')
            sleep(0)
            GPIO.output(LED, True)
        
    def B3A(self, channel):
        print (int(GPIO.input(BUTTON1)))
        print (int(GPIO.input(BUTTON2)))
        print (int(GPIO.input(BUTTON3)))
        if ( int(GPIO.input(BUTTON1)) < 1 or int(GPIO.input(BUTTON2)) < 1 ):
            return
        else:
            GPIO.output(LED, False)
            print ('Button 3')
            sleep(0)
            GPIO.output(LED, True)


if __name__ == '__main__':
    Main()
    while True:
        sleep(60)
