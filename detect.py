from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
 
GPIO.setmode(GPIO.BOARD)  # Set's GPIO pins to BOARD GPIO numbering
# Define component pins
BUTTON1 = 15
BUTTON2 = 11
BUTTON3 = 16
LED = 12
# Set our input pins to be an input, with internal pullup resistor on
GPIO.setup(BUTTON1, GPIO.IN)
GPIO.setup(BUTTON2, GPIO.IN)
GPIO.setup(BUTTON3, GPIO.IN)
# Set our output pin to be an output
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, True)

# Create functions to run when the buttons are pressed
def B1A(channel):
    GPIO.output(LED, False);
    print ('Button 1');
    sleep(0);
    GPIO.output(LED, True);
    
def B2A(channel):
    GPIO.output(LED, False);
    print ('Button 2');
    sleep(0);
    GPIO.output(LED, True);
    
def B3A(channel):
    GPIO.output(LED, False);
    print ('Button 3');
    sleep(0);
    GPIO.output(LED, True);

# Wait for Button 1 to be pressed, run the function in "callback" when it does, also software debounce for 300 ms to avoid triggering it multiple times a second
GPIO.add_event_detect(BUTTON1, GPIO.FALLING, callback=B1A, bouncetime=500) 
GPIO.add_event_detect(BUTTON2, GPIO.FALLING, callback=B2A, bouncetime=500)
GPIO.add_event_detect(BUTTON3, GPIO.FALLING, callback=B3A, bouncetime=500)

# Start a loop that never ends
while True:
    # Put anything you want to loop normally in here
    sleep(60);           # Sleep for a full minute, any interrupt will break this so we are just saving cpu cycles.
