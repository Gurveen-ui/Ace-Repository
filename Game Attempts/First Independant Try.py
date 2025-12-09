import pygame
import threading
import time
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Game")

GROUND_LEVEL = 592
LEFT_BOUND = 80
RIGHT_BOUND = 1200
DASH_DISTANCE = 300

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Player Resized.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (80,592))

        self.gravity = 0
        self.jump_count = 0
        self.last_dash_time = 0
        self.dash_cooldown = 5000

    def Movement(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_d] and keys[pygame.K_LCTRL]:
            if current_time - self.last_dash_time > self.dash_cooldown_duration:
                self.rect.x += 300
                self.last_dash_time = current_time
            else:
                self.rect.x += 6
        elif keys[pygame.K_d]:
            self.rect.x += 6
        if keys[pygame.K_a] and keys[pygame.K_LCTRL]:
            if current_time - self.last_dash_time > self.dash_cooldown_duration:
                self.rect.x -= 300
                self.last_dash_time = current_time
            else:
                self.rect.x -= 5
        elif keys[pygame.K_a]:
            self.rect.x -= 5
        if self.rect.right > 1200:
            corridor_background_movement(corridor_background, -4)
            corridor_floor_movement(corridor_floor, -6)
            self.rect.right = 1200
        elif self.rect.left < 80:
            corridor_background_movement(corridor_background, 4)
            corridor_floor_movement(corridor_floor, 6)
            self.rect.left = 80

    def Dash_Countdown(self):
        time.sleep(5)
        self.dash_cooldown = False

    
    def Apply_Gravity(self):
        self.rect.y += self.gravity
        self.gravity += 1
        if self.rect.bottom >= 592:
            self.rect.bottom = 592
            self.jump_count = 0



    def update(self):
        self.Movement()
        self.Apply_Gravity()


player = pygame.sprite.GroupSingle()
player.add(Player())

class Corridor_Background(pygame.sprite.Sprite):
    def __init__(self, left_x_pos):
        super().__init__()
        self.left_x_pos = left_x_pos #-1280, 0, 1280
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Background Resized.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (left_x_pos,0))

    def destroy(self):
        if self.rect.right <= -1280:
            corridor_background.add(Corridor_Background(1280))
            self.kill()
        elif self.rect.left >= 2560:
            corridor_background.add(Corridor_Background(-1280))
            self.kill()

    def update(self):
        self.destroy()

corridor_background = pygame.sprite.Group()
corridor_background.add(Corridor_Background(0))

def corridor_background_movement(background_list, movement_direction):
    for background in background_list:
        background.rect.x = background.rect.x + movement_direction

class Corridor_Floor(pygame.sprite.Sprite):
    def __init__(self, left_x_pos):
        super().__init__()
        self.left_x_pos = left_x_pos #-1280, 0, 1280
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Floor.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (left_x_pos,720))

    def destroy(self):
        if self.rect.right <= -1280:
            corridor_floor.add(Corridor_Floor(1280))
            self.kill()
        elif self.rect.left >= 2560:
            corridor_floor.add(Corridor_Floor(-1280))
            self.kill()

    def update(self):
        self.destroy()


corridor_floor = pygame.sprite.Group()
corridor_floor.add(Corridor_Floor(0),Corridor_Floor(1280),Corridor_Floor(-1280))

def corridor_floor_movement(floor_list, movement_direction):
    for floor in floor_list:
        floor.rect.x = floor.rect.x + movement_direction

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.jump_count == 0:
                    player.sprite.gravity = -20
                    player.sprite.jump_count = 1
                elif event.key == pygame.K_SPACE and player.sprite.jump_count == 1:
                    player.sprite.gravity = -15
                    player.sprite.jump_count = 2
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    corridor_background.draw(Screen)
    corridor_floor.draw(Screen)
    player.draw(Screen)
    player.update()
    corridor_background.update()
    corridor_floor.update()    
    pygame.display.update()
    clock.tick(60)
