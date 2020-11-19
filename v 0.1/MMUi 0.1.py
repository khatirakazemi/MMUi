import pygame
import itertools #for id
import sys

## universal defaults ##
defaultCOLOR = (22, 55, 156)
defaultFONT_SIZE = 32

## help functions ##
def GetFontDimensions(fontName, size):
    pygame.font.init()
    if fontName == '':
        fontName = None
    test_font = pygame.font.SysFont(fontName, size)
    test_render = test_font.render('1', True, (0 ,0 ,0), (255 ,255, 255))
    test_rect = test_render.get_rect()
    return (test_rect.width, test_rect.height)

## classes ##
class TextBox:

    textBox_idIter = itertools.count() ## next count

    def __init__(self, x, y, w, h,  limit_vertically = bool, text = '', font_name = '', color = defaultCOLOR, border = False, fontSize_override = None): ## defaults 
        self.id = next(self.textBox_idIter) ## id
# properties
        try:
            self.dimensions = [x, y, w, h]
            self.text = text 
            self.limit = 'height' if limit_vertically == True else 'width'
            self.border = border
        except:
            print(self.id, 'error in __init__ #properties')
# format
        try:
            self.color = defaultCOLOR if color == None else color 
            self.font_name = None if font_name == '' else font_name
            if fontSize_override != None:
                self.font = pygame.font.Font(self.font_name, fontSize_override)
            else:
                self.font = self.get_font()
        except:
            print(self.id, 'error in __init__ #format')
# get surface and rect

        self.render()
        

        
    def get_font(self): ## returns font at an apropriate size for the limiting factor
        out_width, out_height = GetFontDimensions(self.font_name, defaultFONT_SIZE)
        fontSize = defaultFONT_SIZE
        if self.limit == 'width':
            while out_width < self.dimensions[2]:
                fontSize += 1
                out_width, out_height = GetFontDimensions(self.font_name, fontSize)
            while out_width > self.dimensions[2]:
                fontSize -= 1
                out_width, out_height = GetFontDimensions(self.font_name, fontSize)
        elif self.limit == 'height':
            while out_height < self.dimensions[3]:
                fontSize += 1
                out_width, out_height = GetFontDimensions(self.font_name, fontSize)
            while out_height > self.dimensions[3]:
                fontSize -= 1
                out_width, out_height = GetFontDimensions(self.font_name, fontSize)
        else:
            print(self.id, 'error in self.get_font()')
        return pygame.font.Font(self.font_name, fontSize)

    def render(self):
