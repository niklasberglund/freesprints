import helpers
import os
import os.path
import json
import imp
import source.freesprints

class PluginLoader:
    availablePlugins = None
    
    def __init__(self):
        self.checkAvailablePlugins()
        
    def checkAvailablePlugins(self):
        print helpers.pluginsPath()
        
        pluginDirs = [pluginPath for pluginPath in os.listdir(helpers.pluginsPath())] #if os.path.isdir(f)]
        
        self.availablePlugins = []
        
        for pluginPath in pluginDirs:
            print pluginPath
            pluginPathAbsolute = os.path.join(helpers.pluginsPath(), pluginPath)
            jsonInfoPath = os.path.join(pluginPathAbsolute, "info.json")
            
            jsonInfoData = open(jsonInfoPath)
            
            jsonInfo = json.load(jsonInfoData)
            
            self.availablePlugins.append(Plugin(jsonInfo, pluginPathAbsolute))
            
                
        
    def getAvailablePlugins(self):
        pass
        
class Plugin:
    path = None
    name = None
    version = None
    author = None
    
    module = None
    pluginObject = None
    
    def __init__(self, infoJson, path):
        self.path = path
        
        self.name = infoJson.get("name")
        self.version = infoJson.get("version")
        self.author = infoJson.get("author")
        
        print infoJson
        
        self.initModule()
        
    def initModule(self):
        #module = imp.find_module("pluginModule", [self.path])
        self.module = imp.load_source("pluginModule", os.path.join(self.path, "__init__.py"))
        
        print "FIND MODULE:"
        print self.module

        self.pluginObject = self.module.VisualisationPlugin(source.freesprints.get_app())
        self.pluginObject.start()
        self.pluginObject.spinCount(123, 0)
        





