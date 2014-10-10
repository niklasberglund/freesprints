import math
import pygame
from pygame.locals import *
import os.path


class VisualisationPlugin:
    meter_center = (200, 200)
    needle_length = 100
    display_surface = None
    plugin_object = None
    
    gauge_center = (514, 375) # gauge center position in background image
    
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
        # Resolution
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h
        
        background_image_path = os.path.join(self.plugin_object.path, "images/background-wood2-1024x768.png")
        background = pygame.image.load(background_image_path).convert()
        backgroundRect = background.get_rect()
        backgroundRect.x = 0
        backgroundRect.y = 0
        self.display_surface.blit(background, backgroundRect)
        
        #needle_image_path = os.path.join(self.plugin_object.path, "images/needle.png")
        #needle = pygame.image.load(needle_image_path).convert()
        #needleRect = needle.get_rect()
        #needleRect.centerx = 600
        #needleRect.centery = 500
        #self.display_surface.blit(needle, needleRect)     
        
        line_length = 140
        
        line1_angle = 0
        line1_x2 = self.gauge_center[0] + math.cos(math.radians(line1_angle - 90)) * line_length
        line1_y2 = self.gauge_center[1] + math.sin(math.radians(line1_angle - 90)) * line_length
        pygame.draw.line(self.display_surface, Color("red"), self.gauge_center, (line1_x2, line1_y2), 1)
        
        line2_angle = 270
        line2_angle_radians = line2_angle * (180 / math.pi)
        line2_x2 = self.gauge_center[0] + math.cos(math.radians(line2_angle - 90)) * line_length
        line2_y2 = self.gauge_center[1] + math.sin(math.radians(line2_angle - 90)) * line_length
        pygame.draw.line(self.display_surface, Color("blue"), self.gauge_center, (line2_x2, line2_y2), 1)
        
        pygame.display.update()
