import os
import subprocess as sp

def temp_monitoring(temp_alarm = 70):

    a = sp.getoutput('cat /sys/class/thermal/thermal_zone0/temp')

    temp_current = float(a)/1000

    print("current temperature of the raspberry CPU is: %.2f" % temp_current)

    if(temp_current > temp_alarm):
        
        os.system('cvlc --play-and-exit /home/nero/Desktop/monitoring_scripts/limit.mp3')
        
    return temp_current



if __name__ == "__main__":

    temp_monitoring()