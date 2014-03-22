import smtplib
from email.mime.text import MIMEText
from datetime import datetime

PROGRAMLOG = '/var/log/surveyomatic.log'

SUBJECT = 'Surveyomatic Weekly Log File'
FROM = 'pi@lucidica.com'
TO = 'demelza.buckham@lucidica.com'
LOGFILE = "logs/{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1]-1)

try:
    with open(LOGFILE, 'r') as f:
        msg = MIMEText(f.read())
except:
    with open(PROGRAMLOG, 'a') as f:
        f.write('Could not open log file for emailing' + '\n')
    exit(0)

msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

s = smtplib.SMTP('10.0.30.99')
s.sendmail(FROM, TO, msg.as_string())
s.quit()

exit(0)
