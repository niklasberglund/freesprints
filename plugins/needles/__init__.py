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
    participant_info_box_width = 194
    participant_info_box_height = 90
    
    background_image = None
    
    font_big = None
    font_distance = None
    
    gauge_center = (514, 375) # gauge center position in background image
    gauge_rect = pygame.Rect(330, 200, 360, 350)
    time_icon_rect = pygame.Rect(10, 10, 80, 80)
    time_display_rect = pygame.Rect(90, 10, 194, 80)
    
    application = None
    
    def __init__(self, application_object, plugin_object):
        print "init in plugin"
        self.application = application_object
        self.plugin_object = plugin_object
        self.display_surface = self.application.get_window_surface()
        
        font_path = "./fonts/Cave-Story.ttf"
        distance_font_path = "./fonts/Warenhaus-Standard.ttf"
        self.font_big = pygame.font.Font(distance_font_path, 68)
        self.font_distance = pygame.font.Font(distance_font_path, 50)

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
                          participant.increase_distance()
                          print self.race_object.participants[0].get_distance()
                          #print self.race_object.elapsed_time()
                  elif event.key == pygame.locals.K_s:
                      if (self.race_object):
                          participant = self.race_object.participants[1]
                          participant.increase_distance()
                          print self.race_object.participants[1].get_distance()
                          #print self.race_object.elapsed_time()
        
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
        
        background_image_path = os.path.join(self.plugin_object.path, "images/background-wood3-1024x768.png")
        self.background_image = pygame.image.load(background_image_path).convert()
        backgroundRect = self.background_image.get_rect()
        backgroundRect.x = 0
        backgroundRect.y = 0
        self.display_surface.blit(self.background_image, backgroundRect)
        
        self.render_time_icon()
        
        #needle_image_path = os.path.join(self.plugin_object.path, "images/needle.png")
        #needle = pygame.image.load(needle_image_path).convert()
        #needleRect = needle.get_rect()
        #needleRect.centerx = 600
        #needleRect.centery = 500
        #self.display_surface.blit(needle, needleRect)
        
        pygame.display.update()

    def render_time_icon(self):
        self.display_surface.fill(Color("black"), self.time_icon_rect)
        
        time_icon_path = os.path.join(self.plugin_object.path, "images/stopwatch.png")
        time_icon = pygame.image.load(time_icon_path).convert()
        time_icon_image_rect = time_icon.get_rect()
        time_icon_image_rect.centerx = self.time_icon_rect.centerx
        time_icon_image_rect.centery = self.time_icon_rect.centery
        self.display_surface.blit(time_icon, time_icon_image_rect)
    
    def update(self):
        self.clear_gauge()
        self.update_gauge()
        
        self.update_time_display()
        
        self.update_boxes()
        
        pygame.display.update()

    def clear_gauge(self):
        self.display_surface.blit(self.background_image, (self.gauge_rect[0], self.gauge_rect[1]), self.gauge_rect)

    def update_gauge(self):
        line1_angle = (self.race_object.participants[0].get_distance() / self.race_object.options.distance) * 360
        line1_x2 = self.gauge_center[0] + math.cos(math.radians(line1_angle - 90)) * self.needle_length
        line1_y2 = self.gauge_center[1] + math.sin(math.radians(line1_angle - 90)) * self.needle_length
        pygame.draw.line(self.display_surface, self.race_object.participants[0].color, self.gauge_center, (line1_x2, line1_y2), 1)
        print "line1: " + str(self.race_object.participants[0].get_distance())
        
        line2_angle = (self.race_object.participants[1].get_distance() / self.race_object.options.distance) * 360
        line2_angle_radians = line2_angle * (180 / math.pi)
        line2_x2 = self.gauge_center[0] + math.cos(math.radians(line2_angle - 90)) * self.needle_length
        line2_y2 = self.gauge_center[1] + math.sin(math.radians(line2_angle - 90)) * self.needle_length
        pygame.draw.line(self.display_surface, self.race_object.participants[1].color, self.gauge_center, (line2_x2, line2_y2), 1)
        print "line2: " + str(self.race_object.participants[1].get_distance())

    def update_time_display(self):
        self.display_surface.fill(Color("black"), self.time_display_rect)

        # set up the text
        time_string = '{0:.2f}'.format(self.race_object.elapsed_time())
        #print time_string
        text = self.font_big.render(time_string, True, Color("white"), None)
        text_rect = text.get_rect()
        text_rect.centerx = self.time_display_rect.centerx
        text_rect.centery = self.time_display_rect.centery
        self.display_surface.blit(text, text_rect)

    def update_boxes(self):
        self.render_participant_info_box(self.race_object.participants[0], (800, 20))
        self.render_participant_info_box(self.race_object.participants[1], (800, 150))

    def render_participant_info_box(self, participant, position):
        box_rect = pygame.Rect(position[0], position[1], self.participant_info_box_width, self.participant_info_box_height)
        self.display_surface.fill(Color("black"), box_rect)
        
        color_box_width = 20
        color_box_rect = pygame.Rect(position[0] - color_box_width, position[1], color_box_width, self.participant_info_box_height)
        self.display_surface.fill(participant.color, color_box_rect)
        
        distance_string = str('{0:.2f}'.format(participant.get_distance())) + 'm'
        text = self.font_distance.render(distance_string, True, Color("white"), None)
        text_rect = text.get_rect()
        text_rect.centerx = box_rect.centerx
        text_rect.centery = box_rect.centery
        self.display_surface.blit(text, text_rect)


