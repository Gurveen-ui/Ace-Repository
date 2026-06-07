import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))

import Pause
import Start_Menu
import Corridor

type = "Start_Menu"
paused = False
pause_screen = pygame.surface.Surface((1280,720))
pause_screen.fill((0,0,0))
pause_screen.set_alpha(180)

def pause_display():
    if type == "Corridor":
        Screen.fill((0,0,0))
        Corridor.corridor_background.draw(Screen)
        Corridor.corridor_floor.draw(Screen)
        Corridor.corridor_door.draw(Screen)
        Corridor.corridor_platforms.draw(Screen)
        Corridor.player.draw(Screen)
        Screen.blit(pause_screen, (0,0))
    elif type == "Courtyard":
        Corridor.Screen.fill((0,0,0))
        Screen.blit(pause_screen, (0,0))
clock = pygame.time.Clock()

while True:
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_ESCAPE] and (type == "Corridor" or type == "Courtyard"):
        if paused == False:
            paused = True
            
    if paused == True:
        for event in pygame.event.get():
            if Pause.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                paused = False
            elif Pause.exit_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pause_display()
        Pause.start_button.draw(Screen)
        Pause.exit_button.draw(Screen)
        Pause.start_button.update()
        Pause.exit_button.update()
        pygame.display.update()
        clock.tick(60)  
        continue

    if Start_Menu.section == "Start_Menu":
        for event in pygame.event.get():
            if Start_Menu.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                Start_Menu.section = "Corridor"
                Corridor.start_time = pygame.time.get_ticks()
            elif Start_Menu.exit_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Screen.fill((0,0,0))
        Screen.blit(Start_Menu.Background, (0,0))
        Screen.blit(Start_Menu.AkaKnight, Start_Menu.Title_Rect)
        Screen.blit(Start_Menu.Knight, Start_Menu.Knight_Rect)
        #pygame.draw.rect(Start_Menu.Screen, "red", (800, 300, 80, 80))
        Start_Menu.start_button.draw(Screen)
        Start_Menu.exit_button.draw(Screen)
        Start_Menu.start_button.update()
        Start_Menu.exit_button.update()
        type = "Start_Menu"


    elif Corridor.section == "Corridor":
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
        Screen.fill((0,0,0))
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
        Corridor.thought_bubble.update()
        #pygame.draw.rect(Corridor.Screen, "red", (100, 130, 300, 150))
        #pygame.draw.line(Corridor.Screen, "red", (640, 0), (640, 720), 5) # center line
        type = "Corridor"
    elif Corridor.section == "Main_Courtyard":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Corridor.Screen.fill((0,0,0))
        type = "Courtyard"
    pygame.display.update()
    clock.tick(60)
