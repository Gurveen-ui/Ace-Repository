import pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Corridor")

FLOOR_HEIGHT = 38

GROUND_LEVEL = 592 # point at which gravity cant pull player below
LEFT_BOUND = 80 # x value player cant go past
RIGHT_BOUND = 1200 # x value player cant go past
CENTER_LEFT_BOUND = 576
CENTER_RIGHT_BOUND = 704
LOWEST_PLATFORM = 450
PLATFORM_HEIGHT = 100
NORMAL_MOVEMENT_SPEED = 9
BACKGROUND_MOVEMENT_SPEED = 7
SCREEN_WIDTH = 1280
KING_TEXT = ["My Knight!!"," The princess is getting married today,"," you must put your life on the line"," to ensure nothing goes wrong."," Continue on to the courtyard!"]
PLAYER_THOUGHTS = ["The princess...                  ","I- I should go."]

left_forcefield = 0
right_forcefield = 5120 #4 floors length
current_time = 0
Movement_Stopped = False
Royal_Font = pygame.font.Font("Game Attempts\\Font\\citadel_of_blackrose\\Citadel of Blackrose.ttf", 30)
Royal_Font_Small = pygame.font.Font("Game Attempts\\Font\\citadel_of_blackrose\\Citadel of Blackrose.ttf", 20)
section = "Corridor"
start_time = 0

player_still_image = pygame.image.load("Game Attempts\\Images\\Player\\Test Player Resized.png").convert_alpha()

player_forward_spritesheet = pygame.image.load("Game Attempts\\Images\\Player\\Player Forward Animation.png").convert_alpha()
player_forward_animation_list = []

player_backward_spritesheet = pygame.image.load("Game Attempts\\Images\\Player\\Player Backward Animation.png").convert_alpha()
player_backward_animation_list = []

player_upward_spritesheet = pygame.image.load("Game Attempts\\Images\\Player\\Player Upward Animation.png").convert_alpha()
player_upward_animation_list = []

player_downward_spritesheet = pygame.image.load("Game Attempts\\Images\\Player\\Player Downward Animation.png").convert_alpha()
player_downward_animation_list = []

player_forward_running_spritesheet = pygame.image.load("Game Attempts\\Images\\Player\\Player Forward Running Animation.png").convert_alpha()
player_forward_running_animation_list = []

player_backward_running_spritesheet = pygame.image.load("Game Attempts\\Images\\Player\\Player Backward Running Animation.png").convert_alpha()
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

left_wall = pygame.image.load("Game Attempts\\Images\\Wall\\Left Wall Pixel.png").convert_alpha()
right_wall = pygame.image.load("Game Attempts\\Images\\Wall\\Right Wall Pixel.png").convert_alpha()


def sprite_group_movement(sprite_list, x_value):
    for sprite in sprite_list:
        sprite.rect.x = sprite.rect.x + x_value

def dialogue_producer(Box_class, Text_constant, Letter_Speed):
    if Box_class.Display_box == True:
        if Box_class.dialogue_counter % 1 == 0:
            if Box_class.dialogue[int(Box_class.line_counter)] == Text_constant[int(Box_class.line_counter)]:
                Box_class.line_counter += 1
                Box_class.dialogue_counter = 0
                if Box_class.line_counter >= len(Box_class.dialogue):
                    Box_class.text_paused = True
            if Box_class.line_counter <= len(Box_class.dialogue) - 1:
                Box_class.dialogue[Box_class.line_counter] += Text_constant[Box_class.line_counter][int(Box_class.dialogue_counter)]
        Box_class.dialogue_counter += Letter_Speed

