import pygame, sys
import pygame.font
from pygame.locals import *
import timeit

class Menu:
    items = []
    currentItems = None
    currentIndex = 0
    menuPosition = []
    displaySurface = None
    
    # Display
    font = None
    color = None # TODO
    
    # Colors
    colorBlack = (0, 0, 0)
    colorWhite = (255, 255, 255)
    colorRed = (255, 0, 0)
    colorGreen = (0, 255, 0)
    colorBlue = (0, 0, 255)
    
    def __init__(self, displaySurface, menuStructure, menuOptions = None):
        self.displaySurface = displaySurface
        print "MENUOPTIONS:::"
        print menuOptions
        
        font_name = None
        font_path = None
        font_size = 40
        
        pygame.font.init()
        
        if menuOptions != None:
            if menuOptions.has_key("font_size"):
                font_size = menuOptions["font_size"]
                
            if menuOptions.has_key("font_name"):
                font_name = menuOptions["font_name"]
                self.font = pygame.font.SysFont(font_path, font_size)
                
            if menuOptions.has_key("font_path"):
                font_path = menuOptions["font_path"]
                self.font = pygame.font.Font(font_path, font_size)
                
                
                
        pygame.font.init()
        font_path = "./fonts/Cave-Story.ttf"
        self.font = pygame.font.Font(font_path, 48)
        
        # populate with MenuItem objects
        #self.currentItems = MenuItem.itemsListFromDict(menuStructure)
        self.items = MenuItem.itemsListFromDict(menuStructure, menuOptions)
        self.currentItems = self.items
        
        
    def show(self):
        pass
        
    def hide(self):
        pass
        
    def getParentMenu(self):
        print self.currentItems[0].getParentMenu()
        return self.currentItems[0].getParentMenu()
        
    def registerKeypress(self, key):
        print "registered key " + str(key)
        
        if key == K_ESCAPE: # ESC
            print "parent menu:"
            print self.getParentMenu()
            if self.getParentMenu() != None:
                print "HAVE PARENT"
                self.currentItems = self.getSiblingsOfItem(self.getParentMenu())
                self.currentIndex = 0
                self.clear()
                self.render()
                #pygame.quit()
                #sys.exit()
            else:
                print "NO PARENT"
                pygame.quit()
                sys.exit()
                #self.currentItems = self.getParentMenu().getSubmenu()
                #self.render()
        elif key == K_q:
            pygame.quit()
            sys.exit()
        elif key == K_UP:
            print "UP"
            self.moveUp()
            self.render()
        elif key == K_DOWN:
            print "DOWN"
            self.moveDown()
            self.render()
        elif key == K_RETURN:
            print "selected item"
            
            selectedItem = self.currentItems[self.currentIndex]
            
            print selectedItem
            
            if selectedItem.hasSubmenu():
                self.currentItems = selectedItem.getSubmenu()
                self.currentIndex = 0
                self.clear()
                self.render()
            else:
                selectedItem.execute()
    
    #@profile
    def render(self):
        start_time = timeit.default_timer()
        
        print "Menu.render"
        
        i = 0
        for menuItem in self.currentItems:
            print "currentIndex: " + str(self.currentIndex)
            self.renderItemAtIndex(i)
            pygame.display.update()
            i = i+1
            
            elapsed_time = timeit.default_timer() - start_time
        
        print "\033[91mMenu.render time: " + str(elapsed_time) + "\033[0m"
    
    def renderItemAtIndex(self, index):
        item = self.currentItems[index]
        
        if (index == self.currentIndex):
            #textColor = self.colorRed
            text = item.getHighlightedText()
        else:
            #textColor = self.colorWhite
            text = item.getText()
            
        textRect = text.get_rect()
        height = textRect.height
        
        menuStartY = self.displaySurface.get_rect().centery - ((len(self.currentItems)*height)/2)
        y = menuStartY + (index*height)
        
        textRect.centerx = self.displaySurface.get_rect().centerx
        textRect.y = y
        
        print height
        
        #pygame.draw.rect(self.displaySurface, self.colorRed, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))
        self.displaySurface.blit(text, textRect)
        
    def clear(self):
        self.displaySurface.fill(self.colorBlack)
        
    def moveUp(self):
        if self.currentIndex > 0:
            self.currentIndex = self.currentIndex-1
            
        print "currentIndex:" + str(self.currentIndex)
    
    def moveDown(self):
        if self.currentIndex < (len(self.currentItems)-1):
            self.currentIndex = self.currentIndex+1
            
        print "currentIndex:" + str(self.currentIndex)
        print self.currentItems
    
    def getCurrentMenuItems(self):
        pass
        
    def getSiblingsOfItem(self, needleItem, haystackList = None):
        if haystackList == None:
            haystackList = self.items
            
        for item in haystackList:
            if item == needleItem:
                return haystackList
            
            elif item.hasSubmenu():
                siblings = getSiblingsOfItem(needleItem, item.getSubmenu())
                
                if siblings != None:
                    return siblings
            
        return None


class MenuItem(object):
    title = None
    callback = None
    submenuDict = None
    submenu = None
    parent = None
    
    font = None
    text = None
    highlightedText = None
    
    
    def __init__(self, dict, menuOptions, itemParent = None):
        #self._displaySurface = displaySurface
        print "dict:"
        print dict
        self.title = dict['title']
        self.parent = itemParent
        
        print "MenuItem menuOptions:"
        print menuOptions
        
        if menuOptions != None:
            if menuOptions.has_key("font_size"):
                font_size = menuOptions["font_size"]
                
            if menuOptions.has_key("font_name"):
                font_name = menuOptions["font_name"]
                self.font = pygame.font.SysFont(font_path, font_size)
                
            if menuOptions.has_key("font_path"):
                font_path = menuOptions["font_path"]
                self.font = pygame.font.Font(font_path, font_size)
                
        print "self.font:"
        print self.font
        
        if dict.has_key("callback"):
            self.callback = dict['callback']
        
        if dict.has_key("submenu"):
            self.submenu = MenuItem.itemsListFromDict(dict['submenu'], menuOptions, self)
            print "SUBMENU:"
            print self.submenu
        
    def show(self):
        pass
        
    def hide(self):
        pass
        
    def registerKeypress(self, key):
        pass
        
    def execute(self):
        self.callback()
        
    def hasSubmenu(self):
        if self.submenu != None:
            return True
        else:
            return False
            
    def getSubmenu(self):
        return self.submenu
        
    def getParentMenu(self):
        return self.parent
        
    def getText(self):
        if self.text == None:
            self.text = self.font.render(self.title, True, Menu.colorWhite, Menu.colorBlue)
        
        return self.text
        
    def getHighlightedText(self):
        if self.highlightedText == None:
            self.highlightedText = self.font.render(self.title, True, Menu.colorRed, Menu.colorBlue)
            
        return self.highlightedText
        
    @staticmethod
    def itemsListFromDict(dict, menuOptions, itemsParent = None):
        itemsList = []
        
        print "DICT:"
        print dict
        
        for itemDict in dict:
            print "ITEMDICT:"
            print itemDict
            itemsList.append(MenuItem(itemDict, menuOptions, itemsParent))
        
        return itemsList
        

class MenuFolder(MenuItem):
    def __init__(self, title):
        pass
        
    def show(self):
        pass
        
    def hide(self):
        pass
        
    def registerKeypress(self, key):
        pass
