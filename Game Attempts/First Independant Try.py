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
PLATFORM_HEIGHT = 100
NORMAL_MOVEMENT_SPEED = 9
BACKGROUND_MOVEMENT_SPEED = 7
SCREEN_WIDTH = Screen.get_width()

left_forcefield = 0
right_forcefield = 8960 #7 floors length

player_still_image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Test Player Still.png").convert_alpha()

player_forward_spritesheet = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Player Forward Animation.png").convert_alpha()
player_forward_animation_list = []

player_backward_spritesheet = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Player Backward Animation.png").convert_alpha()
player_backward_animation_list = []

player_upward_spritesheet = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Player Upward Animation.png").convert_alpha()
player_upward_animation_list = []

player_downward_spritesheet = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Player Downward Animation.png").convert_alpha()
player_downward_animation_list = []

player_forward_running_spritesheet = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Player Forward Running Animation.png").convert_alpha()
player_forward_running_animation_list = []

player_backward_running_spritesheet = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Player\\Player Backward Running Animation.png").convert_alpha()
player_backward_running_animation_list = []

def get_image_from_sheet(list,sheet,width,height):
    sprite_count = 0
    spritesheet_width = sheet.get_rect().width
    for sprites in range(0, int(spritesheet_width / width)):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(sheet, (0,0), ((width * sprite_count,0),((width * sprite_count) + width ,height)))
        list.append(image)
        sprite_count += 1
    return list

player_forward_animation_list = get_image_from_sheet(player_forward_animation_list, player_forward_spritesheet, 128, 128)
player_backward_animation_list = get_image_from_sheet(player_backward_animation_list, player_backward_spritesheet, 128, 128)
player_upward_animation_list = get_image_from_sheet(player_upward_animation_list, player_upward_spritesheet, 128, 128)
player_downward_animation_list = get_image_from_sheet(player_downward_animation_list, player_downward_spritesheet, 128, 128)
player_forward_running_animation_list = get_image_from_sheet(player_forward_running_animation_list, player_forward_running_spritesheet, 128, 128)
player_backward_running_animation_list = get_image_from_sheet(player_backward_running_animation_list, player_backward_running_spritesheet, 128, 128)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_still_image
        self.rect = self.image.get_rect(bottomleft = (LEFT_BOUND,GROUND_LEVEL))

        self.gravity = 0
        self.jump_count = 0
        self.last_dash_time = -5000
        self.dash_cooldown = 5000
        self.previous_frame_bottom = self.rect.bottom
        self.at_forcefield = False
        self.horizontal_animation_count = 0
        self.vertical_animation_count = 0
        self.on_ground = False
        self.on_platform = False
        self.on_platform_name = self
        self.running = False



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
        if keys[pygame.K_a] and keys[pygame.K_LCTRL]:
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
            self.on_ground = True
            self.gravity = 0
            self.jump_count = 0
        else:
            self.on_ground = False

    def Platform_Collisions(self, platforms):
        keys = pygame.key.get_pressed()
        for sprite in platforms:
            if self.rect.colliderect(sprite.rect):
                if self.previous_frame_bottom <= sprite.rect.top:
                    self.rect.bottom = sprite.rect.top
                    self.gravity = 0
                    self.on_platform_name = sprite
                    self.on_platform = True
                    self.jump_count = 0
                    if keys[pygame.K_c] or keys[pygame.K_s]:
                        self.rect.bottom += 1
                        self.on_platform = False
        if self.rect.bottom != self.on_platform_name.rect.top:
            self.on_platform = False
            
                
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
                    self.Check_Boundaries(None)
                self.last_dash_time = self.current_time
            elif type == "Backward Dash":
                for dash_sixth in range(6):
                    sprite_group_movement(corridor_background, (DASH_DISTANCE / 18))
                    sprite_group_movement(corridor_floor, (DASH_DISTANCE / 6))
                    sprite_group_movement(corridor_platforms, (DASH_DISTANCE / 6))
                    left_forcefield += (DASH_DISTANCE / 6)
                    right_forcefield += (DASH_DISTANCE / 6)
                    self.Check_Boundaries(None)
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
    
    def Update_Animation(self):
        keys = pygame.key.get_pressed()
        if self.on_ground == False and self.on_platform == False:
            if self.gravity < 0:
                self.Vertical_Movement_Animation(player_upward_animation_list)
            elif self.gravity > 0:
                self.Vertical_Movement_Animation(player_downward_animation_list)
            else:
                self.running = False
                self.horizontal_animation_count = 0
                self.vertical_animation_count = 0
                self.image = player_still_image
        else:
            if keys[pygame.K_d] and keys[pygame.K_a]:
                self.running = False
                self.horizontal_animation_count = 0
                self.vertical_animation_count = 0
                self.image = player_still_image
            elif keys[pygame.K_d]:
                self.Horizontal_Movement_Animation(player_forward_animation_list, player_forward_running_animation_list)
            elif keys[pygame.K_a]:
                self.Horizontal_Movement_Animation(player_backward_animation_list, player_backward_running_animation_list)
            else:
                self.running = False
                self.horizontal_animation_count = 0
                self.vertical_animation_count = 0
                self.image = player_still_image
    
    def Horizontal_Movement_Animation(self, list, running_list):
        if self.image != list[(len(list) - 1)] and self.running == False:
            self.horizontal_animation_count += 0.2
            self.image = list[int(self.horizontal_animation_count)]
            if self.horizontal_animation_count >= (len(list) - 1):
                self.running = True
                self.horizontal_animation_count = 0
        if self.running == True:
            self.horizontal_animation_count += 0.3
            self.image = running_list[int(self.horizontal_animation_count)]
            if self.horizontal_animation_count >= (len(running_list) - 1):
                self.horizontal_animation_count = 0
    
    def Vertical_Movement_Animation(self, list):
        if self.image != list[(len(list) - 1)]:
            self.vertical_animation_count += 0.25
            self.image = list[int(self.vertical_animation_count)]
            if self.vertical_animation_count >= (len(list) - 1):
                self.vertical_animation_count = 0
        


    def update(self):
        self.Movement()
        self.Apply_Gravity()
        self.Platform_Collisions(corridor_platforms)
        self.Update_Animation()



player = pygame.sprite.GroupSingle()
player.add(Player())

class Corridor_Background(pygame.sprite.Sprite):
    def __init__(self, left_x_pos):
        super().__init__()
        self.left_x_pos = left_x_pos #-1280, 0, 1280
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Background Spritesheet.png").convert_alpha()
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
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Floor Spritesheet.png").convert_alpha()
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
    def __init__(self, topleft_x, topleft_y):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Platform.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (topleft_x, topleft_y))


corridor_platforms = pygame.sprite.Group()
corridor_platforms.add(Corridor_Platform(400,400), Corridor_Platform(800,325), Corridor_Platform(1200,250), Corridor_Platform(1800,375),
                       Corridor_Platform(2500,275), Corridor_Platform(2900,150), Corridor_Platform(3000,400), Corridor_Platform(3500,200), Corridor_Platform(4000,350))

class Corridor_Door(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:\\Blaze\\Holiday learning\\Python\\GitHub\\Ace-Repository\\Game Attempts\\Test Images\\Gate.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (592, 8450))

corridor_door = pygame.sprite.GroupSingle()
corridor_door.add(Corridor_Door())


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
    #pygame.draw.rect(Screen, "red", (100, 100, 300, 450))
    #pygame.draw.line(Screen, "red", (640, 0), (640, 720), 5) # center line
    pygame.display.update()
    clock.tick(60)
