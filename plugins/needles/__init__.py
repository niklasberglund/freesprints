import math
import pygame
from pygame.locals import *

class VisualisationPlugin:
    meter_center = (200, 200)
    needle_length = 100
    display_surface = None
    plugin_object = None
    
    application = None
    
    def __init__(self, application_object, plugin_object):
        print "init in plugin"
        self.application = application_object
        self.plugin_object = plugin_object
        self.display_surface = self.application.get_window_surface()

    def start(self, race_options):
        print "start in plugin"
        print "race options sent to plugin:"
        print race_options
        self.render()

    def spinCount(self, count, roller):
        print "spinCount in plugin"

    def render(self):
        background = pygame.image.load('images/needles-background-1024x768.png').convert()
        backgroundRect = background.get_rect()
        backgroundRect.x = 0
        backgroundRect.y = 0
        self.display_surface.blit(background, backgroundRect)
        
        needle = pygame.image.load('images/needle.png').convert()
        needleRect = needle.get_rect()
        needleRect.centerx = 600
        needleRect.centery = 500
        self.display_surface.blit(needle, needleRect)
        
        angle = 45
        end_x = self.meter_center[0] + math.cos(math.radians(angle)) * self.needle_length
        end_y = self.meter_center[1] + math.sin(math.radians(angle)) * self.needle_length
        pygame.draw.line(self.display_surface, Color("red"), self.meter_center, (end_x, end_y), 1)
        
        pygame.display.update()
