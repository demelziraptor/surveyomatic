import smtplib
from email.mime.text import MIMEText
from datetime import datetime


PROGRAMLOG = '/var/log/surveyomatic.log'

FROM = 'pi@lucidica.com'
TO = 'demelza.buckham@lucidica.com'
LOGFILE = "logs/{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1]-1)


def get_log_contents():
    try:
        with open(LOGFILE, 'r') as f:
            msg = MIMEText(f.read())
    except:
        with open(PROGRAMLOG, 'a') as f:
            f.write('Could not open log file for emailing' + '\n')
        exit(0)
    return msg
    

class SendEmail():

    def __init__(self, subject='Surveyomatic email',contents='',sender=FROM,recipient=TO):
        
        msg = MIMEText(contents)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        s = smtplib.SMTP('10.0.30.99')
        print str(msg)
        exit(0)
        s.sendmail(sender, to, msg.as_string())
        s.quit()


if __name__ == '__main__':
    SendEmail('Surveyomatic Weekly Log File',get_log_contents())
