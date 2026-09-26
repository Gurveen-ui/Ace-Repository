# import all nessesary things
import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))

import Global_Assets
import Overlay_Screen
import Start_Menu
import Corridor
import Courtyard


# create needed variables
type = "Start_Menu"
paused = False
overlay_screen = pygame.surface.Surface((1280,720))
overlay_screen.fill((0,0,0))
overlay_screen.set_alpha(180)
clock = pygame.time.Clock()

# pause display background function
def pause_display():
    if type == "Corridor":
        Screen.fill((0,0,0))
        Corridor.corridor_background.draw(Screen)
        Corridor.corridor_floor.draw(Screen)
        Corridor.corridor_side_walls.draw(Screen)
        Corridor.corridor_door.draw(Screen)
        Corridor.corridor_platforms.draw(Screen)
        Corridor.corridor_signs.draw(Screen)
        Corridor.player.draw(Screen)
        Screen.blit(overlay_screen, (0,0))
        Screen.blit(Global_Assets.Royal_Font.render(str(round(clock.get_fps())), False, (255,0,0)), (1280 - 90,720 - 50))
    elif type == "Courtyard":
        Courtyard.Screen.fill((0,0,0))
        Courtyard.draw_courtyard(Screen)
        Courtyard.draw_wall_npc(Screen, Courtyard.wall_npc.sprite)
        Courtyard.player_attacks("paused")
        Courtyard.draw_enemies(Screen, Courtyard.enemies)
        Courtyard.player.draw(Screen)
        Courtyard.draw_gui(Screen)
        Screen.blit(overlay_screen, (0,0))
        Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.get_player_grid_pos(Courtyard.player.sprite)), False, (255,0,255)),(1280 - 110 ,720 - 120))
        Screen.blit(Global_Assets.Royal_Font.render(str(round(clock.get_fps())), False, (255,0,0)), (1280 - 90,720 - 50))

# reset all things after death
def reset_all():
    global paused, type
    paused = False
    Start_Menu.section = "Start_Menu"
    Corridor.section = "Corridor"
    Courtyard.section = "Courtyard"
    type = "Start_Menu"
    Corridor.initialise()
    Courtyard.initialise()

