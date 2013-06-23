from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
 
GPIO.setmode(GPIO.BOARD)  # Set's GPIO pins to BCM GPIO numbering
BUTTON_1 = 15           # Sets our input pins
BUTTON_2 = 16           # Sets our input pins
BUTTON_3 = 11           # Sets our input pins
LED = 12
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set our input pin to be an input, with internal pullup resistor on
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set our input pin to be an input, with internal pullup resistor on
GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set our input pin to be an input, with internal pullup resistor on
GPIO.setup(LED, GPIO.OUT)

# Create functions to run when the buttons are pressed
def Input_1(channel):
    GPIO.output(LED, True);
    sleep(2);
    GPIO.output(LED, False);
    
def Input_2(channel):
    GPIO.output(LED, True);
    sleep(2);
    GPIO.output(LED, False);
    
def Input_3(channel):
    GPIO.output(LED, True);
    sleep(2);
    GPIO.output(LED, False);

# Wait for Button 1 to be pressed, run the function in "callback" when it does, also software debounce for 300 ms to avoid triggering it multiple times a second
GPIO.add_event_detect(BUTTON_1, GPIO.BOTH, callback=Input_1, bouncetime=300) 
GPIO.add_event_detect(BUTTON_2, GPIO.BOTH, callback=Input_2, bouncetime=300) # Wait for Button 2 to be pressed
GPIO.add_event_detect(BUTTON_3, GPIO.BOTH, callback=Input_3, bouncetime=300) # Wait for Button 3 to be pressed

# Start a loop that never ends
while True:
    # Put anything you want to loop normally in here
    sleep(60);           # Sleep for a full minute, any interrupt will break this so we are just saving cpu cycles.
