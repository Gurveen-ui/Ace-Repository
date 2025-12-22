import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Game")

vector = pygame.math.Vector2

FLOOR_HEIGHT = 38

GROUND_LEVEL = 592 # point at which gravity cant pull player below
LEFT_BOUND = 80 # x value player cant go past
RIGHT_BOUND = 1200 # x value player cant go past
CENTER_LEFT_BOUND = 576
CENTER_RIGHT_BOUND = 704
DASH_DISTANCE = 300
LOWEST_PLATFORM = 450
NORMAL_MOVEMENT_SPEED = 9
BACKGROUND_MOVEMENT_SPEED = 7
SCREEN_WIDTH = Screen.get_width()

left_forcefield = 0
right_forcefield = 8960 #that is 7 floors

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Player Resized.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (LEFT_BOUND,GROUND_LEVEL))

        self.gravity = 0
        self.jump_count = 0
        self.last_dash_time = -5000
        self.dash_cooldown = 5000
        self.previous_frame_bottom = self.rect.bottom
        self.at_forcefield = False



    def Movement(self):
        self.previous_frame_bottom = self.rect.bottom
        keys = pygame.key.get_pressed()
        self.current_time = pygame.time.get_ticks()
        if keys[pygame.K_d] and keys[pygame.K_LCTRL]:
            if self.current_time - self.last_dash_time > self.dash_cooldown:
                self.Normal_Movement("Forward Dash")
            else:
                self.Normal_Movement("Forward")
        elif keys[pygame.K_d]:
            self.Normal_Movement("Forward")
        elif keys[pygame.K_a] and keys[pygame.K_LCTRL]:
            if self.current_time - self.last_dash_time > self.dash_cooldown:
                self.Normal_Movement("Backward Dash")
            else:
                self.Normal_Movement("Backward")
        elif keys[pygame.K_a]:
            self.Normal_Movement("Backward")
        self.Check_Boundaries(None)

    
    def Apply_Gravity(self):
        self.rect.y += self.gravity
        self.gravity += 1
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.gravity = 0
            self.jump_count = 0

    def Platform_Collisions(self, platforms):
        keys = pygame.key.get_pressed()
        for sprite in platforms:
            if self.rect.colliderect(sprite.rect):
                if self.previous_frame_bottom <= sprite.rect.top:
                    self.rect.bottom = sprite.rect.top
                    self.gravity = 0
                    self.jump_count = 0
                    if keys[pygame.K_c]:
                        self.rect.bottom += 1
                
    def Check_Boundaries(self, type):
        global left_forcefield, right_forcefield
        if self.rect.left <= left_forcefield:
            self.rect.left = left_forcefield
            self.at_forcefield = True
        elif self.rect.right >= right_forcefield:
            self.rect.right = right_forcefield
            self.at_forcefield = True
        else:
            self.at_forcefield = False
            if type == "Right":
                if self.rect.right > CENTER_RIGHT_BOUND:
                    depth = self.rect.right - CENTER_RIGHT_BOUND
                    sprite_group_movement(corridor_background, int(-depth / 3))
                    sprite_group_movement(corridor_floor, -depth)
                    sprite_group_movement(corridor_platforms, -depth)
                    left_forcefield += -depth
                    right_forcefield += -depth
                    self.rect.right = CENTER_RIGHT_BOUND
            elif type == "Left":
                if self.rect.left < CENTER_LEFT_BOUND:
                    depth = CENTER_LEFT_BOUND - self.rect.left
                    sprite_group_movement(corridor_background, int(depth / 3))
                    sprite_group_movement(corridor_floor, depth)
                    sprite_group_movement(corridor_platforms, depth)
                    left_forcefield += depth
                    right_forcefield += depth
                    self.rect.left = CENTER_LEFT_BOUND
            else:
                if self.rect.right > RIGHT_BOUND:
                    depth = self.rect.right - RIGHT_BOUND
                    sprite_group_movement(corridor_background, int(-depth / 3))
                    sprite_group_movement(corridor_floor, -depth)
                    sprite_group_movement(corridor_platforms, -depth)
                    left_forcefield += -depth
                    right_forcefield += -depth
                    self.rect.right = RIGHT_BOUND
                elif self.rect.left < LEFT_BOUND:
                    depth = LEFT_BOUND - self.rect.left
                    sprite_group_movement(corridor_background, int(depth / 3))
                    sprite_group_movement(corridor_floor, depth)
                    sprite_group_movement(corridor_platforms, depth)
                    left_forcefield += depth
                    right_forcefield += depth
                    self.rect.left = LEFT_BOUND
    
    def Normal_Movement(self, type):
        global left_forcefield, right_forcefield
        if left_forcefield < 0 and right_forcefield > 1280:
            if type == "Forward":
                if self.at_forcefield == False:
                    sprite_group_movement(corridor_background, -BACKGROUND_MOVEMENT_SPEED)
                    sprite_group_movement(corridor_floor, -NORMAL_MOVEMENT_SPEED)
                    sprite_group_movement(corridor_platforms, -NORMAL_MOVEMENT_SPEED)
                    left_forcefield -= NORMAL_MOVEMENT_SPEED
                    right_forcefield -= NORMAL_MOVEMENT_SPEED
            elif type == "Backward":
                if self.at_forcefield == False:
                    sprite_group_movement(corridor_background, BACKGROUND_MOVEMENT_SPEED)
                    sprite_group_movement(corridor_floor, NORMAL_MOVEMENT_SPEED)
                    sprite_group_movement(corridor_platforms, NORMAL_MOVEMENT_SPEED)
                    left_forcefield += NORMAL_MOVEMENT_SPEED
                    right_forcefield += NORMAL_MOVEMENT_SPEED
            elif type == "Forward Dash":
                for dash_sixth in range(6):
                    sprite_group_movement(corridor_background, -(DASH_DISTANCE / 18))
                    sprite_group_movement(corridor_floor, -(DASH_DISTANCE / 6))
                    sprite_group_movement(corridor_platforms, -(DASH_DISTANCE / 6))
                    left_forcefield -= (DASH_DISTANCE / 6)
                    right_forcefield -= (DASH_DISTANCE / 6)
                self.last_dash_time = self.current_time
            elif type == "Backward Dash":
                for dash_sixth in range(6):
                    sprite_group_movement(corridor_background, (DASH_DISTANCE / 18))
                    sprite_group_movement(corridor_floor, (DASH_DISTANCE / 6))
                    sprite_group_movement(corridor_platforms, (DASH_DISTANCE / 6))
                    left_forcefield += (DASH_DISTANCE / 6)
                    right_forcefield += (DASH_DISTANCE / 6)
                    self.last_dash_time = self.current_time
        elif left_forcefield >= 0:
            if type == "Forward":
                self.rect.x += NORMAL_MOVEMENT_SPEED
                self.Check_Boundaries("Right")
            elif type == "Backward":
                self.rect.x -= NORMAL_MOVEMENT_SPEED
            elif type == "Forward Dash":
                for dash_sixth in range(6):
                    self.rect.x += (DASH_DISTANCE / 6)
                    self.Check_Boundaries("Right")
                self.last_dash_time = self.current_time
            elif type == "Backward Dash":
                for dash_sixth in range(6):
                    self.rect.x -= (DASH_DISTANCE / 6)
                    self.Check_Boundaries(None)
                self.last_dash_time = self.current_time
        elif right_forcefield <= 1280:
            if type == "Forward":
                self.rect.x += NORMAL_MOVEMENT_SPEED
            elif type == "Backward":
                self.rect.x -= NORMAL_MOVEMENT_SPEED
                self.Check_Boundaries("Left")
            elif type == "Forward Dash":
                for dash_sixth in range(6):
                    self.rect.x += (DASH_DISTANCE / 6)
                    self.Check_Boundaries(None)
                self.last_dash_time = self.current_time
            elif type == "Backward Dash":
                for dash_sixth in range(6):
                    self.rect.x -= (DASH_DISTANCE / 6)
                    self.Check_Boundaries("Left")
                self.last_dash_time = self.current_time


    def update(self):
        self.Movement()
        self.Apply_Gravity()
        self.Platform_Collisions(corridor_platforms)



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

