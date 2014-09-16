import helpers

# platform-specific imports
if helpers.is_running_on_rpi():# running on Raspberry Pi
    import RPi.GPIO as GPIO
    print "freesprints.hardware using Rpi.GPIO"
else: # running on computer
    import FakeRPiGPIO.GPIO as GPIO
    print "freesprints.hardware using FakeRpiGPIO.GPIO"

class Roller(object):
    pin = None # board number
    number = None
    spin_count = 0
    spin_callback = None
    
    def __init__(self, pin):
        self.pin = pin
    
    def set_spin_callback(self, callback_function):
        self.spin_callback = callback_function
    
    



class RollerController(object):
    rollers = []
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
    def get_rollers(self):
        return rollers
        
    def get_roller_for_pin(pin_number):
        return Roller(pin_number)
