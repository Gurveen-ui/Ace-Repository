import pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Start Menu")

section = "Start_Menu"

Background = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Images\\Start_Menu\\Background Pixel.png").convert_alpha()

class Start_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Images\\Start_Menu\\Start Button\\Start Pixel.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (200,200))

start_button = pygame.sprite.GroupSingle()
start_button.add(Start_Button())