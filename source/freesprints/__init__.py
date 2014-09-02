import pygame, sys
import pygame.font
import logging
from pygame.locals import *
import FSMenu
import helpers as helpers

# platform-specific imports
if (helpers.isRunningOnRPi()): # running on Raspberry Pi
    import RPi.GPIO
    import os
    os.environ['SDL_VIDEODRIVER']="fbcon"
else: # running on computer
    import FakeRPiGPIO.GPIO

class Application(object):
    # application state constants
    STATE_MAINMENU = 0
    STATE_INGAME = 1
    
    # member variables
    windowSurface = None
    menuSurface = None
    menu = None
    state = STATE_MAINMENU
    
    def __init__(self):
        print "Application.__init__"
        
        menuOptions = {
            "font_path": "fonts/Cave-Story.ttf",
            "font_size": 42,
            "color_background": (0, 0, 0),
            "color_text": (255, 255, 255),
            "color_text_highlight": (100, 20, 45)
        }
        
        menuStructure = [
            {
                "title": "New race",
                "callback": self.startGame,
                "submenu": [
                    {
                        "title": "Start",
                        "callback": self.startGame
                    },
                    {
                        "title": "Race visualizer",
                        "callback": None,
                        "identifier": "race_visualizer_selection"
                    },
                    {
                        "title": "Number of rollers",
                        "input": {
                            "type": "int",
                            "verifier": None
                        },
                        "callback": self.startGame
                    },
                    {
                        "title": "Roller diameter(mm)",
                        "input": {
                            "type": "int",
                            "verifier": None
                        }
                    }
                ]
            },
            {
                "title": "Options",
                "callback": self.showOptions
            },
            {
                "title": "Exit",
                "callback": self.exit
            }
        ]
        self.windowSurface = pygame.display.set_mode((500, 400), 0, 32)
        self.menu = FSMenu.Menu(self.windowSurface, menuStructure)
        
    def start(self):
        print "asd"
        
    def startGame(self):
        print "start game"
    
    def showOptions(self):
        print "show options"
        
    def exit(self):
        pygame.quit()
        sys.exit()
        
    def hide(self):
        pass
        
    def gameLoop(self):
        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                elif event.type == KEYUP:
                    self.menu.registerKeypress(event.key)
        
    def start(self):
        # set up pygame
        pygame.init()
        pygame.font.init()

        # set up the window
        pygame.display.set_caption('Freesprints')

        # set up the colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        # set up fonts
        #availableFonts = pygame.font.get_fonts()
        font_path = "./fonts/Cave-Story.ttf"
        #basicFont = pygame.font.SysFont(None, 30)
        basicFont = pygame.font.Font(font_path, 48)

        # set up the text
        text = basicFont.render('asdasd', True, WHITE, BLUE)
        textRect = text.get_rect()
        textRect.centerx = self.windowSurface.get_rect().centerx
        textRect.centery = self.windowSurface.get_rect().centery

        # draw the white background onto the surface
        self.windowSurface.fill(WHITE)

        # draw a green polygon onto the surface
        pygame.draw.polygon(self.windowSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

        # draw some blue lines onto the surface
        pygame.draw.line(self.windowSurface, BLUE, (60, 60), (120, 60), 4)
        pygame.draw.line(self.windowSurface, BLUE, (120, 60), (60, 120))
        pygame.draw.line(self.windowSurface, BLUE, (60, 120), (120, 120), 4)

        # draw a blue circle onto the surface
        pygame.draw.circle(self.windowSurface, BLUE, (300, 50), 20, 0)

        # draw a red ellipse onto the surface
        pygame.draw.ellipse(self.windowSurface, RED, (300, 250, 40, 80), 1)

        # draw the text's background rectangle onto the surface
        pygame.draw.rect(self.windowSurface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

        # get a pixel array of the surface
        pixArray = pygame.PixelArray(self.windowSurface)
        pixArray[480][380] = BLACK
        del pixArray

        # draw the text onto the surface
        self.windowSurface.blit(text, textRect)

        # image
        cyclist = pygame.image.load('images/1p_small.png').convert()
        cyclistRect = cyclist.get_rect()
        cyclistRect.centerx = 100
        cyclistRect.centery = 100
        self.windowSurface.blit(cyclist, cyclistRect)


        # draw the window onto the screen
        pygame.display.update()
        
        self.menu.render()
        self.gameLoop()
        
        

app = None

def init():
    global app
    
    app = Application()
    
def start():
    global app
    
    print "start"
    app.start()
    
    