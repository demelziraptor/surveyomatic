import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from main import log_action
import config


def get_log_contents():
    logfile = "logs/{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1]-1)
    try:
        with open(logfile, 'r') as f:
            msg = MIMEText(f.read())
    except:
        log_action('Could not open log file for emailing')
        exit(0)
    return msg
    

class SendEmail():

    def __init__(self, subject='Surveyomatic email',contents='',sender=config.DEFAULT_FROM,recipient=config.DEFAULT_TO):
        
        msg = MIMEText(contents)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        s = smtplib.SMTP('10.0.30.99')
        s.sendmail(sender, recipient, msg.as_string())
        s.quit()


if __name__ == '__main__':
    SendEmail('Surveyomatic Weekly Log File',get_log_contents())