class Corridor_Platform(pygame.sprite.Sprite):
    def __init__(self, bottomleft_x, bottomleft_y):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Test Platform.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (bottomleft_x, bottomleft_y))

corridor_platforms = pygame.sprite.Group()
corridor_platforms.add(Corridor_Platform(400,450), Corridor_Platform(800,375), Corridor_Platform(1200,300), Corridor_Platform(1800,425),
                       Corridor_Platform(2500,325), Corridor_Platform(2900,200), Corridor_Platform(3000,450), Corridor_Platform(3500,250), Corridor_Platform(4000,400))

def sprite_group_movement(sprite_list, x_value):
    for sprite in sprite_list:
        sprite.rect.x = sprite.rect.x + x_value

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.jump_count == 0:
                    player.sprite.gravity = -20
                    player.sprite.jump_count += 1
                elif event.key == pygame.K_SPACE and player.sprite.jump_count > 0 and player.sprite.jump_count < 2:
                    player.sprite.gravity = -15
                    player.sprite.jump_count += 1
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    Screen.fill((0,0,0))
    corridor_background.draw(Screen)
    corridor_floor.draw(Screen)
    corridor_platforms.draw(Screen)
    player.draw(Screen)
    corridor_background.update()
    corridor_floor.update() 
    player.update()  
    #pygame.draw.line(Screen, "red", (640, 0), (640, 720), 5) # center line
    pygame.display.update()
    clock.tick(60)
