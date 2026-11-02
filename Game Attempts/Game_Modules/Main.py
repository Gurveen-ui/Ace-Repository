# import all nessesary things
import pygame, random
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))

import Global_Assets
import Overlay_Screen
import Start_Menu
import Corridor
import Courtyard
import End_Screen


# create needed variables
paused = False
overlay_screen = pygame.surface.Surface((1280,720))
overlay_screen.fill((0,0,0))
overlay_screen.set_alpha(180)
clock = pygame.time.Clock()
# pause display background function
def pause_display():
    if Global_Assets.section == "Corridor":
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
    elif Global_Assets.section == "Courtyard":
        Courtyard.Screen.fill((0,0,0))
        Courtyard.draw_courtyard(Screen, Courtyard.sand_tiles)
        Courtyard.background_attacks("paused")
        Courtyard.draw_enemies(Screen, Courtyard.enemies)
        Courtyard.player.draw(Screen)
        Courtyard.draw_front_attacks()
        Courtyard.draw_courtyard(Screen, Courtyard.wall_tiles)
        Courtyard.draw_wall_npc(Screen, Courtyard.wall_npc.sprite)
        Courtyard.draw_coins(Screen)
        Courtyard.draw_gui(Screen)
        Screen.blit(overlay_screen, (0,0))
        #Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.get_player_grid_pos(Courtyard.player.sprite)), False, (255,0,255)),(1280 - 110 ,720 - 120))
        Screen.blit(Global_Assets.Royal_Font.render(str(round(clock.get_fps())), False, (255,0,0)), (1280 - 90,720 - 50))

# reset all things after death
def reset_all():
    global paused
    paused = False
    Global_Assets.section = "Start_Menu"
    Corridor.initialise()
    Courtyard.initialise()

