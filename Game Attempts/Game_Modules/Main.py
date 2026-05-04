import pygame
from sys import exit
import Corridor

pygame.init()
Screen = pygame.display.set_mode((1280,720))


clock = pygame.time.Clock()
while True:
    if Corridor.section == "Corridoor":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Corridor.player.sprite.jump_count == 0:
                    Corridor.player.sprite.gravity = -20
                    Corridor.player.sprite.jump_count += 1
                elif event.key == pygame.K_SPACE and Corridor.player.sprite.jump_count > 0 and Corridor.player.sprite.jump_count < 2:
                    Corridor.player.sprite.gravity = -15
                    Corridor.player.sprite.jump_count += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Corridor.Screen.fill((0,0,0))
        Corridor.corridor_background.draw(Screen)
        Corridor.corridor_floor.draw(Screen)
        Corridor.corridor_door.draw(Screen)
        Corridor.corridor_platforms.draw(Screen)
        Corridor.player.draw(Screen)
        Corridor.corridor_background.update()
        Corridor.corridor_floor.update() 
        Corridor.corridor_door.update()
        Corridor.player.update()  
        #pygame.draw.rect(Corridor.Screen, "red", (100, 100, 300, 450))
        #pygame.draw.line(Corridor.Screen, "red", (640, 0), (640, 720), 5) # center line
    elif Corridor.section == "Main_Courtyard":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Corridor.Screen.fill((0,0,0))
    pygame.display.update()
    clock.tick(60)
