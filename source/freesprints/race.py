from pygame.locals import *
import helpers

class Race(object):
    options = None
    participants = None
    
    def __init__(self, options_object):
        self.options = options_object
        self.participants = participants_list

    def start(self):
        pass
        
    def render(self):
        pass


class Options(object):
    distance = None # meters
    participants = None
    
    _roller_controller = None
    
    def __init__(self):
        _roller_controller = RollerController()
    
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
        self.roller = Roller(roller_pin)


class Roller(object):
    def __init__(self, pin_number):
        pass


class RollerController(object):
    sensor_roller_list = None
    
    def __init__(self):
        pass
