#import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from threading import Timer
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

    import RPi.GPIO as GPIO

    def __init__(self, logging_queue):
        # Keep track of LED state (as GPIO.input not working)
        self.ledstate = True
        self.logging_queue = logging_queue
        self.buttons = [BUTTON1, BUTTON2, BUTTON3]
        self.button_names = {BUTTON1: 'green', BUTTON2: 'yellow', BUTTON3: 'red'}
        self.setup_GPIO()

    def setup_GPIO(self):
        GPIO.cleanup()
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
        logfile = "{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1])
        text = "The {bn} button was pressed at {t}".format(bn = button_name, t = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            with open(logfile, 'a') as f:
                f.write(text + '\n')
        except:
            print "Could not open log file for writing"
    
    def run(self):
        while True:
            button_name = self.queue.get()
            self.log(button_name)
            self.queue.task_done()

class ProcessThread(threading.Thread):
    def __init__(self, processing_queue, logging_queue):
        threading.Thread.__init__(self)
        self.processing_queue = processing_queue
        self.logging_queue = logging_queue

    def run(self):
        while True:
            Main(self.logging_queue)
            self.processing_queue.task_done()

processingqueue = Queue.Queue()
loggingqueue = Queue.Queue()


# spawn thread for main program
t = ProcessThread(processingqueue, loggingqueue)
t.setDaemon(True)
t.start()

# spawn threads for logging
t = LoggingThread(loggingqueue)
t.setDaemon(True)
t.start()

# wait for queue to get empty
processingqueue.join()
loggingqueue.join()
