import smtplib
from email.mime.text import MIMEText
from datetime import datetime

SUBJECT = 'Surveyomatic Weekly Log File'
FROM = 'pi@lucidica.com'
TO = 'demelza.buckham@lucidica.com'
LOGFILE = "{y}_week-{w}.log".format(y = datetime.now().strftime('%Y'), w = datetime.now().isocalendar()[1])

fp = open(LOGFILE, 'rb')
msg = MIMEText(fp.read())
fp.close()

msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

s = smtplib.SMTP('10.0.30.99')
s.sendmail(FROM, TO, msg.as_string())
s.quit()
