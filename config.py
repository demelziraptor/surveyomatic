# Define component pins
BUTTON1 = 15
BUTTON2 = 11
BUTTON3 = 16
LED = 12

# Logging
LOGGING = True

# Emailing
EMAIL_EACH_PRESS = True
DEFAULT_FROM = 'pi@lucidica.com'
DEFAULT_TO = 'demelza.buckham@lucidica.com'

# Program settings
# (any changes must also be made to sysvinit and logrotate scripts)
PIDFILE = '/var/run/surveyomatic.pid'
PROGRAMLOG = '/var/log/surveyomatic.log'
RESTARTLOG = '/home/pi/demelziraptor/surveyomatic/restartcount.log'
