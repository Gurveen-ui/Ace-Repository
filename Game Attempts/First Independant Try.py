import sys
import pygame

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image
        self.rect = self.image.get_rect()
    pass

Screen = pygame.display.set_mode((1800,1000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()