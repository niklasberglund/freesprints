from pygame.locals import *
import helpers
import hardware

class Race(object):
    options = None
    
    def __init__(self, options_object):
        self.options = options_object

    def start(self):
        pass
        
    def render(self):
        pass


class Options(object):
    distance = None # meters
    participants = None
    
    _roller_controller = None
    
    def __init__(self):
        self._roller_controller = hardware.RollerController()
    
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
    distance = 0
    
    def __init__(self, name, roller_pin, color = Color("pink")):
        self.roller = hardware.Roller(roller_pin)
    
    def set_distance(self, new_distance):
        self.distance = new_distance
    
    def increase_distance(self, increment):
        self.distance = self.distance + increment