# main while loop
while True:
    # checks for pause button (esc)
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_ESCAPE] and (Global_Assets.section == "Corridor" or Global_Assets.section == "Courtyard") and Courtyard.player.sprite.player_dead == False:
        if paused == False:
            paused = True
            Global_Assets.pause_pressed = pygame.time.get_ticks()

    # paused section, higher priority than others      
    if paused == True:
        for event in pygame.event.get():
            if Overlay_Screen.start_button.sprite.Mouse_Sprite_Collision == True and event.type == pygame.MOUSEBUTTONDOWN:
                Global_Assets.pause_stopped = pygame.time.get_ticks()
                Global_Assets.paused_time += Global_Assets.pause_stopped - Global_Assets.pause_pressed
                paused = False
            elif Overlay_Screen.exit_button.sprite.Mouse_Sprite_Collision == True and event.type == pygame.MOUSEBUTTONDOWN:
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
    if Global_Assets.section == "Start_Menu":
        for event in pygame.event.get():
            if Start_Menu.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                Global_Assets.section = "Corridor"
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

    # corridor section, 2nd priority
    elif Global_Assets.section == "Corridor":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and Corridor.Movement_Stopped == False:
                if event.key == pygame.K_j:
                    Global_Assets.section = "Courtyard"
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

    # courtyard section, 3rd priorityd
    elif Global_Assets.section == "Courtyard":

        # event loop
        for event in pygame.event.get():

            # if the player is dead
            if Courtyard.player.sprite.player_dead == True:
                    if Overlay_Screen.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                        reset_all()
                    elif Overlay_Screen.exit_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit()

            # if the wall npc is talking
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

            # if the game is running as normal
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if Courtyard.player.sprite.swirl_attributes["active"] == False:
                            Courtyard.player.sprite.swirl_attributes["active"] = True
                            Courtyard.player.sprite.swirl_attributes["last_used"] = Courtyard.current_time
                            Courtyard.player.sprite.swirl_attributes["pos"] = Courtyard.player.sprite.rect.center - Courtyard.camera_offset
                    if event.key == pygame.K_q:
                        if Courtyard.player.sprite.wind_available == True:
                            Courtyard.player.sprite.wind_thrown = Courtyard.current_time
                            Courtyard.player.sprite.wind_available = False
                            surface = Courtyard.player.sprite.wind_projectile
                            Courtyard.player.sprite.wind_projectiles.append({"surface": surface, 
                                     "rect": surface.get_rect(center = Courtyard.player.sprite.rect.center - Courtyard.camera_offset), 
                                     "velocity": Courtyard.vector(Courtyard.player.sprite.velocity.x * 1.2, -17),
                                     "pos": Courtyard.player.sprite.rect.center - Courtyard.camera_offset, 
                                     "thrown": Courtyard.current_time})
                    if event.key == pygame.K_c:
                        if Courtyard.player.sprite.heal_attributes["active"] == False:
                            Courtyard.player.sprite.heal_attributes["active"] = True
                            Courtyard.player.sprite.heal_attributes["last_used"] = Courtyard.current_time
                            Courtyard.player.sprite.heal_attributes["pos"] = Courtyard.player.sprite.rect.center - Courtyard.camera_offset
                            Courtyard.player.sprite.health += Courtyard.player.sprite.heal_attributes["heal"]
                            x = random.randint(-30, 30)
                            y = random.randint(-30, 30)
                            Courtyard.Floating_numbers(Courtyard.player.sprite.heal_attributes["heal"], "green", Courtyard.vector(x/10, -5), Courtyard.vector((Courtyard.player.sprite.rect.centerx + x, Courtyard.player.sprite.rect.centery + y)))
                    if event.key == pygame.K_e:
                        if Courtyard.player.sprite.bean_available == True and Courtyard.enemies:
                            Courtyard.player.sprite.bean_thrown = Courtyard.current_time
                            Courtyard.player.sprite.bean_available = False
                            surface = Courtyard.player.sprite.bean_image
                            enemy_list = Courtyard.enemies.copy()
                            enemy = min(enemy_list, key=lambda enemy: Courtyard.h_value(enemy.grid_pos, Courtyard.player.sprite.grid_pos))
                            pixel_distance = Courtyard.find_pixel_distance(Courtyard.player.sprite.grid_pos, enemy.grid_pos)
                            velocity = Courtyard.vector(5,5)
                            if pixel_distance.x != 0 or pixel_distance.y != 0: velocity = (pixel_distance).normalize() * 10
                            Courtyard.player.sprite.bean_projectiles.append({"surface": surface, 
                                     "rect": surface.get_rect(center = Courtyard.player.sprite.rect.center - Courtyard.camera_offset), 
                                     "velocity": Courtyard.vector(velocity),
                                     "pos": Courtyard.player.sprite.rect.center - Courtyard.camera_offset, 
                                     "thrown": Courtyard.current_time})
                    if event.key == pygame.K_k:
                        Global_Assets.section = "End_Menu"
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
            Courtyard.draw_courtyard(Screen, Courtyard.sand_tiles)
            Courtyard.background_attacks("functional")
            Courtyard.draw_enemies(Screen, Courtyard.enemies)
            Courtyard.player.draw(Screen)
            #pygame.draw.rect(Screen, "red", (80,320,320,320), 5)
            Courtyard.draw_flashes(Screen)
            Courtyard.draw_front_attacks("functional")
            Courtyard.draw_courtyard(Screen, Courtyard.wall_tiles)
            Courtyard.draw_wall_npc(Screen, Courtyard.wall_npc.sprite)
            Courtyard.draw_health_markers(Screen, "functional")
            Courtyard.draw_coins(Screen, "functional")
            Courtyard.draw_gui(Screen)
            # Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.current_time // 1000), False, (0,0,0)),(1280 - 110 ,720 - 170))
            # Screen.blit(Global_Assets.Royal_Font.render(str(Courtyard.get_player_grid_pos(Courtyard.player.sprite)), False, (255,0,255)),(1280 - 110 ,720 - 120))
            Courtyard.wall_npc.update()

        # death display loop, displays only, doesnt call update functions
        else:
            Courtyard.draw_courtyard(Screen, Courtyard.sand_tiles)
            Courtyard.background_attacks("dead")
            Courtyard.draw_enemies(Screen, Courtyard.enemies)
            Courtyard.player.draw(Screen)
            Courtyard.draw_front_attacks()
            Courtyard.draw_courtyard(Screen, Courtyard.wall_tiles)
            Courtyard.draw_wall_npc(Screen, Courtyard.wall_npc.sprite)
            Courtyard.draw_coins(Screen)
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
    
    # end menu section, currently an else statement as end module is yet to be made
    elif Global_Assets.section == "End_Menu":
        for event in pygame.event.get():
            if End_Screen.start_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                reset_all()
            elif End_Screen.exit_button.sprite.Mouse_Sprite_Collision == True  and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Screen.fill((0,0,0))
        Screen.blit(End_Screen.Background, (0,0))
        Screen.blit(End_Screen.Board, (5,130))
        Screen.blit(End_Screen.Knight, End_Screen.Knight_Rect)
        End_Screen.start_button.draw(Screen)
        End_Screen.exit_button.draw(Screen)
        End_Screen.start_button.update()
        End_Screen.exit_button.update()

        
    Screen.blit(Global_Assets.Royal_Font.render(str(round(clock.get_fps())), False, (255,0,0)), (1280 - 140,720 - 50))
    pygame.display.update()
    clock.tick(60)