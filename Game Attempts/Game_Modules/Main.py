import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))

import Corridor





clock = pygame.time.Clock()
while True:
    if Corridor.section == "Corridoor":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and Corridor.Movement_Stopped == False:
                if event.key == pygame.K_SPACE and Corridor.player.sprite.jump_count == 0:
                    Corridor.player.sprite.gravity = -20
                    Corridor.player.sprite.jump_count += 1
                elif event.key == pygame.K_SPACE and Corridor.player.sprite.jump_count > 0 and Corridor.player.sprite.jump_count < 2:
                    Corridor.player.sprite.gravity = -15
                    Corridor.player.sprite.jump_count += 1
            if Corridor.king_text.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                Corridor.king_text.sprite.Remove_display = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Corridor.Screen.fill((0,0,0))
        Corridor.corridor_background.draw(Screen)
        Corridor.corridor_floor.draw(Screen)
        Corridor.corridor_door.draw(Screen)
        Corridor.corridor_platforms.draw(Screen)
        Corridor.player.draw(Screen)
        #Screen.blit(Corridor.text, (100,100))
        #Corridor.king_text.draw(Screen)
        Corridor.corridor_background.update()
        Corridor.corridor_floor.update() 
        Corridor.corridor_door.update()
        Corridor.player.update() 
        Corridor.king_text.update()
        #pygame.draw.rect(Corridor.Screen, "red", (100, 130, 300, 150))
        #pygame.draw.line(Corridor.Screen, "red", (640, 0), (640, 720), 5) # center line
    elif Corridor.section == "Main_Courtyard":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Corridor.Screen.fill((0,0,0))
    pygame.display.update()
    clock.tick(60)
