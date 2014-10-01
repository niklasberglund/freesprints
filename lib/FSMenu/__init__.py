import pygame, sys
import pygame.font
#from pygame.locals import *
import pygame.locals
import timeit

class Menu:
    items = []
    currentItems = None
    currentIndex = 0
    menuPosition = []
    displaySurface = None
    
    # optimization
    clearIndex = None
    
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

        if menuOptions == None:
            menuOptions = MenuOptions() # with default values

        self.font = menuOptions.getItemFont()

        # populate with MenuItem objects
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
        
        if key == pygame.locals.K_ESCAPE: # ESC
            if self.getParentMenu() != None:
                self.currentItems = self.getSiblingsOfItem(self.getParentMenu())
                self.currentIndex = 0
                self.clear()
                self.render()
            else:
                pygame.quit()
                sys.exit()
        elif key == pygame.locals.K_q:
            pygame.quit()
            sys.exit()
        elif key == pygame.locals.K_UP:
            print "UP"
            self.clearIndex = self.currentIndex
            self.moveUp()
            self.render()
        elif key == pygame.locals.K_DOWN:
            print "DOWN"
            self.clearIndex = self.currentIndex
            self.moveDown()
            self.render()
        elif key == pygame.locals.K_RETURN:
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

    def render(self):
        start_time = timeit.default_timer()
        
        if self.clearIndex == None:
            self.renderFull()
        else:
            print "PARTIAL RENDER"
            self.renderItemAtIndex(self.clearIndex)
            self.renderItemAtIndex(self.currentIndex)
            self.clearIndex = None
            
        pygame.display.update()
            
        elapsed_time = timeit.default_timer() - start_time
        print "\033[91mMenu.render time: " + str(elapsed_time) + "\033[0m"

    def renderFull(self):
        #start_time = timeit.default_timer()
        
        print "Menu.render"
        
        i = 0
        for menuItem in self.currentItems:
            print "currentIndex: " + str(self.currentIndex)
            self.renderItemAtIndex(i)
            i = i+1
        
        #elapsed_time = timeit.default_timer() - start_time
        #print "\033[91mMenu.renderFull time: " + str(elapsed_time) + "\033[0m"

    def renderChange(self):
        start_time = timeit.default_timer()
        if self.clearIndex == None:
            self.renderFull()
        else:
            self.renderItemAtIndex(self.clearIndex)
            self.renderItemAtIndex(self.currentIndex)
            self.clearIndex = None
        
        elapsed_time = timeit.default_timer() - start_time
        print "\033[91mMenu.renderChange time: " + str(elapsed_time) + "\033[0m"

    def renderItemAtIndex(self, index):
        item = self.currentItems[index]
        
        if index == self.currentIndex:
            text = item.getHighlightedText()
        else:
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
        #self.displaySurface.fill(self.colorBlack)
        leftmost_x = 0
        rightmost_x = 0
        
        last_item_rect = self.currentItems[-1].getText().get_rect()
        
        for menu_item in self.currentItems:
            rect = menu_item.getText().get_rect()
            if (rect.x < leftmost_x ): leftmost_x = rect.x
            if (rect.x + rect.width > rightmost_x): rightmost_x = rect.x + rect.width
        
        clear_width = rightmost_x - leftmost_x
        clear_height = last_item_rect.height * len(self.currentItems)
        clear_x = self.displaySurface.get_rect().centerx - (clear_width/2)
        clear_y = self.displaySurface.get_rect().centery - ((len(self.currentItems)*last_item_rect.height)/2)
        clear_rect = pygame.Rect(clear_x, clear_y, clear_width, clear_height)
        
        self.displaySurface.fill(pygame.locals.Color("black"), clear_rect)

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
                siblings = self.getSiblingsOfItem(needleItem, item.getSubmenu())
                
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
    
    input_type = None
    input_verifier = None
    input_value = None
    
    
    def __init__(self, dict, menuOptions, itemParent = None):
        print "dict:"
        print dict
        self.title = dict['title']
        self.parent = itemParent
        self.font = menuOptions.getItemFont()
        
        self.callback = dict.get("callback")
        
        input = dict.get("input")
        if input != None:
            self.input_type = input.get("type")
            self.input_verifier = input.get("verifier")
            self.input_value = input.get("value")
        
        if dict.has_key("submenu"):
            self.submenu = MenuItem.itemsListFromDict(dict['submenu'], menuOptions, self)
        
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
            title_string = self.title if self.input_value == None else self.title + ":"
            item_text = self.font.render(title_string, True, Menu.colorWhite, None)
            item_value = self.font.render(self.input_value, True, Menu.colorGreen, None)
            item_text_rect = item_text.get_rect()
            item_value_rect = item_value.get_rect()
            width = item_text_rect.width + item_value_rect.width
            height = item_text_rect.height
            
            item_text_rect.x = 0
            item_text_rect.y = 0
            
            item_value_rect.x = item_text_rect.width
            item_value_rect.y = 0
            
            text_surface = pygame.Surface([width, height], pygame.SRCALPHA, 32)
            text_surface.blit(item_text, item_text_rect)
            text_surface.blit(item_value, item_value_rect)
            
            self.text = text_surface
        
        return self.text
        
    def getHighlightedText(self):
        if self.highlightedText == None:
            title_string = self.title if self.input_value == None else self.title + ":"
            item_text = self.font.render(title_string, True, Menu.colorRed, None)
            item_value = self.font.render(self.input_value, True, Menu.colorGreen, None)
            item_text_rect = item_text.get_rect()
            item_value_rect = item_value.get_rect()
            width = item_text_rect.width + item_value_rect.width
            height = item_text_rect.height
            
            item_text_rect.x = 0
            item_text_rect.y = 0
            
            item_value_rect.x = item_text_rect.width
            item_value_rect.y = 0
            
            text_surface = pygame.Surface([width, height], pygame.SRCALPHA, 32)
            text_surface.blit(item_text, item_text_rect)
            text_surface.blit(item_value, item_value_rect)
            
            self.highlightedText = text_surface
            
        return self.highlightedText
        
    @staticmethod
    def itemsListFromDict(dict, menuOptions, itemsParent = None):
        itemsList = []
        
        for itemDict in dict:
            itemsList.append(MenuItem(itemDict, menuOptions, itemsParent))
        
        return itemsList


class MenuOptions(object):
    # options
    font_name = None
    font_path = None
    font_size = None
    color_background = None
    color_text = None
    color_text_highlight = None

    # created
    itemFont = None
    valueFont = None

    def __init__(self, optionsDict):
        # read options
        self.font_name = optionsDict.get("font_name")
        self.font_path = optionsDict.get("font_path")
        self.font_size = optionsDict.get("font_size")
        self.color_background = optionsDict.get("color_background")
        self.color_text = optionsDict.get("color_text")
        self.color_text_highlight = optionsDict.get("color_text_highlight")
        
        # default values
        if self.font_size == None:
            self.font_size = 40
            
            
        # create based on specified options
        if self.font_name != None:
            self.itemFont = pygame.font.SysFont(self.font_name, self.font_size)
            
        if self.font_path != None:
            self.itemFont = pygame.font.Font(self.font_path, self.font_size)

    def getItemFont(self):
        return self.itemFont

    def getValueFont(self):
        return self.valueFont
