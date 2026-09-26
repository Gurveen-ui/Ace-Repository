# imports and initialises modules and creates display
import pygame
pygame.init()
Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("paused")

# death message for death screen 
death_message = pygame.image.load("Game Attempts\\Images\\Death Message Pixel.png").convert_alpha()

# button hover function, checks if mouse is hovering above a button and also changes the image size
def Button_Hover(Button):
        Mouse_x, Mouse_Y = pygame.mouse.get_pos()
        if Button.sprite.rect.collidepoint((Mouse_x, Mouse_Y)):
            Button.sprite.Mouse_Sprite_Collision = True
            Button.sprite.image = Button.sprite.Hover_Image
            Button.sprite.rect = Button.sprite.image.get_rect(center = Button.sprite.center)
        else:
            Button.sprite.Mouse_Sprite_Collision = False
            Button.sprite.image = Button.sprite.Still_Image
            Button.sprite.rect = Button.sprite.image.get_rect(center = Button.sprite.center)

# start button class
class Start_Button(pygame.sprite.Sprite):

    # initialising class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Start_Menu\\Start Button\\Start Pixel.png").convert_alpha()
        self.rect = self.image.get_rect(center = (640,400)) #+25
        self.Still_Image = self.image
        self.Mouse_Sprite_Collision = False
        self.Hover_Image = pygame.image.load("Game Attempts\\Images\\Start_Menu\\Start Button\\Start Pixel Hover.png").convert_alpha()
        self.center = self.rect.center
    
    # update method, calls button hover function
    def update(self):
        Button_Hover(start_button)

start_button = pygame.sprite.GroupSingle()
start_button.add(Start_Button())

# exit button class
class Exit_Button(pygame.sprite.Sprite):

    # initialising method
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Start_Menu\\Exit Button\\Exit Pixel.png").convert_alpha()
        self.rect = self.image.get_rect(center = (665,540)) #445,
        self.Still_Image = self.image
        self.Mouse_Sprite_Collision = False
        self.Hover_Image = pygame.image.load("Game Attempts\\Images\\Start_Menu\\Exit Button\\Exit Pixel Hover.png").convert_alpha()
        self.center = self.rect.center
    
    # update method, calls btton hover function
    def update(self):
        Button_Hover(exit_button)
        
exit_button = pygame.sprite.GroupSingle()
exit_button.add(Exit_Button())
