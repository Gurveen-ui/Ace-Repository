import pygame
from pytmx.util_pygame import load_pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Courtyard")

tmx_data = load_pygame("Game Attempts\\Tiled\\tmx\\Courtyard Map.tmx")


sprite_group = pygame.sprite.Group()


section = "Courtyard"

def sprite_group_movement(type, sprite_list, value):
    # if type == "Horizontal":
    #     for sprite in sprite_list:
    #         sprite.rect.x = sprite.rect.x + value
    # if type == "Vertical":
    #     for sprite in sprite_list:
    #         sprite.rect.y = sprite.rect.y + value
    pass

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

    def Movement(self):
        self.previous_frame_bottom = self.rect.bottom
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pass
        elif keys[pygame.K_a]:
            pass
        elif keys[pygame.K_s]:
            pass
        elif keys[pygame.K_d]:
            pass

    def update(self):
        self.Movement()

player = pygame.sprite.GroupSingle()
player.add(Player())


class Courtyard_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface,Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)

courtyard_tiles = pygame.sprite.Group()
Extract_Tiles(Courtyard_Tile, "Sand", courtyard_tiles)





