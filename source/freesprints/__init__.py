import pygame, sys
import pygame.font
import pygame.locals
import logging
import FSMenu
import helpers as helpers
import plugins
import os.path

# platform-specific imports
if helpers.is_running_on_rpi():# running on Raspberry Pi
    import RPi.GPIO
    import os
    print "ON RASPBERRY PI"
    #os.environ['SDL_VIDEODRIVER']="fbcon"
    #os.environ["SDL_FBDEV"] = "/dev/fb1"
    print "SET DRIVER"
else: # running on computer
    import FakeRPiGPIO.GPIO


class Application(object):
    instance = None
    
    # application state constants
    STATE_MAINMENU = 0
    STATE_INGAME = 1

    # member variables
    window_surface = None
    menu_surface = None
    menu = None
    state = STATE_MAINMENU
    plugin_loader = None

    def __init__(self):
        print "Application.__init__"

        pygame.font.init()

        menu_options_dict = {
            "font_path": "fonts/Cave-Story.ttf",
            "font_size": 42,
            "color_background": (0, 0, 0),
            "color_text": (255, 255, 255),
            "color_text_highlight": (100, 20, 45)
        }

        menu_structure = [
            {
                "title": "New race",
                "callback": self.start_game,
                "submenu": [
                    {
                        "title": "Start",
                        "callback": self.start_game
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
                            "verifier": None,
                            "value": "2"
                        },
                        "callback": self.start_game
                    },
                    {
                        "title": "Roller diameter(mm)",
                        "input": {
                            "type": "int",
                            "verifier": None,
                            "value": "200"
                        }
                    }
                ]
            },
            {
                "title": "Options",
                "callback": self.show_options
            },
            {
                "title": "Exit",
                "callback": self.exit
            }
        ]
        #self.window_surface = pygame.display.set_mode((500, 400), pygame.FULLSCREEN, 32)
        pygame.display.init()
        self.window_surface = pygame.display.set_mode((800, 600), 0, 32)

        menu_options = FSMenu.MenuOptions(menu_options_dict)
        self.menu = FSMenu.Menu(self.window_surface, menu_structure, menu_options)

    def load_plugins(self):
        self.plugin_loader = plugins.PluginLoader()

    def start_game(self):
        print "start game"
        plugins = self.plugin_loader.getAvailablePlugins()
        plugins[0].start()

    def show_options(self):
        print "show options"

    def exit(self):
        pygame.quit()
        sys.exit()

    def hide(self):
        pass

    def get_window_surface(self):
        return self.window_surface

    def game_loop(self):
        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.exit()
                elif event.type == pygame.locals.KEYUP:
                    self.menu.registerKeypress(event.key)

    def start(self):
        # set up pygame
        pygame.init()
        pygame.font.init()

        if helpers.is_running_on_rpi():
            disp_no = os.getenv("DISPLAY")

            if disp_no:
                print "I'm running under X display = {0}".format(disp_no)

            # Check which frame buffer drivers are available
            # Start with fbcon since directfb hangs with composite output
            drivers = ['fbcon', 'directfb', 'svgalib']
            found = False
            for driver in drivers:
                # Make sure that SDL_VIDEODRIVER is set
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    pygame.display.init()
                except pygame.error:
                    print 'Driver: {0} failed.'.format(driver)
                    continue
                found = True
                break

            if not found:
                raise Exception('No suitable video driver found!')

            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            print "Framebuffer size: %d x %d" % (size[0], size[1])
            #self.window_surface = pygame.display.set_mode(size, pygame.FULLSCREEN)

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
        #text = basicFont.render('asdasd', True, WHITE, BLUE)
        #textRect = text.get_rect()
        #textRect.centerx = self.window_surface.get_rect().centerx
        #textRect.centery = self.window_surface.get_rect().centery

        # draw the white background onto the surface
        self.window_surface.fill(BLACK)

        # draw a green polygon onto the surface
        pygame.draw.polygon(self.window_surface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

        # draw some blue lines onto the surface
        pygame.draw.line(self.window_surface, BLUE, (60, 60), (120, 60), 4)
        pygame.draw.line(self.window_surface, BLUE, (120, 60), (60, 120))
        pygame.draw.line(self.window_surface, BLUE, (60, 120), (120, 120), 4)

        # draw a blue circle onto the surface
        pygame.draw.circle(self.window_surface, BLUE, (300, 50), 20, 0)

        # draw a red ellipse onto the surface
        pygame.draw.ellipse(self.window_surface, RED, (450, 160, 40, 80), 1)

        # draw the text's background rectangle onto the surface
        #pygame.draw.rect(self.window_surface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

        # get a pixel array of the surface
        #pixArray = pygame.PixelArray(self.window_surface)
        #pixArray[480][380] = BLACK
        #del pixArray

        # draw the text onto the surface
        #self.window_surface.blit(text, textRect)

        # image
        cyclist = pygame.image.load('images/1p_small.png').convert()
        cyclistRect = cyclist.get_rect()
        cyclistRect.centerx = 100
        cyclistRect.centery = 100
        self.window_surface.blit(cyclist, cyclistRect)

        # draw the window onto the screen
        pygame.display.update()

        self.menu.render()
        self.game_loop()


app = None

def get_app():
    global app
    if app == None:
        app = Application()
    
    return app


def init():
    global app

    print "start"
    app = get_app()
    app.load_plugins()
    app.start()

