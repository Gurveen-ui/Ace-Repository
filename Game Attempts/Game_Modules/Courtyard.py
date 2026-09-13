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
PLAYER_SIZE = (67,67)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MAP_WIDTH = 80 * 80
MAP_HEIGHT = 80 * 45



tmx_data = load_pygame("Game Attempts\\Tiled\\tmx\\Courtyard Map.tmx")



vector = pygame.math.Vector2
camera_offset = vector(0,0)


section = "Courtyard"



def Extract_Tiles(Class, Layer_Name, Group, Side_length):
    for layer in tmx_data:
        if hasattr(layer, "data") and layer.name == Layer_Name:
            for x, y, surf in layer.tiles():
                world_pos = vector(x * Side_length, (y * Side_length - 2880)) # -200, -3000
                Class(world_pos, surf, Group)

def draw_courtyard(surface):
    offset = (round(camera_offset.x),round(camera_offset.y))
    for tile in courtyard_tiles:
        screen_rect = tile.world_rect.move(offset)
        if screen_rect.colliderect(surface.get_rect()):
            surface.blit(tile.image, screen_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Courtyard\\Player\\Knight Top Down Test.png").convert_alpha()
        self.Pre_rotation_image = self.image
        self.rect = self.image.get_rect(bottomleft = (90, 220))
        self.position = vector(self.rect.center)
        self.velocity = vector(0,0)
        self.prior_velocity_x = 0
        self.prior_velocity_y = 0
        self.acceleration = vector(0,0)
        self.ACCELERATION = 1
        self.FRICTION = -0.15
        self.at_horizontal_forcefield = False
        self.at_vertical_forcefield = False
        self.current_angle = 0
        self.rotation_speed = 10
        self.world_rect = self.rect



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
        self.velocity.x *= (1 + self.FRICTION)
        self.velocity.x += self.acceleration.x
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        if abs(self.acceleration.x) < 0.1:
            self.acceleration.x = 0
        self.position.x += self.velocity.x
        self.rect.center = self.position  
        self.Collision_Check("Horizontal",collision_tiles)
        
        self.velocity.y *= (1 + self.FRICTION)
        self.velocity.y += self.acceleration.y
        if abs(self.velocity.y) < 0.1:
            self.velocity.y = 0
        if abs(self.acceleration.y) < 0.1:
            self.acceleration.y = 0
        self.position.y += self.velocity.y
        self.rect.center = self.position
        self.Collision_Check("Vertical",collision_tiles)
    
    def Check_Boundaries(self):
        global camera_offset
        tile_movement = self.velocity
        if self.rect.right > RIGHT_BOUND:
            depth = self.rect.right - RIGHT_BOUND
            camera_offset.x -= depth
            self.rect.right = RIGHT_BOUND
        elif self.rect.left < LEFT_BOUND:
            depth = LEFT_BOUND - self.rect.left
            camera_offset.x += depth
            self.rect.left = LEFT_BOUND
        if self.rect.top < TOP_BOUND:
            depth = TOP_BOUND - self.rect.top
            camera_offset.y += depth
            self.rect.top = TOP_BOUND
        elif self.rect.bottom > BOTTOM_BOUND:
            depth = self.rect.bottom - BOTTOM_BOUND
            camera_offset.y -= depth
            self.rect.bottom = BOTTOM_BOUND

        camera_offset.x = max(SCREEN_WIDTH - MAP_WIDTH, min(0, camera_offset.x))
        camera_offset.y = max(0, min(2880, camera_offset.y))
        self.position = vector(self.rect.center)


    def Rotate(self):
        if self.acceleration.length_squared() == 0 or self.velocity.length_squared() == 0: pass
        else:
            y_distance = -self.prior_velocity_y
            x_distance = self.prior_velocity_x
            target_angle = math.degrees(math.atan2(y_distance,x_distance)) - 90

            angle_diff = (target_angle - self.current_angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
            if abs(angle_diff) < self.rotation_speed:
                self.current_angle = target_angle
            else:
                self.current_angle += self.rotation_speed * (1 if angle_diff > 0 else -1)

            rotated_image = pygame.transform.rotate(self.Pre_rotation_image, self.current_angle)
            self.image = rotated_image
            #self.rect = pygame.rect.Rect()
            self.rect = self.image.get_rect(center= self.position, size = PLAYER_SIZE)

    def Collision_Check(self, type, tiles):
        if type == "Horizontal": self.prior_velocity_x = self.velocity.x
        else: self.prior_velocity_y = self.velocity.y

        self.world_rect = self.rect.move(-round(camera_offset.x), -round(camera_offset.y))

        for tile in tiles:
            if not self.world_rect.colliderect(tile.world_rect):
                continue

            if type == "Horizontal":
                if self.velocity.x > 0:
                    self.world_rect.right = tile.world_rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0:
                    self.world_rect.left = tile.world_rect.right
                    self.velocity.x = 0
            elif type == "Vertical":
                if self.velocity.y > 0:
                    self.world_rect.bottom = tile.world_rect.top
                    self.velocity.y = 0
                elif self.velocity.y < 0:
                    self.world_rect.top = tile.world_rect.bottom
                    self.velocity.y = 0
        self.rect.topleft = (self.world_rect.left + round(camera_offset.x),
                             self.world_rect.top + round(camera_offset.y))
        self.position = vector(self.rect.center)
                    


    def update(self):
        self.Movement()
        self.Apply_Movement()
        self.Check_Boundaries()
        self.Rotate()
        #pygame.draw.rect(Screen, "red", self.rect)


player = pygame.sprite.GroupSingle()
player.add(Player())


class Courtyard_Tile(pygame.sprite.Sprite):
    def __init__(self, world_pos, surface,Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = world_pos)
        self.world_rect = self.image.get_rect(topleft = (round(world_pos.x), round(world_pos.y)))





courtyard_tiles = pygame.sprite.Group()
collision_tiles = pygame.sprite.Group()
Extract_Tiles(Courtyard_Tile, "Sand", courtyard_tiles, 80)
Extract_Tiles(Courtyard_Tile, "Walls", courtyard_tiles, 80)
Extract_Tiles(Courtyard_Tile, "Wall_Hit", collision_tiles, 80)




