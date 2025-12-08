import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Player Resized.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100,592))

player = pygame.sprite.GroupSingle()
player.add(Player())



Test_Background = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Background Resized.png").convert_alpha()
Test_Floor = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Floor.png").convert_alpha()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    Screen.blit(Test_Background, (0,0))
    Screen.blit(Test_Floor, (0,592))
    player.draw(Screen)
    pygame.display.update()
    clock.tick(60)

