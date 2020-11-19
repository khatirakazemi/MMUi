import pygame
import sys
import csv
pygame.init()
screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = pygame.Color((100, 92, 108))
COLOR_ACTIVE = pygame.Color((66, 66, 66))
COLOR_GRID = pygame.Color((116, 116, 112))
FONT = pygame.font.Font(None, 32)

class TextBox: # takes x, y, w, h, text = ''

    def __init__(self, x, y, w, h, text = ''):##height doesnt affect this right now
        self.dimesions = [x, y, w, h]
        self.color = COLOR_ACTIVE
        self.text = text 
        
        self.font_size = (self.dimesions[3] // 8) * 7
        self.get_FONT()
        #self.TEXT_FONT = pygame.font.Font(None, self.font_size)

        self.txt_surface = self.TEXT_FONT.render(text, True, self.color)
        self.width, self.height = self.TEXT_FONT.size(text)
        self.txt_rect = self.txt_surface.get_rect(     center=((x + (self.width//2)), (y + (self.height//2)))     )
    
    def get_FONT(self):## bit slow and messy but no time rn    ########no functionality to change style
        max_height = self.dimesions[3] + 1
        while max_height + 1 > self.dimesions[3]:
            self.TEXT_FONT = pygame.font.Font(None, self.font_size)
            irellevant, max_height = self.TEXT_FONT.size(self.text)
            self.font_size -= 1
        self.font_size += 1

    def draw(self, screen):
        ##blit the text
        screen.blit(self.txt_surface, (self.txt_rect.x, self.txt_rect.y))

    def __del__(self):
        print('deleted text box')

class InputBoxUNEDITABLE: # takes x, y, w, h, text = ''

    def __init__(self, x, y, w, h, text = '', identifier = int):
        self.dimesions = [x, y, w, h]
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text 
        self.identity = identifier
        #print(self.text)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            ##if the user clicks on the input box
            if self.rect.collidepoint(event.pos):
                ## toggle the active var
                self.active = not self.active
            else:
                self.active = False
            ##change the current color of the input box
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
                


    def update(self):
        ##reseize if the text is too long:
        width = max(self.dimesions[2], self.txt_surface.get_width()+10)
        self.rect.w = width
        #rerendert the text
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        ##blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        ##blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return str(self.text)

    def __del__(self):
        print('deleted input box')

class InputBox: # takes x, y, w, h, text = ''

    def __init__(self, x, y, w, h, text = '', identifier = int):
        self.dimesions = [x, y, w, h]
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text 
        self.identity = identifier
        #print(self.text)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            ##if the user clicks on the input box
            if self.rect.collidepoint(event.pos):
                ## toggle the active var
                self.active = not self.active
            else:
                self.active = False
            ##change the current color of the input box
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.get_text()
                    #self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                


    def update(self):
        ##reseize if the text is too long:
        width = max(self.dimesions[2], self.txt_surface.get_width()+10)
        self.rect.w = width
        #rerendert the text
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        ##blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        ##blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return str(self.text)

    def __del__(self):
        print('deleted input box')

class Button: ##takes x, y, w, h, text = '', functions_to_call = [function] not [function()]

    def __init__(self, x, y, w, h,  text = '', functions_to_call = [] ):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.txt_rect = self.txt_surface.get_rect(     center=((x + (w//2)), (y + (h//2)))     )
        self.clicked = False
        self.functions = functions_to_call
        self.width, self.height = FONT.size(self.text)
        self.was_pressed = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked = False
            ##if the user clicks on the box
            if self.rect.collidepoint(event.pos):
                self.clicked = not self.clicked
            ## change the color of the input box
            self.color = COLOR_ACTIVE if self.clicked else COLOR_INACTIVE
            if self.clicked:
                for function in self.functions:
                    function()
            self.was_pressed +=1
        else:
            self.color = COLOR_INACTIVE

    def update(self):## maybe for future changes to the button itself
        pass

    def draw(self, screen):
        ##blit the text
        screen.blit(self.txt_surface, ((self.txt_rect.x, self.txt_rect.y)))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def __del__(self):
        print('deleted button')

class Grid: ## changes 10 to 12 so there is 12 columns - multiples

    def __init__(self, screen, x, y, w, h, items = [], process = ''):
        self.process = process
        self.properties = [x, y, w, h]
        self.height = (len(items) // 12) + 1##num of rows
        #print(bool(items))
        self.width = min((w // 12), (h / self.height)) if items else (w // 12) ## width of boxes
        screenw, screenh = screen.get_size()
        offset = screenw - (self.width * 12) ## so i can center the grid if y  is the prefered limit
        self.x = offset//2 if self.width != (w //12) and items else x
        self.y = y
        self.color = COLOR_GRID

        self.num_columns = 12

        self.items = items
        self.font_size = self.width // 2
        self.GRID_FONT = pygame.font.Font(None, int(self.font_size))
        if self.items:## if there is items using this to curcumvent an index issue that isnt really solvable , could make a better solution but not rn
            self.get_FONT()
       
    
    def get_FONT(self):## bit slow and messy but no time rn    ########no functionality to change style
        ######### in case of text moveing past box make font smaller
        max_width = self.width + 1
        while max_width + 10 > self.width:
            self.GRID_FONT = pygame.font.Font(None, int(self.font_size))
            max_width, irellevant = self.GRID_FONT.size(str(self.items[-1]))
            self.font_size -= 1
        self.font_size += 1

    def handle_grid(self, screen):
        self.new_x = self.x
        self.new_y = self.y
        for item in range(0, len(self.items)):
            
            self.rect = pygame.Rect(self.new_x, self.new_y, self.width , self.width)
            self.text = self.GRID_FONT.render(str(self.items[item]), True, self.color)
            self.text_rect = self.text.get_rect(     center=((self.new_x + self.width // 2), (self.new_y + self.width//2))     )## positions text

            self.draw(screen)
            self.new_x += self.width
            
            if (item + 1) % self.num_columns == 0and item > 0:
                
                ten = (item +1) // self.num_columns
                
                self.new_x = self.x
                self.new_y = self.y + (ten * self.width) 
                
                
    
    def update(self, newinput = []):
        Grid(self.properties[0], self.properties[1], self.properties[2], self.properties[3], items = newinput)
        del self

    def draw(self, screen):
        ##blit the text
        screen.blit(self.text, (self.text_rect.x, self.text_rect.y))
        ##blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)
        ##print('trying to draw')

    def __del__(self):
        if self.process != 'silent':
            print('deleted grid')
            
## to clear object just pop() it 

def writer(header, data, filename):
    with open(filename, 'w', newline = '') as csvfile:
        entry = csv.writer(csvfile)
        entry.writerow(header)
        for x in data:
            entry.writerow(x)

def Quit():
    print('quit')

def yo():
    print('yo')


def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(100, 100, 20, 32, text = 'hi')
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1]
    button1 = Button(200, 100, 140 , 32, text = 'QUIT', functions_to_call= [Quit])
    button2 = Button(200, 300, 140, 32, text = 'yo')
    buttons = []
    grid1 = Grid(screen, 10, 10, 620, 420, items = [1, 4, 5, 6, 78, 8, 7, 4, 3, 6, 7, 8, 3, 5, 7, 3, 6, 4, 6, 3, 2, 1, 0])
    grids = [grid1]
    done = False
     
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
            for button in buttons:
                button.handle_event(event)

        for box in input_boxes:
            box.update()
        for button in buttons:
            button.update()

        screen.fill((30, 30 , 30))
        for grid in grids:
            grid.handle_grid(screen)
        for box in input_boxes:
            box.draw(screen)
            ##print(box.text)
        for button in buttons:
            button.draw(screen)

        for button in buttons:
            
            del button
            

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()

