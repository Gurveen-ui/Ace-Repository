import sys
import pygame

pygame.init()
Screen = pygame.display.set_mode((1800,1000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    