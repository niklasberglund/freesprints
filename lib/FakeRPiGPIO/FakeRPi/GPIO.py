# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio

import threading

VERSION = "0.5.2" # because RPi.GPIO 0.5.2 have support for interrupts(including threaded)

INPUT = 1
OUTPUT = 0

IN = 0
OUT = 1

HIGH = 1
LOW = 0

NO = 0
RISING = 1
FALLING = 2
BOTH = 3

# modes
MODE_UNKNOWN = -1
BOARD = 10
BCM = 11
SERIAL = 40
SPI = 41
I2C = 42
PWM = 43

event_detect_mapping = []

    
def setmode(mode):
    pass

def setup(number, highLow):
    pass

def input(number):
    pass

def output(number, highLow):
    pass

def wait_for_edge(number, edge):
    pass

def add_event_detect(number, risingFalling, callback):
    global event_detect_mapping
    
    event_detect_mapping[number] = {'callback': callback, 'fake_edge': risingFalling}

def cleanup():
    pass

def start_fake_ticks(number, interval):
    fake_ticks_timer = threading.Timer(interval, send_fake_tick, [number])
    event_detect_mapping[number]['timer'] = fake_ticks_timer
    fake_ticks_timer.start()

def stop_fake_ticks(number):
    event_detect_mapping[number]['timer'].cancel()
    event_detect_mapping[number]['timer'] = None

def send_fake_tick(number):
    global event_detect_mapping
    
    event_detect_mapping[number]['callback']()

def fake_edge(number, high_low):
    pass