# makes the text and border (if specified)
        self.text_surface = self.font.render(self.text, True, self.color)## could add fill feature surface.fill(color)
        width, height = self.font.size(self.text)
        self.text_rect = self.text_surface.get_rect(       center = (  (self.dimensions[0] + (width//2))  , (self.dimensions[1] + (height//2)) )      )
        self.border = pygame.Rect(  self.text_rect.x - 5, self.text_rect.y - 5, self.text_rect.width+10, self.text_rect.height+10  )##for now no border offset function easy to implement tho

    def draw(self, screen):
# blit to screen
        screen.blit(self.text_surface, (self.text_rect.x, self.text_rect.y))
        if self.border == True:
            pygame.draw.rect(screen, COLOR_ACTIVE, self.border, 2)

    def __del__(self):
        print(self.id, 'text deleted') ## extra id feature for proofing
        

class InputBox:
    
    inputBox_idIter = itertools.count() ## next count

    def __init__(self, x, y, w, h, text = '', color = defaultCOLOR, colorDiff = 50, font_name = '', editable = True):
        self.id = next(self.inputBox_idIter) ## id
# properties
        self.active = False
        self.dimensions = [x, y, w, h]
        self.text = text
        self.editable = editable
# format
        try:## the reason for this mess is because im making it so that the color of the input boxes are local so each input box doesnt have to be the same global color
            self.true_color = defaultCOLOR if color == defaultCOLOR else color
            self.inactive_color = self.get_inactiveColor(colorDiff / 100)## gets the difference in color in a multiplier
        except:
            print(self.id, 'error in __init__ #format')
        if len(color) != 3: ## incase a tuple like (21, 31) was entered this would fuck shit up
            print(self.id, 'error defining color')
        self.working_color = self.inactive_color
        try:
            self.font_name = None if font_name == '' else font_name
            self.font = self.get_font()
        except:
            print(self.id, 'error in __init__ #format')  
# get surface and rect
        
        self.render()

# handle uneditable box 
        if self.editable == False: ## overide active color
            self.inactive_color = self.true_color


    def get_font(self): ## returns apropriate fontsize for box height
        fontSize = defaultFONT_SIZE
        t_w, t_h = GetFontDimensions(self.font_name, fontSize)
        while t_h < (self.dimensions[3] ):
            fontSize += 1
            t_w, t_h = GetFontDimensions(self.font_name, fontSize)
        while t_h > (self.dimensions[3] ):
            fontSize -= 1
            t_w, t_h = GetFontDimensions(self.font_name, fontSize)
        return pygame.font.Font(self.font_name, fontSize)

    def get_inactiveColor(self, difference): 
        localC = list(self.true_color)
        try:
           for i in range(0, 3):
               if (localC[i] + (localC[i] * 2*difference)) > 255:
                   localC[i] = 255
               else:
                   localC[i] = int(localC[i] + (localC[i] * 2*difference))
        except IndexError:
            print(self.id, 'color tuple invalid')
       
        return tuple(localC)

    def render(self): ## define rectangle and txt_surface
        self.rect = pygame.Rect( self.dimensions[0], self.dimensions[1], self.dimensions[2], self.dimensions[3] )
        self.txt_surface = self.font.render(self.text, True, self.working_color)

    def handle_event(self, event):
        if self.editable == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##if the user clicks on the input box
                if self.rect.collidepoint(event.pos):
                    ## toggle the active var
                    self.active = not self.active
                else:
                    self.active = False
                ##change the current color of the input box
                self.working_color = self.true_color if self.active else self.inactive_color
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        self.get_text()## pointless but can be usefull if need text feedback on enter not here tho
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
        else:
            pass

    def update(self):
        ##reseize if the text is too long:
        self.rect.w = max(self.dimensions[2], self.txt_surface.get_width()+(self.dimensions[3] // 5))
        #rerendert the text
        self.txt_surface = self.font.render(self.text, True, self.working_color)

    def draw(self, screen):
        ##blit the text
        screen.blit(self.txt_surface, (self.rect.x+(self.dimensions[3] // 10), self.rect.y+ (self.dimensions[3] // 10)))
        ##blit the rect
        pygame.draw.rect(screen, self.working_color, self.rect, 2)
    def __del__(self):
        print(self.id, 'deleted input box')


class Button:

    button_idIter = itertools.count() ## next count

    def __init__(self, x, y, w, h, text = '', color = defaultCOLOR, colorDiff = 50, font_name = '', result = [], font_override = 0):
        self.id = next(self.button_idIter) ## id
# properties
        self.dimensions = [x, y, w, h]
        self.text = text
        self.clicked = False
        self.functions = result
        self.was_pressed = 0
# format
        try:## the reason for this mess is because im making it so that the color of the input boxes are local so each input box doesnt have to be the same global color
            self.true_color = defaultCOLOR if color == defaultCOLOR else color
            self.inactive_color = self.get_inactiveColor(colorDiff / 100)## gets the difference in color in a multiplier
        except:
            print(self.id, 'error in __init__ #format')
        if len(color) != 3: ## incase a tuple like (21, 31) was entered this would fuck shit up
            print(self.id, 'error defining color')
        self.working_color = self.inactive_color
        try:
            self.font_name = None if font_name == '' else font_name
            if font_override == 0:
                self.font = self.get_font()
            else:
                self.font = pygame.font.Font(self.font_name, font_override)
        except:
            print(self.id, 'error in __init__ #format')
# get surface and rect

        self.render()
        
    def get_font(self): ## returns apropriate fontsize for box height
        fontSize = defaultFONT_SIZE
        tempFont = pygame.font.Font(self.font_name, fontSize)
        tempSurface = tempFont.render(self.text, True, defaultCOLOR)
        tempSurface_rect = tempSurface.get_rect()
        t_w = tempSurface_rect.width
        while t_w < (self.dimensions[2]-8 ):## -8 is just the spacing
            fontSize += 1
            tempFont = pygame.font.Font(self.font_name, fontSize)
            tempSurface = tempFont.render(self.text, True, defaultCOLOR)
            tempSurface_rect = tempSurface.get_rect()
            t_w = tempSurface_rect.width
        while t_w > (self.dimensions[2]-8 ):## -8 is just the spacing
            fontSize -= 1
            tempFont = pygame.font.Font(self.font_name, fontSize)
            tempSurface = tempFont.render(self.text, True, defaultCOLOR)
            tempSurface_rect = tempSurface.get_rect()
            t_w = tempSurface_rect.width
        return pygame.font.Font(self.font_name, fontSize)

    def get_inactiveColor(self, difference): 
        localC = list(self.true_color)
        try:
           for i in range(0, 3):
               if (localC[i] + (localC[i] * 2*difference)) > 255:
                   localC[i] = 255
               else:
                   localC[i] = int(localC[i] + (localC[i] * 2*difference))
        except IndexError:
            print(self.id, 'color tuple invalid')
       
        return tuple(localC)

    def render(self): ## define rectangle and txt_surface
        self.rect = pygame.Rect( self.dimensions[0], self.dimensions[1], self.dimensions[2], self.dimensions[3] )
        self.txt_surface = self.font.render(self.text, True, self.working_color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            ##if the user clicks on the input box
            if self.rect.collidepoint(event.pos):
                ## toggle the active var
                self.clicked = not self.clicked
            else:
                self.clicked = False
            ##change the current color of the input box
            self.working_color = self.true_color if self.clicked else self.inactive_color
            if self.clicked:
                for function in self.functions:
                    function()
            self.was_pressed += 1
        else:
            self.working_color = self.inactive_color
            self.clicked = False

    def draw(self, screen):
        ##blit the text
        screen.blit(self.txt_surface, (self.rect.x + 4, self.rect.y+ ((self.rect.height - self.txt_surface.get_rect().height)//2)))
        ##blit the rect
        pygame.draw.rect(screen, self.working_color, self.rect, 2)

    def __del__(self):
        print(self.id, 'deleted input box')
