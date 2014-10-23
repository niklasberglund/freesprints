# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio

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

event_detect_mapping = {}

    
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
    
    event_detect_mapping[number] = callback

def cleanup():
    pass
