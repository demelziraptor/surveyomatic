surveyomatic
============

RPi Project.  Uses RPi.GPIO to control GPIO device.


Installation
------------
### Set up the service ###
- Set up correct permissions on the sysvinit file  
  `chmod 755 /path/to/surveyomatic-sysvinit`
- Symlink the sysvinit file (surveyomatic) to /etc/init.d  
  `sudo ln -s /path/to/surveyomatic-sysvinit /etc/init.d/surveyomatic`
- Modify the path to main.py in the sysvinit file if it needs changing
- Add sysvinit file to startup scripts  
   `sudo update-rc.d surveyomatic defaults`

### Set up emailing ###
- Add a cron job to run the send_email.py script as often as you like (default weekly)  
  `crontab -l > file; echo '02 00 * * 1 python /path/to/send_email.py >/dev/null 2>&1' >> file; crontab file`
- If not running weekly, need to change two files in addition to the cron schedule:
    1. main.py; logfile variable under def log
    2. send_email.py; LOGFILE variable  
  For example, if running daily, (1) should be changed to:  
    `logfile = "logs/{t}.log".format(t = datetime.now().strftime('%Y-%m-%d'))`  
  And (2) changed to:  
    `LOGFILE = "logs/{t}-{d}.log".format(t = datetime.now().strftime('%Y-%m'), d = int(datetime.now().strftime('%d'))-1)`
  And cron time schedule changed from 02 00 * * 1 to:  
    `02 0 * * *`
    
### Set up service monitoring ###
- Add a cron job to run the monitor script as often as you like, eg for every 5 minutes:  
  `echo "*/5 * * * * root python /path/to/monitor_service.py" >> /etc/crontab`  
(This is different to the cron line above as it needs to run as root rather than a normal user account)

### Set up service log rotation ###
- Symlink the logrotate config script into /etc/logrotate.d  
  `sudo ln -s /path/to/surveyomatic-logrotate /etc/logrotate.d/surveyomatic.log`


Usage
-----
sudo service surveyomatic start  
sudo service surveyomatic stop

