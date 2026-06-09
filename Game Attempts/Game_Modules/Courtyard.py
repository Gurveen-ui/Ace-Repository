import pygame
from pytmx.util_pygame import load_pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Courtyard")

TOP_BOUND = 80
BOTTOM_BOUND = 640
RIGHT_BOUND = 1200
LEFT_BOUND = 80

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
        self.rect = self.image.get_rect(center = (640, 360))
        self.position = vector(self.rect.center)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.ACCELERATION = 1.4
        self.FRICTION = 0.2



    def Movement(self):
        self.acceleration = vector(0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_s]:
            self.acceleration.y = 0
        elif keys[pygame.K_w]:
            self.acceleration.y = -self.ACCELERATION
        elif keys[pygame.K_s]:
            self.acceleration.y = self.ACCELERATION
        if keys[pygame.K_a] and keys[pygame.K_d]:
            self.acceleration.x = 0
        elif keys[pygame.K_a]:
            self.acceleration.x = -self.ACCELERATION
        elif keys[pygame.K_d]:
            self.acceleration.x = self.ACCELERATION

    def Apply_Movement(self):
        self.acceleration.x -= self.velocity.x * self.FRICTION
        self.acceleration.y -= self.velocity.y * self.FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + (0.5 * self.acceleration)
        self.rect.center = self.position  
    
    def Check_Boundaries(self):
        if self.rect.right > RIGHT_BOUND:
            tile_movement = self.velocity
            sprite_group_movement("Horizontal", courtyard_tiles, -tile_movement.x)
            self.rect.right = RIGHT_BOUND
        elif self.rect.left < LEFT_BOUND:
            tile_movement = self.velocity
            sprite_group_movement("Horizontal", courtyard_tiles, -tile_movement.x)
            self.rect.left = LEFT_BOUND
        if self.rect.top < TOP_BOUND:
            tile_movement = self.velocity
            sprite_group_movement("Vertical", courtyard_tiles, -tile_movement.y)
            self.rect.top = TOP_BOUND
        elif self.rect.bottom > BOTTOM_BOUND:
            tile_movement = self.velocity
            sprite_group_movement("Vertical", courtyard_tiles, -tile_movement.y)
            self.rect.bottom = BOTTOM_BOUND
        self.position = self.rect.center

    def update(self):
        self.Movement()
        self.Apply_Movement()
        self.Check_Boundaries()


player = pygame.sprite.GroupSingle()
player.add(Player())


class Courtyard_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface,Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)

courtyard_tiles = pygame.sprite.Group()
Extract_Tiles(Courtyard_Tile, "Sand", courtyard_tiles)





