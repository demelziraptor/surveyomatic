import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from threading import Timer
from send_email import SendEmail
import threading
import Queue

# Define component pins
BUTTON1 = 15
BUTTON2 = 11
BUTTON3 = 16
LED = 12

# Logging control
LOGGING = True


class Main():

    def __init__(self, logging_queue):
        # Keep track of LED state (as GPIO.input not working)
        self.ledstate = True
        self.logging_queue = logging_queue
        self.buttons = [BUTTON1, BUTTON2, BUTTON3]
        self.button_names = {BUTTON1: 'green', BUTTON2: 'yellow', BUTTON3: 'red'}
        self.setup_GPIO()

    def setup_GPIO(self):
        GPIO.setwarnings(False)
        # Set's GPIO pins to BOARD GPIO numbering
        GPIO.setmode(GPIO.BOARD)
        # Setup inputs and outputs
        for button in self.buttons:
            GPIO.setup(button, GPIO.IN)
        GPIO.setup(LED, GPIO.OUT, initial=self.ledstate)
        # Add button callbacks and software debounce to avoid triggering it multiple times a second
        for button in self.buttons:
            GPIO.add_event_detect(button, GPIO.FALLING, callback=self.handle_button_press, bouncetime=5000)
        
    def handle_button_press(self, channel):
        if not self.ledstate:
            print 'light is on already, skipping button press'
            return
        print 'light is off, registering button press'
        self.change_LED_state()
        button_name = self.button_names[channel]
        self.log_button_press(button_name)
        print "You pressed the {bn} button".format(bn = button_name)
        Timer(10, self.change_LED_state).start()
         
    def change_LED_state(self):
        self.ledstate = not self.ledstate
        GPIO.output(LED, self.ledstate)

    def print_button_states(self):
        for button in self.buttons:
            print int(GPIO.input(button))
            
    def log_button_press(self, button_name):
        if not LOGGING:
            return
        self.logging_queue.put(button_name)
            
            

class LoggingThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def log(self, button_name):
        email_subject = 'The {bn} button was pressed!'.format(bn = button_name)
        SendEmail(email_subject)
        logfile = "logs/{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1])
        text = "{t} | {bn}".format(bn = button_name, t = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print "logfile is:", logfile
        try:
            with open(logfile, 'a') as f:
                f.write(text + '\n')
        except Exception, e:
            t = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print t, "Could not open log file for writing. Error:", str(e)
    
    def run(self):
        while True:
            button_name = self.queue.get()
            self.log(button_name)
            self.queue.task_done()



if __name__ == '__main__':
    print 'starting'
    logging_queue = Queue.Queue()

    # spawn threads for logging
    t = LoggingThread(logging_queue)
    t.setDaemon(True)
    t.start()

    # wait for queue to get empty
    logging_queue.join()
     
    try:
        Main(logging_queue)
        while True:
            sleep(60)
    except:
        raise
    finally:
        GPIO.cleanup()
