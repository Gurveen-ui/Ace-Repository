import pygame
from pytmx.util_pygame import load_pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Courtyard")

tmx_data = load_pygame("Game Attempts\\Tiled\\tmx\\Courtyard Map.tmx")


sprite_group = pygame.sprite.Group()


section = "Main_Courtyard"


class Courtyard_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface,Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)

for layer in tmx_data.visible_layers:
    if hasattr(layer, "data"):
        for x, y, surf in layer.tiles():
            pos = (x * 80, (y * 80 - 2880))
            Courtyard_Tile(pos, surf, sprite_group)



