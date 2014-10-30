import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import main
import config


def get_log_contents(current=False):
    """ Emails log file from last week, or current if specified """
    year = datetime.now().strftime('%Y')
    if current:
        week = datetime.now().isocalendar()[1]
    else:
        week = datetime.now().isocalendar()[1]-1
    logfile = "logs/{y}_week-{w}.log".format(y=year, w=week)
    try:
        with open(logfile, 'r') as f:
            msg = MIMEText(f.read())
    except:
        main.log_action('Could not open log file for emailing')
        exit(0)
    return msg


class SendEmail():

    def __init__(
            self,
            subject='Surveyomatic email',
            contents='',
            sender=config.DEFAULT_FROM,
            recipient=config.DEFAULT_TO):

        msg = MIMEText(contents)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        s = smtplib.SMTP(config.SMTP_IP)
        s.sendmail(sender, recipient, msg.as_string())
        s.quit()


if __name__ == '__main__':
    current = False
    try:
        if sys.argv[1] == 'current':
            current = True
    except:
        pass
    SendEmail('Surveyomatic Weekly Log File', get_log_contents(current))
