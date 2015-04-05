import pygame, sys
import pygame.font
from pygame.locals import *
import logging
import fs_menu
import helpers as helpers
import plugins
import os.path
import race
import hardware
import defaults
import logging
from rainbow_logging_handler import RainbowLoggingHandler

DISPLAY_RESOLUTION = (1024, 768)

# platform-specific imports
if helpers.is_running_on_rpi():# running on Raspberry Pi
    import RPi.GPIO
    import os
    print "ON RASPBERRY PI"
    #os.environ['SDL_VIDEODRIVER']="fbcon"
    #os.environ["SDL_FBDEV"] = "/dev/fb1"
    print "SET DRIVER"
else: # running on computer
    import FakeRPi.GPIO


class Application(object):
    instance = None
    state = None
    
    # application state constants
    STATE_MAINMENU = 0
    STATE_INGAME = 1

    # member variables
    window_surface = None
    menu_surface = None
    menu = None
    state = STATE_MAINMENU
    plugin_loader = None
    roller_controller = None
    race_options = None
    race_object = None
    selected_plugin_index = 0 # 0 by default. this should ideally be restored from stored settings

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
                "callback": self.start_race,
                "submenu": [
                    {
                        "title": "Start",
                        "callback": self.start_race
                    },
                    {
                        "title": "Race visualizer",
                        "callback": None,
                        "submenu_populator_callback": self.populate_visualizers,
                        "identifier": "race_visualizer_selection"
                    },
                    {
                        "title": "Number of rollers",
                        "input": {
                            "type": "int",
                            "verifier": None,
                            "value": "2"
                        },
                        "callback": self.start_race
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
        self.window_surface = pygame.display.set_mode(defaults.RESOLUTION, 0, 32)

        menu_options = fs_menu.MenuOptions(menu_options_dict)
        self.menu = fs_menu.Menu(self.window_surface, menu_structure, menu_options)
        
        self.roller_controller = hardware.RollerController()

    def load_plugins(self):
        self.plugin_loader = plugins.PluginLoader()

    def start_race(self):
        print "start game"
        self.state = self.STATE_INGAME
        
        race_options = race.Options()
        race_participants = ([
            race.Participant("Niklas", 7, Color("red")),
            race.Participant("Some loser", 11, Color("blue"))
        ])
        
        self.race_object = race.Race(race_options, race_participants)
        
        plugins = self.plugin_loader.getAvailablePlugins()
        
        self.race_object.start()
        plugins[self.selected_plugin_index].start(self.race_object)

    def show_options(self):
        print "show options"

    def populate_visualizers(self):
        print "populate_visualizers"
        
        submenu = []
        pluginIndex = 0
        
        for plugin in self.plugin_loader.getAvailablePlugins():
            submenu.append({
                "title": plugin.name,
                "callback": self.select_plugin,
                "tag": pluginIndex
            })
            
            pluginIndex = pluginIndex + 1
        
        return submenu

    def select_plugin(self, plugin_index):
        print "selected plugin with index " + str(plugin_index)
        self.selected_plugin_index = plugin_index

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
                    if self.state == self.STATE_MAINMENU:
                        self.menu.registerKeypress(event.key)
                    elif event.key == pygame.locals.K_ESCAPE:
                        self.exit()

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
        #pygame.draw.polygon(self.window_surface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

        # draw some blue lines onto the surface
        #pygame.draw.line(self.window_surface, BLUE, (60, 60), (120, 60), 4)
        #pygame.draw.line(self.window_surface, BLUE, (120, 60), (60, 120))
        #pygame.draw.line(self.window_surface, BLUE, (60, 120), (120, 120), 4)

        # draw a blue circle onto the surface
        #pygame.draw.circle(self.window_surface, BLUE, (300, 50), 20, 0)

        # draw a red ellipse onto the surface
        #pygame.draw.ellipse(self.window_surface, RED, (450, 160, 40, 80), 1)
        
        # menu background
        background = pygame.image.load('images/menu_background.png').convert()
        backgroundRect = background.get_rect()
        backgroundRect.x = 0
        backgroundRect.y = 0
        self.window_surface.blit(background, backgroundRect)

        # draw the window onto the screen
        pygame.display.update()

        self.menu.render()
        self.game_loop()


app = None
logger = None

def get_app():
    global app
    if app == None:
        app = Application()
    
    return app

def get_logger():
    global logger
    
    if logger == None:
        logger = logging.getLogger('freesprints')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s")  # same as default
        
        # setup colored logging
        handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def init():
    global app

    print "start"
    app = get_app()
    app.load_plugins()
    app.start()

