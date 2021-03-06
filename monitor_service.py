import os
import subprocess
from datetime import datetime
import send_email
from main import log_action
import config
    

def check_process_ok():        
    """ Check pid file and running process """
    if not os.path.isfile(config.PIDFILE):
        return True 
    with open(config.PIDFILE, 'r') as f:
        pid = f.read()
    try:
        os.kill(int(pid.rstrip()), 0)
    except OSError:
        return False
    else:
        return True
        
def should_restart():
    times = 0
    date_format = '%d/%m/%Y'
    if os.path.isfile(config.RESTARTLOG):
        with open(config.RESTARTLOG, 'r') as f:
            status = f.readline()
            if status.split()[0] == datetime.now().strftime(date_format):
                # last restart was today,
                times = int(status.split()[1])
                if times == 3:
                    # restarted 3 times today already, exit
                    log_action('Already restarted 3 times today, exiting')
                    send_email.SendEmail('Surveyomatic has been restarted 3 times already today, it will not be restarted again')
                    return False
    with open(config.RESTARTLOG, 'w') as f:
        times += 1
        text = "{d} {t}".format(d = datetime.now().strftime(date_format), t = str(times))
        f.write(text + '\n')
    return True
        
def restart_process():
    log_action('Found PID file but no process, attempting to restart')
    ret = subprocess.call('service surveyomatic restart', shell=True)
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


if __name__ == "__main__":
    main()

