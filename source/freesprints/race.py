from pygame.locals import *
import helpers
import hardware
import timeit

class Race(object):
    options = None
    participants = None
    start_time = None
    
    def __init__(self, options_object, participants_list = None):
        self.options = options_object
        self.participants = participants_list

    def start(self):
        self.start_time = timeit.default_timer()
        
    def render(self):
        pass
    
    def set_participants(self, participants_list):
        self.participants = participants_list

    def elapsed_time(self):
        print self.start_time
        print timeit.default_timer()
        return timeit.default_timer() - self.start_time


class Options(object):
    distance = None # meters
    participants = None
    
    _roller_controller = None
    
    def __init__(self):
        self._roller_controller = hardware.RollerController()
        self.distance = 300 # default distance
    
    def set_distance(self, distance):
        self.distance = distance
    
    def set_participants(self, participants):
        self.participants = participants
    
    def get_participants(self):
        return self.participants
        
    def __str__(self):
        return helpers.string_representation(self, {
            "participants": self.participants,
            "distance": self.distance
        })


class Participant(object):
    roller = None
    name = None
    color = None
    
    def __init__(self, name, roller_pin, color = Color("pink")):
        self.color = color
        
        self.roller = hardware.get_roller_controller().get_roller_for_pin(roller_pin)
    
    def increase_distance(self):
        self.roller.increase_spin_count()

    def get_distance(self):
        return float((self.roller.spin_count * self.roller.diameter) / 1000)
