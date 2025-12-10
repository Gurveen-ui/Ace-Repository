import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Game")

GROUND_LEVEL = 592 # point at which gravity cant pull player below
LEFT_BOUND = 80 # x value player cant go past
RIGHT_BOUND = 1200 # x value player cant go past
DASH_DISTANCE = 300
SCREEN_WIDTH = Screen.get_width()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Player Resized.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (LEFT_BOUND,GROUND_LEVEL))

        self.gravity = 0
        self.jump_count = 0
        self.last_dash_time = -5000
        self.dash_cooldown = 5000

    def Movement(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_d] and keys[pygame.K_LCTRL]:
            if current_time - self.last_dash_time > self.dash_cooldown:
                self.rect.x += DASH_DISTANCE
                self.last_dash_time = current_time
            else:
                self.rect.x += 6
                sprite_group_movement(corridor_background, -1)
                sprite_group_movement(corridor_floor, -3)
        elif keys[pygame.K_d]:
            self.rect.x += 6
            sprite_group_movement(corridor_background, -1)
            sprite_group_movement(corridor_floor, -3)
        if keys[pygame.K_a] and keys[pygame.K_LCTRL]:
            if current_time - self.last_dash_time > self.dash_cooldown:
                self.rect.x -= DASH_DISTANCE
                self.last_dash_time = current_time
            else:
                self.rect.x -= 5
                sprite_group_movement(corridor_background, 1)
                sprite_group_movement(corridor_floor, 3)
        elif keys[pygame.K_a]:
            self.rect.x -= 5
            sprite_group_movement(corridor_background, 1)
            sprite_group_movement(corridor_floor, 3)
        if self.rect.right > RIGHT_BOUND:
            depth = self.rect.right - RIGHT_BOUND
            sprite_group_movement(corridor_background, int(((-depth / 3) * 2) + 1))
            sprite_group_movement(corridor_floor, -depth + 3)
            self.rect.right = RIGHT_BOUND
        elif self.rect.left < LEFT_BOUND:
            depth = LEFT_BOUND - self.rect.left
            sprite_group_movement(corridor_background, int(((depth / 3) * 2) + 1))
            sprite_group_movement(corridor_floor, depth - 3)
            self.rect.left = LEFT_BOUND

    
    def Apply_Gravity(self):
        self.rect.y += self.gravity
        self.gravity += 1
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.gravity = 0
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
        if self.rect.right <= 0:
            rightmost = max([bg.rect.right for bg in corridor_background])
            corridor_background.add(Corridor_Background(rightmost))
            self.kill()
        elif self.rect.left >= SCREEN_WIDTH:
            leftmost = min([bg.rect.left for bg in corridor_background])
            corridor_background.add(Corridor_Background(leftmost - self.rect.width))
            self.kill()

    def update(self):
        self.destroy()

corridor_background = pygame.sprite.Group()
corridor_background.add(Corridor_Background(-SCREEN_WIDTH), Corridor_Background(0), Corridor_Background(SCREEN_WIDTH))


class Corridor_Floor(pygame.sprite.Sprite):
    def __init__(self, left_x_pos):
        super().__init__()
        self.left_x_pos = left_x_pos #-1280, 0, 1280
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Floor.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (left_x_pos,720))

    def destroy(self):
        if self.rect.right <= 0:
            rightmost = max([flr.rect.right for flr in corridor_floor])
            corridor_floor.add(Corridor_Floor(rightmost))
            self.kill()
        elif self.rect.left >= SCREEN_WIDTH:
            leftmost = min([flr.rect.left for flr in corridor_floor])
            corridor_floor.add(Corridor_Floor(leftmost - self.rect.width))
            self.kill()

    def update(self):
        self.destroy()


corridor_floor = pygame.sprite.Group()
corridor_floor.add(Corridor_Floor(0),Corridor_Floor(SCREEN_WIDTH),Corridor_Floor(-SCREEN_WIDTH))

def sprite_group_movement(sprite_list, x_value):
    for sprite in sprite_list:
        sprite.rect.x = sprite.rect.x + x_value

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
    Screen.fill((0,0,0))
    corridor_background.draw(Screen)
    corridor_floor.draw(Screen)
    player.draw(Screen)
    corridor_background.update()
    corridor_floor.update() 
    player.update()  
    pygame.display.update()
    clock.tick(60)
