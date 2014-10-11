from pygame.locals import *
import helpers
import hardware

class Race(object):
    options = None
    participants = None
    
    def __init__(self, options_object, participants_list = None):
        self.options = options_object
        self.participants = participants_list

    def start(self):
        pass
        
    def render(self):
        pass
    
    def set_participants(self, participants_list):
        self.participants = participants_list


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
    distance = 0
    
    def __init__(self, name, roller_pin, color = Color("pink")):
        self.roller = hardware.Roller(roller_pin)
    
    def set_distance(self, new_distance):
        self.distance = new_distance
    
    def increase_distance(self, increment):
        self.distance = self.distance + increment