def Display_Dialogue(Box_class, X_Distance, Y_Distance, Line_Spacing, Font):
    line_count = 0
    for line in Box_class.dialogue:
        text = Font.render(line, False, (0,0,0))
        for i in Box_class.dialogue:
            if line != Box_class.dialogue[line_count]:
                line_count += 1
        Screen.blit(text,(Box_class.rect.left + X_Distance , Box_class.rect.top + Y_Distance + (line_count* Line_Spacing)))
        line_count = 0
    if Box_class.text_paused == True:
        Box_class.pause_timer += 0.1

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
        if keys[pygame.K_d]:
            self.Normal_Movement("Forward")
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
                    if keys[pygame.K_c] or keys[pygame.K_s] and Movement_Stopped == False:
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
                    self.Foreground_Movement(-depth)
                    self.rect.right = CENTER_RIGHT_BOUND
            elif type == "Left":
                if self.rect.left < CENTER_LEFT_BOUND:
                    depth = CENTER_LEFT_BOUND - self.rect.left
                    sprite_group_movement(corridor_background, int(depth / 3))
                    self.Foreground_Movement(depth)
                    self.rect.left = CENTER_LEFT_BOUND
            else:
                if self.rect.right > RIGHT_BOUND:
                    depth = self.rect.right - RIGHT_BOUND
                    sprite_group_movement(corridor_background, int(-depth / 3))
                    self.Foreground_Movement(-depth)
                    self.rect.right = RIGHT_BOUND
                elif self.rect.left < LEFT_BOUND:
                    depth = LEFT_BOUND - self.rect.left
                    sprite_group_movement(corridor_background, int(depth / 3))
                    self.Foreground_Movement(depth)
                    self.rect.left = LEFT_BOUND
    
    def Normal_Movement(self, type):
        global left_forcefield, right_forcefield
        if left_forcefield < 0 and right_forcefield > 1280:
            if type == "Forward":
                if self.at_forcefield == False:
                    sprite_group_movement(corridor_background, -BACKGROUND_MOVEMENT_SPEED)
                    self.Foreground_Movement(-NORMAL_MOVEMENT_SPEED)
            elif type == "Backward":
                if self.at_forcefield == False:
                    sprite_group_movement(corridor_background, BACKGROUND_MOVEMENT_SPEED)
                    self.Foreground_Movement(NORMAL_MOVEMENT_SPEED)
        elif left_forcefield >= 0:
            if type == "Forward":
                self.rect.x += NORMAL_MOVEMENT_SPEED
                self.Check_Boundaries("Right")
            elif type == "Backward":
                self.rect.x -= NORMAL_MOVEMENT_SPEED
        elif right_forcefield <= 1280:
            if type == "Forward":
                self.rect.x += NORMAL_MOVEMENT_SPEED
            elif type == "Backward":
                self.rect.x -= NORMAL_MOVEMENT_SPEED
                self.Check_Boundaries("Left")
            
    
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
        
    def Gate_Check(self, Gates):
        global section
        keys = pygame.key.get_pressed()
        for gate in Gates:
            if self.rect.colliderect(gate.rect) and keys[pygame.K_e]:
                section = "Courtyard" 

    def Foreground_Movement(self, speed):
        global left_forcefield, right_forcefield
        sprite_group_movement(corridor_floor, speed)
        sprite_group_movement(corridor_door, speed)
        sprite_group_movement(corridor_platforms, speed)
        sprite_group_movement(corridor_side_walls, speed)
        left_forcefield += speed
        right_forcefield += speed


    def update(self):
        global current_time
        current_time = pygame.time.get_ticks()
        if Movement_Stopped == False:
            self.Movement()
            self.Update_Animation()
        self.Apply_Gravity()
        self.Platform_Collisions(corridor_platforms)
        self.Gate_Check(corridor_door)




player = pygame.sprite.GroupSingle()
player.add(Player())

