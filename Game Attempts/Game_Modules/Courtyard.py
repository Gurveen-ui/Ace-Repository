import pygame
import math
from pytmx.util_pygame import load_pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Courtyard")

TOP_BOUND = 80
BOTTOM_BOUND = 640
RIGHT_BOUND = 1200
LEFT_BOUND = 80

left_forcefield = 0
right_forcefield = 6400
top_forcefield = -2080
bottom_forcefield = 720

tmx_data = load_pygame("Game Attempts\\Tiled\\tmx\\Courtyard Map.tmx")



vector = pygame.math.Vector2
sprite_group = pygame.sprite.Group()


section = "Courtyard"

def sprite_group_movement(type, sprite_list, value):
     if type == "Horizontal":
         for sprite in sprite_list:
             sprite.rect.x = sprite.rect.x + int(round(value))
     if type == "Vertical":
         for sprite in sprite_list:
             sprite.rect.y = sprite.rect.y + int(round(value))

def Extract_Tiles(Class, Layer_Name, Group):
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "data") and layer.name == Layer_Name:
            for x, y, surf in layer.tiles():
                pos = (x * 80, (y * 80 - 2880))
                Class(pos, surf, Group)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Courtyard\\Player\\Knight Top Down Test.png").convert_alpha()
        self.Pre_rotation_image = pygame.image.load("Game Attempts\\Images\\Courtyard\\Player\\Knight Top Down Test.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (80, 520))
        self.position = vector(self.rect.center)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.ACCELERATION = 1
        self.FRICTION = -0.15
        self.at_horizontal_forcefield = False
        self.at_vertical_forcefield = False
        self.current_angle = 0
        self.rotation_speed = 10



    def Movement(self):
        self.acceleration = vector(0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_s]:
            self.acceleration.y = 0
        elif keys[pygame.K_w]:
            self.acceleration.y = -self.ACCELERATION
        elif keys[pygame.K_s]:
            self.acceleration.y = self.ACCELERATION
        else:
            self.acceleration.y = 0
        if keys[pygame.K_a] and keys[pygame.K_d]:
            self.acceleration.x = 0
        elif keys[pygame.K_a]:
            self.acceleration.x = -self.ACCELERATION
        elif keys[pygame.K_d]:
            self.acceleration.x = self.ACCELERATION
        else:
            self.acceleration.x = 0

    def Apply_Movement(self):
        self.velocity *= (1 + self.FRICTION)
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        if abs(self.velocity.y) < 0.1:
            self.velocity.y = 0
        if abs(self.acceleration.x) < 0.1:
            self.acceleration.x = 0
        if abs(self.acceleration.y) < 0.1:
            self.acceleration.y = 0
        self.position += self.velocity
        self.rect.center = self.position  
    
    def Check_Boundaries(self):
        global left_forcefield, right_forcefield, top_forcefield, bottom_forcefield
        tile_movement = self.velocity
        if self.rect.left -80 <= left_forcefield:
            self.rect.left = LEFT_BOUND
            self.at_forcefield = True
        elif self.rect.right + 80 >= right_forcefield:
            self.rect.right = RIGHT_BOUND
            self.at_forcefield = True
        else:
            self.at_horizontal_forcefield = False
        if self.rect.top -80 <= top_forcefield:
            self.rect.top = TOP_BOUND
            self.at_vertical_forcefield = True
        elif self.rect.bottom + 80 >= bottom_forcefield:
            self.rect.bottom = BOTTOM_BOUND
            self.at_vertical_forcefield = True
        else:
            self.at_vertical_forcefield = False
        if self.at_horizontal_forcefield == False:
             if self.rect.right > RIGHT_BOUND:
                sprite_group_movement("Horizontal", courtyard_tiles, -tile_movement.x)
                left_forcefield += -tile_movement.x
                right_forcefield += -tile_movement.x
                self.rect.right = RIGHT_BOUND
             elif self.rect.left < LEFT_BOUND:
                sprite_group_movement("Horizontal", courtyard_tiles, -tile_movement.x)
                left_forcefield += -tile_movement.x
                right_forcefield += tile_movement.x
                self.rect.left = LEFT_BOUND
        if self.at_vertical_forcefield == False:
             if self.rect.top < TOP_BOUND:
                sprite_group_movement("Vertical", courtyard_tiles, -tile_movement.y)
                top_forcefield += -tile_movement.y
                bottom_forcefield += -tile_movement.y
                self.rect.top = TOP_BOUND
             elif self.rect.bottom > BOTTOM_BOUND:
                sprite_group_movement("Vertical", courtyard_tiles, -tile_movement.y)
                top_forcefield += -tile_movement.y
                bottom_forcefield += -tile_movement.y
                self.rect.bottom = BOTTOM_BOUND
        self.position = self.rect.center

    def Forcefield_Updates(self):
        global left_forcefield, right_forcefield, top_forcefield, bottom_forcefield
        right_forcefield = max([tl.rect.right for tl in courtyard_tiles])
        left_forcefield = min([tl.rect.left for tl in courtyard_tiles])
        top_forcefield = min([tl.rect.top for tl in courtyard_tiles])
        bottom_forcefield = max([tl.rect.bottom for tl in courtyard_tiles])

    def rotate(self):
        if self.acceleration.length_squared() == 0: pass
        else:
            y_distance = -self.velocity.y
            x_distance = self.velocity.x
            target_angle = math.degrees(math.atan2(y_distance,x_distance)) - 90

            angle_diff = (target_angle - self.current_angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
            #print(angle)
            if abs(angle_diff) < self.rotation_speed:
                self.current_angle = target_angle
            else:
                self.current_angle += self.rotation_speed * (1 if angle_diff > 0 else -1)

            rotated_image = pygame.transform.rotate(self.Pre_rotation_image, self.current_angle)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.position)


    def update(self):
        self.Movement()
        self.Apply_Movement()
        self.Check_Boundaries()
        self.Forcefield_Updates()
        self.rotate()


player = pygame.sprite.GroupSingle()
player.add(Player())


class Courtyard_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface,Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)




courtyard_tiles = pygame.sprite.Group()
Extract_Tiles(Courtyard_Tile, "Sand", courtyard_tiles)
Extract_Tiles(Courtyard_Tile, "Walls", courtyard_tiles)