# main while loop
while True:
    # pause button (esc)
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_ESCAPE] and (type == "Corridor" or type == "Courtyard") and Courtyard.player.sprite.player_dead == False:
        if paused == False:
            paused = True

    # paused section, higher priority than others      
    if paused == True:
        for event in pygame.event.get():
            if Overlay_Screen.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                paused = False
            elif Overlay_Screen.exit_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pause_display()
        Overlay_Screen.start_button.draw(Screen)
        Overlay_Screen.exit_button.draw(Screen)
        Overlay_Screen.start_button.update()
        Overlay_Screen.exit_button.update()
        pygame.display.update()
        clock.tick(60)  
        continue

    # start menu section, 1st priority
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

    # corridor section, 2nd priority
    elif Corridor.section == "Corridor":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and Corridor.Movement_Stopped == False:
                if event.key == pygame.K_j:
                    Corridor.section = "Courtyard"
                if event.key == pygame.K_SPACE and Corridor.player.sprite.jump_count == 0:
                    Corridor.player.sprite.gravity = -20
                    Corridor.player.sprite.jump_count += 1
                elif event.key == pygame.K_SPACE and Corridor.player.sprite.jump_count > 0 and Corridor.player.sprite.jump_count < 2:
                    Corridor.player.sprite.gravity = -15
                    Corridor.player.sprite.jump_count += 1
            if Corridor.king_text.sprite.Mouse_Sprite_Collision == True and event.type == pygame.MOUSEBUTTONDOWN:
                Corridor.king_text.sprite.Remove_display = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Screen.fill((0,0,0))
        Corridor.corridor_background.draw(Screen)
        Corridor.corridor_side_walls.draw(Screen)
        Corridor.corridor_signs.draw(Screen)
        Corridor.corridor_door.draw(Screen)
        Corridor.corridor_floor.draw(Screen)
        Corridor.player.draw(Screen)
        Corridor.corridor_platforms.draw(Screen)
        Corridor.corridor_background.update()
        Corridor.corridor_floor.update() 
        Corridor.corridor_door.update()
        Corridor.player.update() 
        Corridor.king_text.update()
        Corridor.thought_bubble.update()
        #pygame.draw.rect(Corridor.Screen, "red", (70, 100, 400, 150))
        #pygame.draw.line(Corridor.Screen, "red", (640, 0), (640, 720), 5) # center line
        type = "Corridor"

    # courtyard section, 3rd priority
    elif Courtyard.section == "Courtyard":

        # event loop
        for event in pygame.event.get():
            if Courtyard.player.sprite.player_dead == True:
                    if Overlay_Screen.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                        reset_all()
                    elif Overlay_Screen.exit_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit()
            elif Courtyard.wall_npc.sprite.display_box == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Courtyard.wall_npc.sprite.text_paused == False: 
                        Courtyard.wall_npc.sprite.dialogue = list(Courtyard.wall_npc.sprite.current_text_constant)
                        Courtyard.wall_npc.sprite.text_paused = True
                    else:
                        Courtyard.wall_npc.sprite.dialogue_count += 1
                        Courtyard.wall_npc.sprite.line_counter = 0
                        Courtyard.wall_npc.sprite.text_counter = 0
                        Courtyard.wall_npc.sprite.pause_timer = 0
                        Courtyard.wall_npc.sprite.text_paused = False
                        Courtyard.wall_npc.sprite.dialogue.clear()
                        for lines in Courtyard.wall_npc.sprite.current_text_constant:
                            Courtyard.wall_npc.sprite.dialogue += [""]
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if Courtyard.player.sprite.swirl_attributes["active"] == False:
                            Courtyard.player.sprite.swirl_attributes["active"] = True
                            Courtyard.player.sprite.swirl_attributes["last_used"] = Courtyard.current_time
                            Courtyard.player.sprite.swirl_attributes["pos"] = Courtyard.player.sprite.rect.center - Courtyard.camera_offset
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    
        Screen.fill((0,0,0))

        # normal courtyard loop, while player is alive
        if Courtyard.player.sprite.player_dead == False:
            if Courtyard.Movement_Stopped == False:
                Courtyard.levels.update()
                Courtyard.player.update()
                if Courtyard.levels.wave_completed == False:
                    Courtyard.enemies.update()
            Courtyard.gui.update()
            Courtyard.draw_courtyard(Screen)
            Courtyard.draw_wall_npc(Screen, Courtyard.wall_npc.sprite)
            Courtyard.player_attacks("functional")
            Courtyard.draw_enemies(Screen, Courtyard.enemies)
            Courtyard.player.draw(Screen)
            #pygame.draw.rect(Screen, "red", (80,320,320,320), 5)
            Courtyard.draw_flashes(Screen)
            Courtyard.draw_gui(Screen)
            # Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.current_time // 1000), False, (0,0,0)),(1280 - 110 ,720 - 170))
            # Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.get_player_grid_pos(Courtyard.player.sprite)), False, (255,0,255)),(1280 - 110 ,720 - 120))
            Courtyard.wall_npc.update()
            type = "Courtyard"

        # death display loop, displays only, doesnt call update functions
        else:
            Courtyard.draw_courtyard(Screen)
            Courtyard.draw_wall_npc(Screen, Courtyard.wall_npc.sprite)
            Courtyard.player_attacks("dead")
            Courtyard.draw_enemies(Screen, Courtyard.enemies)
            Courtyard.player.draw(Screen)
            Courtyard.draw_gui(Screen)
            # Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.current_time // 1000), False, (0,0,0)),(1280 - 110 ,720 - 170))
            # Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.get_player_grid_pos(Courtyard.player.sprite)), False, (255,0,255)),(1280 - 110 ,720 - 120))
            Screen.blit(overlay_screen, (0,0))
            Screen.blit(Overlay_Screen.death_message, Overlay_Screen.death_message.get_rect(center = (620, 160)))
            Screen.blit(Global_Assets.Royal_Font.render("Now she is gone..", False, (80,30,30)),(10, 685))
            Overlay_Screen.start_button.draw(Screen)
            Overlay_Screen.exit_button.draw(Screen)
            Overlay_Screen.start_button.update()
            Overlay_Screen.exit_button.update()
            pygame.display.update()
        # if Courtyard.player.sprite.rect.colliderect(Courtyard.wall_npc.sprite.rect):
        #     pygame.draw.rect(Screen, "black", (80,320,320,320), 5)
        # pygame.draw.rect(Screen, "red", Courtyard.player.sprite.rect)
        # pygame.draw.rect(Screen, "red", Courtyard.wall_npc.sprite.rect)
    
    Screen.blit(Global_Assets.Royal_Font.render(str(round(clock.get_fps())), False, (255,0,0)), (1280 - 90,720 - 50))
    pygame.display.update()
    clock.tick(60)