class Corridor_Background(pygame.sprite.Sprite):
    def __init__(self, left_x_pos):
        super().__init__()
        self.left_x_pos = left_x_pos #-1280, 0, 1280
        self.image = pygame.image.load("Game Attempts\\Images\\Wall\\Wall Pixel.png").convert_alpha()
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
        self.image = pygame.image.load("Game Attempts\\Images\\Floor\\Floor Pixel.png").convert_alpha()
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
        self.image = pygame.image.load("Game Attempts\\Images\\Platform\\Platform.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (topleft_x, topleft_y))


corridor_platforms = pygame.sprite.Group()
corridor_platforms.add(Corridor_Platform(400,400), Corridor_Platform(800,325), Corridor_Platform(1200,250), Corridor_Platform(1800,375),
                       Corridor_Platform(2500,275), Corridor_Platform(2900,150), Corridor_Platform(3000,400), Corridor_Platform(3500,200), Corridor_Platform(4000,350))

class Corridor_Door(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Gate\\Gate Pixel.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (right_forcefield - 350,160))

corridor_door = pygame.sprite.GroupSingle()
corridor_door.add(Corridor_Door())

class King_Text(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Text Box\\Kings Text Box Large.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (10,700))
        self.Display_box = False
        self.dialogue = []
        for lines in KING_TEXT:
            self.dialogue += [""]
        self.dialogue_counter = 0
        self.line_counter = 0
        self.text_paused = False
        self.pause_timer = 0
        self.Box_Displayed = False
        self.Remove_display = False
        self.Mouse_Sprite_Collision = False
    
    def Display_Box(self):
        global Movement_Stopped
        if self.Display_box == True:
            Movement_Stopped = True
            king_text.draw(Screen)
        

    def update(self):
        global Movement_Stopped
        if self.Box_Displayed == False:
            if current_time >= start_time + 5000 and self.Remove_display == False:
                self.Display_box = True
            if self.pause_timer < 10 and self.Remove_display == False:
                self.Display_Box()
                if self.text_paused == False:
                    dialogue_producer(self, KING_TEXT, 0.5)
                Display_Dialogue(self, 370, 100, 35, Royal_Font)
            else:
                Movement_Stopped = False
                self.Display_box = False
                self.Box_Displayed = True
        Mouse_x, Mouse_Y = pygame.mouse.get_pos()
        if self.rect.collidepoint((Mouse_x, Mouse_Y)) and self.Display_box == True:
            self.Mouse_Sprite_Collision = True
        else:
            self.Mouse_Sprite_Collision = False

king_text = pygame.sprite.GroupSingle()
king_text.add(King_Text())

class Player_Thoughts(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Player Thoughts\\Thought Pixel.png").convert_alpha()
        self.rect = self.image.get_rect(bottomright = (player.sprite.rect.x,player.sprite.rect.y))
        self.Display_box = False
        self.dialogue = []
        for lines in PLAYER_THOUGHTS:
            self.dialogue += [""]
        self.dialogue_counter = 0
        self.line_counter = 0
        self.text_paused = False
        self.pause_timer = 0
        self.Box_Displayed = False
        self.Remove_display = False
    
    def Display_Box(self):
        if self.Display_box == True and self.Box_Displayed == False:
            self.rect.bottomright = ((player.sprite.rect.x + 30,player.sprite.rect.y + 30))
            thought_bubble.draw(Screen)
    
    def update(self):
        if self.Box_Displayed == False:
            if king_text.sprite.Box_Displayed == True and self.Remove_display == False:
                self.Display_box = True
            if self.pause_timer < 15 and self.Remove_display == False:
                self.Display_Box()
                if self.text_paused == False:
                    dialogue_producer(self, PLAYER_THOUGHTS, 0.25)
                Display_Dialogue(self, 60, 50, 25, Royal_Font_Small)
            else:
                self.Display_box = False
                self.Box_Displayed = True

thought_bubble = pygame.sprite.GroupSingle()
thought_bubble.add(Player_Thoughts())

class Corridor_Side_Wall(pygame.sprite.Sprite):
    def __init__(self, image, topleft_x, topleft_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = (topleft_x, topleft_y))

corridor_side_walls = pygame.sprite.Group()
corridor_side_walls.add(Corridor_Side_Wall(left_wall, -80, 0), Corridor_Side_Wall(right_wall, 5120, 0))