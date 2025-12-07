import pygame
from sys import exit

pygame.init()

#class Player(pygame.sprite.Sprite):
#    def __init__(self):
#        super().__init__()
#        self.image
#        self.rect = self.image.get_rect()
#    pass

Screen = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("Game")

Test_Background = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\Game Attempts\\Test Images\\Test Background.png").convert_alpha()


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Screen.blit(Test_Background, (0,0))
    print("hi")
    pygame.display.update()
    clock.tick(60)

