import math
import pygame
from pygame.locals import *
import os.path
import sys


class VisualisationPlugin:
    meter_center = (200, 200)
    needle_length = 100
    display_surface = None
    plugin_object = None
    race_object = None
    
    needle_length = 140
    
    background_image = None
    
    gauge_center = (514, 375) # gauge center position in background image
    gauge_rect = pygame.Rect(330, 200, 360, 350)
    time_display_rect = pygame.Rect(10, 10, 180, 80)
    
    start_time = None
    
    application = None
    
    def __init__(self, application_object, plugin_object):
        print "init in plugin"
        self.application = application_object
        self.plugin_object = plugin_object
        self.display_surface = self.application.get_window_surface()

    def start(self, race_object):
        print "start in plugin"
        print "race object sent to plugin:"
        print race_object
        
        self.race_object = race_object
        self.render()
        
        clock = pygame.time.Clock()
        while True:
          clock.tick(50)
          
          for event in pygame.event.get():
              if event.type == pygame.locals.KEYUP:
                  if event.key == pygame.locals.K_ESCAPE:
                      pygame.quit()
                      sys.exit()
                  elif event.key == pygame.locals.K_a:
                      if (self.race_object):
                          participant = self.race_object.participants[0]
                          participant.increase_distance(0.5)
                          print self.race_object.participants[0].distance
                          print self.race_object.elapsed_time()
                  elif event.key == pygame.locals.K_s:
                      if (self.race_object):
                          participant = self.race_object.participants[1]
                          participant.increase_distance(0.5)
                          print self.race_object.participants[1].distance
                          print self.race_object.elapsed_time()
        
          # Clear the screen
          #self.display_surface.fill((0, 0, 0))
          
          self.update()

    def spinCount(self, count, roller):
        print "spinCount in plugin"

    def render(self):
        # Resolution
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h
        
        background_image_path = os.path.join(self.plugin_object.path, "images/background-wood2-1024x768.png")
        self.background_image = pygame.image.load(background_image_path).convert()
        backgroundRect = self.background_image.get_rect()
        backgroundRect.x = 0
        backgroundRect.y = 0
        self.display_surface.blit(self.background_image, backgroundRect)
        
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
    
    def update(self):
        self.clear_gauge()
        self.update_gauge()
        
        self.update_time_display()
        
        pygame.display.update()

    def clear_gauge(self):
        self.display_surface.blit(self.background_image, (self.gauge_rect[0], self.gauge_rect[1]), self.gauge_rect)

    def update_gauge(self):        
        line1_angle = (self.race_object.participants[0].distance / self.race_object.options.distance) * 360
        line1_x2 = self.gauge_center[0] + math.cos(math.radians(line1_angle - 90)) * self.needle_length
        line1_y2 = self.gauge_center[1] + math.sin(math.radians(line1_angle - 90)) * self.needle_length
        pygame.draw.line(self.display_surface, Color("red"), self.gauge_center, (line1_x2, line1_y2), 1)
        
        line2_angle = (self.race_object.participants[1].distance / self.race_object.options.distance) * 360
        line2_angle_radians = line2_angle * (180 / math.pi)
        line2_x2 = self.gauge_center[0] + math.cos(math.radians(line2_angle - 90)) * self.needle_length
        line2_y2 = self.gauge_center[1] + math.sin(math.radians(line2_angle - 90)) * self.needle_length
        pygame.draw.line(self.display_surface, Color("blue"), self.gauge_center, (line2_x2, line2_y2), 1)

    def update_time_display(self):
        self.display_surface.fill(Color("black"), self.time_display_rect)
        
        font_path = "./fonts/Cave-Story.ttf"
        time_font = pygame.font.Font(font_path, 68)

        # set up the text
        time_string = str(round(self.race_object.elapsed_time(), 2))
        print time_string
        text = time_font.render(time_string, True, Color("white"), None)
        text_rect = text.get_rect()
        text_rect.centerx = self.time_display_rect.centerx
        text_rect.centery = self.time_display_rect.centery
        
        self.display_surface.blit(text, text_rect)
