import helpers
import os
import os.path
import json
import imp
import source.freesprints
from pygame.locals import *

class PluginLoader:
    available_plugins = None
    
    def __init__(self):
        self.checkAvailablePlugins()
        
    def checkAvailablePlugins(self):
        print helpers.pluginsPath()
        
        plugin_dirs = [plugin_path for plugin_path in os.listdir(helpers.pluginsPath())] #if os.path.isdir(f)]
        
        self.available_plugins = []
        
        for plugin_path in plugin_dirs:
            print plugin_path
            plugin_path_absolute = os.path.join(helpers.pluginsPath(), plugin_path)
            json_info_path = os.path.join(plugin_path_absolute, "info.json")
            
            json_info_data = open(json_info_path)
            
            jsonInfo = json.load(json_info_data)
            
            self.available_plugins.append(Plugin(jsonInfo, plugin_path_absolute))
            
                
        
    def getAvailablePlugins(self):
        return self.available_plugins
        
class Plugin:
    path = None
    name = None
    version = None
    author = None
    
    module = None
    plugin_object = None
    
    def __init__(self, info_json, path):
        self.path = path
        
        self.name = info_json.get("name")
        self.version = info_json.get("version")
        self.author = info_json.get("author")
        
        print info_json
        
        self.init_module()
        
    def init_module(self):
        #module = imp.find_module("pluginModule", [self.path])
        self.module = imp.load_source("pluginModule", os.path.join(self.path, "__init__.py"))
        
        print "FIND MODULE:"
        print self.module

        self.plugin_object = self.module.VisualisationPlugin(source.freesprints.get_app())
        #self.plugin_object.start()
        #self.plugin_object.spinCount(123, 0)

    def start(self):
        source.freesprints.get_app().get_window_surface().fill(Color("black"))
        self.plugin_object.start()



