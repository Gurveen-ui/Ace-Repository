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

Test_Background = pygame.image.load("GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Background.png").convert_alpha()
test_surface = pygame.Surface((100,200))
test_surface.fill("red")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    print("Hi")
    Screen.blit(test_surface, (0,0))
    Screen.blit(Test_Background, (200,100))

    pygame.display.update()
    clock.tick(60)