import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from threading import Timer
import send_email
import threading
import Queue
import config


class Main():

    def __init__(self, logging_queue):
        # Keep track of config.LED state (as GPIO.input not working)
        self.ledstate = True
        self.logging_queue = logging_queue
        self.button_names = {
            config.BUTTON1: 'green',
            config.BUTTON2: 'yellow',
            config.BUTTON3: 'red'}
        self.buttons = self.button_names.keys()
        self.setup_GPIO()

    def setup_GPIO(self):
        GPIO.setwarnings(False)
        # Set's GPIO pins to BOARD GPIO numbering
        GPIO.setmode(GPIO.BOARD)
        # Setup inputs and outputs
        for button in self.buttons:
            GPIO.setup(button, GPIO.IN)
        GPIO.setup(config.LED, GPIO.OUT, initial=self.ledstate)
        # Add config.BUTTON callbacks and software debounce
        for button in self.buttons:
            GPIO.add_event_detect(
                button,
                GPIO.FALLING,
                callback=self.handle_button_press,
                bouncetime=5000)

    def handle_button_press(self, channel):
        if not self.ledstate:
            return
        self.change_led_state()
        button_name = self.button_names[channel]
        self.log_button_press(button_name)
        log_action("You pressed the {bn} button".format(bn=button_name))
        Timer(10, self.change_led_state).start()

    def change_led_state(self):
        self.ledstate = not self.ledstate
        GPIO.output(config.LED, self.ledstate)

    def log_button_press(self, button_name):
        self.logging_queue.put(button_name)


class LoggingThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def log(self, button_name):
        if config.EMAIL_EACH_PRESS:
            email_subject = 'The {bn} button was pressed!'.format(
                bn=button_name)
            send_email.SendEmail(email_subject)
        if not config.LOGGING:
            return
        logfile = "logs/{y}_week-{w}.log".format(
            y=datetime.now().strftime('%Y'),
            w=datetime.now().isocalendar()[1])
        text = "{t} | {bn}".format(
            bn=button_name,
            t=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            with open(logfile, 'a') as f:
                f.write(text + '\n')
        except Exception, e:
            log_action("Could not open log file for writing. Error: "+str(e))

    def run(self):
        while True:
            button_name = self.queue.get()
            self.log(button_name)
            self.queue.task_done()


def log_action(action):
    with open(config.PROGRAMLOG, 'a') as f:
        text = "{t} - {a}".format(
            t=datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            a=action)
        f.write(text + '\n')


if __name__ == '__main__':
    log_action("Starting up surveyomatic")

    logging_queue = Queue.Queue()
    t = LoggingThread(logging_queue)
    t.setDaemon(True)
    t.start()

    logging_queue.join()

    try:
        Main(logging_queue)
        while True:
            sleep(60)
    except:
        raise
    finally:
        GPIO.cleanup()
        log_action("Exiting surveyomatic")
