#https://www.raspberrypi.org/forums/viewtopic.php?f=144&t=301414

#!/usr/bin/env python3
import time
from threading import Timer
import os
import serial
import csv
from datetime import datetime


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True


class PicoCom:
    """
    Simple serial communication with a PICO. You can read or write a message. Read returns
    None if there is no message. Poll communicates at regular intervals and returns the received message.
    The latest data is stored in self.pico_data. You probably want your parse_fn to write this to file.

    Vars:
    COM_port : The allocated com port by your computer to the virtual serial port of the PICO
    log_filename: filename to write data for, used in poll.
    msg      : String to be sent to the PICO
    newline  : Terminating character to indicate new line, default \n
    parse_fn : A function to determine how the read string will be formatted
    count    : Number of times to contact the PICO for a message. None = continuous
    interval : Time between contacting PICO in seconds
    pico_data: Latest data returned from the PICO
    

    """
    def __init__(self, COM_port='COM3', log_filename='data.csv', log=True):
        self.ser = serial.Serial(COM_port, 115200)
        self.log_filename=log_filename
        self.log=log
        self.now=datetime.now()
        time.sleep(1)

    def write(self, msg, newline='\n'):
        msg=msg+newline
        self.ser.write(bytes(msg.encode('ascii')))

    def read(self, parse_fn=None):
        if self.ser.inWaiting() > 0:
            self.pico_data = self.ser.readline()
            self.ser.flushInput()
            self.ser.flushOutput()
            self.pico_data = self.pico_data.decode("utf-8","ignore")
            if parse_fn is not None:
                self.pico_data = parse_fn(self.pico_data)
        else:
            self.pico_data = 'None'
        if self.log:
            self._logdata()
        
        return self.pico_data

    def poll(self, interval=2, parse_fn=None):
        #Repeatedly polls the pico for data at the specified interval in seconds
        self.parse_fn = parse_fn
        self.timer = RepeatedTimer(interval, self._func)
       
    def _func(self):
        self.read(parse_fn=self.parse_fn)       
        if self.log:
            self._logdata()          
            
            
    def _logdata(self):
        with open(self.log_filename, 'a', newline='\n') as logfile:
            f = csv.writer(logfile)
            f.writerow(self.pico_data)
            

  



if __name__ == '__main__':
    
    def parse_data(msg):
        msg = msg.strip('\r\n')
        T,SP = msg.split(',')
        return [float(T),float(SP)]   

    pico_com = PicoCom(log_filename='test.csv')
    pico_com.poll(interval=2, parse_fn=parse_data)

    
        