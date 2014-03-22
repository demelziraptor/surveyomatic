import os
import subprocess
from datetime import datetime

PIDFILE = '/var/run/surveyomatic.pid'
LOGFILE = '/var/log/surveyomatic.log'
RESTARTLOG = '/home/pi/demelziraptor/surveyomatic/restartcount.log
    

def check_process_ok():        
    """ Check pid file and running process """
    if not os.path.isfile(fname):
        return True 
    with open(PIDFILE, 'r') as f:
        pid = f.read()
    try:
        os.kill(int(pid.rstrip()), 0)
    except OSError:
        return False
    else:
        return True
        
def should_restart():
    times = 0
    with open(RESTARTLOG, 'w+') as f:
        status = f.readline()
        if status.split()[0] == datetime.now().strftime('%m%d'):
            # last restart was today, 
            times = int(status.split()[1])
            if times == 3:
                # restarted 3 times today already, exit
                log_action('Already restarted 3 times today, exiting')
                return False
        times =+ 1
        text = "{d} {t}".format(d = datetime.now().strftime('%m%d'), t = str(times))
        f.write(text + '\n')
    return True 

def log_action(action):
    with open(LOGFILE, 'a') as f:
        text = "{t} - {a}".format(t = datetime.now().strftime('%Y/%m/%d %H:%M:%S'), a = action)
        f.write(text + '\n')
        
def log_restart():
    times = 0
    with open(RESTARTLOG, 'a+') as f:
        status = f.readline()
        if status.split()[0] == datetime.now().strftime('%m%d'):
            times = int(status.split()[1])
            if times == 3:
                # restarted 3 times today already, exit
                log_action('Already restarted 3 times today, exiting')
                exit(0)
            times =+ 1
        text = "{d} {t}".format(d = datetime.now().strftime('%m%d'), t = str(times))
        f.write(text + '\n')
     
def restart_process():
    log_action('Found PID file but no process, attempting to restart')
    log_restart()
    ret = subprocess.call('service surveyomatic restart', shell=False)
    if ret == 0:
        log_action('Restart was successful')
        return True
    log_action('Restart was unsuccessful')
    return False
    
              
def main():
    # check process is ok, exit if it is
    if check_process_ok():
        exit(0)
    # process not ok, check how many times restarted today
    if not should_restart():
        exit(0)
    # not reached restart limit, restart
    if restart_process():
        exit(0)
    # could do something here; send email etc    


if __name__ == "__main__":
    main()
    exit(0)

