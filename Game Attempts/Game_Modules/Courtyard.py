import pygame
import math, random, Global_Assets
from pytmx.util_pygame import load_pygame
pygame.init()

Screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Courtyard")
vector = pygame.math.Vector2

TOP_BOUND = 80
BOTTOM_BOUND = 640
RIGHT_BOUND = 1200
LEFT_BOUND = 80
PLAYER_SIZE = (67,67)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MAP_WIDTH = 80 * 80
MAP_HEIGHT = 80 * 45

tmx_data = load_pygame("Game Attempts\\Tiled\\tmx\\Courtyard Map Small.tmx")
current_time = 0
camera_offset = vector(0,0)
section = "Courtyard"
enemy_spawns = []
grid = dict()
for x in range(80):
    for y in range(45):
        grid[(x,y)] = {"accessible": True,
                       "cost": 1 }


def Extract_Tiles(Class, Layer_Name, Group, Side_length, Type = None, List = None):
    if Type == "Object":
        for layer in tmx_data:
            if layer.name == Layer_Name:
                if Layer_Name == "Wall_NPC":
                    for obj in layer:
                        world_pos = vector(int(obj.x) , int(obj.y - 2880))
                        Class(world_pos, obj.image, Group)
                else:
                    for obj in layer:
                        world_pos = vector(int(obj.x + 40) , int(obj.y - 2880 + 40)) # -200, -3000
                        List.append(tuple(world_pos))
    else:
        for layer in tmx_data:
            if hasattr(layer, "data") and layer.name == Layer_Name:
                for x, y, surf in layer.tiles():
                    world_pos = vector(x * Side_length, (y * Side_length - 2880)) # -200, -3000
                    Class(world_pos, (x,y), surf, Group)
                    if Layer_Name == "Wall_Hit":
                        grid[(x, y)] = {"accessible": False,
                                        "cost": 1}

Extract_Tiles(None,"Spawnpoints", None, 80, "Object", enemy_spawns)

def draw_courtyard(surface):
    offset = (round(camera_offset.x),round(camera_offset.y))
    for tile in courtyard_tiles:
        screen_rect = tile.world_rect.move(offset)
        if screen_rect.colliderect(surface.get_rect()):
            surface.blit(tile.image, screen_rect)

def draw_enemies(surface, enemy_group):
    offset = (round(camera_offset.x),round(camera_offset.y))
    for enemy in enemy_group:
        screen_rect = enemy.world_rect.move(offset)
        if screen_rect.colliderect(surface.get_rect()):
            surface.blit(enemy.image, screen_rect)

def draw_wall_npc(surface, object):
    offset = (round(camera_offset.x),round(camera_offset.y))
    screen_rect = object.world_rect.move(offset)
    if screen_rect.colliderect(surface.get_rect()):
        surface.blit(object.image, screen_rect)

def get_player_grid_pos(object):
    world_rect = object.rect.center - camera_offset
    grid_x = int(world_rect.x / 80)
    grid_y = int((world_rect.y + 2880) / 80)
    return vector(grid_x, grid_y)

def get_grid_pos(world_rect):
    grid_x = int(vector(world_rect.center).x / 80)
    grid_y = int((vector(world_rect.center).y + 2880) / 80)
    return vector(grid_x, grid_y)

def h_value(start, target):
    start = vector(start)
    target = vector(target)
    h = math.sqrt((target.x - start.x)**2 + (target.y - start.y)**2)
    return h

def find_pixel_distance(start, target):
    x_distance = target.x * 80 - start.x * 80
    y_distance =  ((target.y * 80) + 2880) - ((start.y * 80) + 2880)
    return vector(x_distance, y_distance)

def A_Star(start, target):
    start = tuple((int(start.x),int(start.y)))
    target = tuple((int(target.x),int(target.y)))
    if start not in grid or target not in grid:
        return[]
    if not grid[start]["accessible"] or not grid[target]["accessible"]:
        return []
    open = [start]
    g_cost = {start: 0}
    f_cost = {start: h_value(start, target)}
    parent = {start: None}
    closed = set()
    while open:
        q = min(open, key=lambda pos: f_cost[pos])
        open.remove(q)
        for i in range(-1,2):
            for j in range(-1,2):
                child = (q[0] + i, q[1] + j)
                if child == q or child not in grid or not grid[child]["accessible"]:
                    continue
                if i != 0 and j != 0:
                        continue
                else: movement_cost = 1

                child_g = g_cost[q] + movement_cost
                child_h = h_value(child, target)
                child_cost = child_g + child_h

                if child in closed:
                    continue
                if child in g_cost and child_g >= g_cost[child]:
                    continue
                if child == target:
                    parent[child] = q
                    path = []
                    current = child
                    while current != None:
                        path.insert(0,current)
                        current = parent[current]
                    return path
                parent[child] = q
                g_cost[child] = child_g
                f_cost[child] = child_cost
                if child not in open:
                    open.append(child)
        closed.add(q)
    return[]




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
        self.current_angle = 0
        self.rotation_speed = 10
        self.grid_pos = get_player_grid_pos(self)

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
        self.grid_pos = get_player_grid_pos(self)

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
        global current_time
        current_time = pygame.time.get_ticks()
        self.Movement()
        self.Apply_Movement()
        self.Check_Boundaries()
        self.Rotate()
        #pygame.draw.rect(Screen, "red", self.rect)

player = pygame.sprite.GroupSingle()
player.add(Player())

class Levels():
    def __init__(self):
        self.wave = 0
        self.wave_completed = False

levels = Levels()

class Courtyard_Tile(pygame.sprite.Sprite):
    def __init__(self, world_pos, grid_pos, surface, Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = world_pos)
        self.grid_pos = grid_pos
        self.world_rect = self.image.get_rect(topleft = (round(world_pos.x), round(world_pos.y)))

courtyard_tiles = pygame.sprite.Group()
collision_tiles = pygame.sprite.Group()
Extract_Tiles(Courtyard_Tile, "Sand", courtyard_tiles, 80)
Extract_Tiles(Courtyard_Tile, "Walls", courtyard_tiles, 80)
Extract_Tiles(Courtyard_Tile, "Wall_Hit", collision_tiles, 80)

class Wall_NPC(pygame.sprite.Sprite):
    def __init__(self, world_pos, surface, Group):
        super().__init__(Group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = (world_pos))
        self.text_box = pygame.image.load("Game Attempts\Images\Text Box\Test Kings Text Box.png").convert_alpha()
        self.box_rect = self.text_box.get_rect(bottomleft = (10,700))
        self.world_rect = self.rect
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
            self.text_box.draw(Screen)
        

    def update(self):
        global Movement_Stopped
        keys = pygame.key.get_pressed()
        if self.Box_Displayed == False:
            Mouse_x, Mouse_Y = pygame.mouse.get_pos()
            if self.box_rect.collidepoint((Mouse_x, Mouse_Y)) and self.Display_box == True:
                self.Mouse_Sprite_Collision = True
            else:
                self.Mouse_Sprite_Collision = False
            if keys[pygame.K_e] and player.sprite.rect.colliderect(self.rect) and self.Remove_display == False:
                self.Display_box = True
            if self.pause_timer < 10 and self.Remove_display == False:
                self.Display_Box()
                if self.text_paused == False:
                    Global_Assets.dialogue_producer(self, KING_TEXT, 0.5)
                Global_Assets.Display_Dialogue(self, 370, 100, 35, Global_Assets.Royal_Font)
            else:
                Movement_Stopped = False
                self.Display_box = False
                self.Box_Displayed = True

wall_npc = pygame.sprite.GroupSingle()
Extract_Tiles(Wall_NPC, "Wall_NPC", wall_npc, 80, "Object")

class Courtyard_Enemies(pygame.sprite.Sprite):
    def __init__(self, world_pos):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Courtyard\\Enemies\\Slimes\\Goof_Slime.png").convert_alpha()
        self.rect = self.image.get_rect(center = world_pos)
        self.world_rect = self.rect.copy()
        self.position = vector(self.rect.center)
        self.grid_pos = get_grid_pos(self.world_rect)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.ACCELERATION = 0.3
        self.FRICTION = -0.05
        self.last_target_check = 0
        self.path = [self.grid_pos]
        self.current_target = self.grid_pos
        self.vector_distance = vector(0)

    def Movement(self):
        self.acceleration = vector(0,0)
        if self.vector_distance.y < -10:
            self.acceleration.y = -self.ACCELERATION
        elif self.vector_distance.y > 10:
            self.acceleration.y = self.ACCELERATION

        if self.vector_distance.x < -10:
            self.acceleration.x = -self.ACCELERATION
        elif self.vector_distance.x > 10:
            self.acceleration.x = self.ACCELERATION

    def Apply_Movement(self):
        self.velocity.x *= (1 + self.FRICTION)
        self.velocity.x += self.acceleration.x
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        if abs(self.acceleration.x) < 0.1:
            self.acceleration.x = 0
        self.position.x += self.velocity.x
        self.world_rect.center = self.position
        self.Collision_Check("Horizontal", collision_tiles)  
        
        self.velocity.y *= (1 + self.FRICTION)
        self.velocity.y += self.acceleration.y
        if abs(self.velocity.y) < 0.1:
            self.velocity.y = 0
        if abs(self.acceleration.y) < 0.1:
            self.acceleration.y = 0
        self.position.y += self.velocity.y
        self.world_rect.center = self.position
        self.Collision_Check("Vertical", collision_tiles)

    def Collision_Check(self, type, tiles):
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
        self.position = vector(self.world_rect.center)
        self.world_rect.center = self.position

    def Find_path(self):
        global current_time
        if h_value(player.sprite.grid_pos, self.grid_pos) < 10 and self.last_target_check + 500 < current_time:
            if not player.sprite.grid_pos == self.grid_pos:
                self.path = A_Star((self.grid_pos), (player.sprite.grid_pos))
                self.last_target_check = current_time
        else:
            if vector.length(self.vector_distance) < 2 and self.last_target_check + 10000 < current_time :
                target_x = self.grid_pos.x + random.randint(-10, 10)
                target_y = self.grid_pos.y + random.randint(-10, 10)
                new_path = A_Star((self.grid_pos), vector(target_x, target_y))
                if new_path:
                    self.path = new_path
                    self.last_target_check = current_time
                

    def Update_Path(self):
        if vector.length(self.vector_distance) < 2 and len(self.path) > 1:
            self.path.remove(self.path[0])
        self.current_target = vector(self.path[0])

    def update(self):
        self.grid_pos = get_grid_pos(self.world_rect)
        self.vector_distance = find_pixel_distance(self.grid_pos, self.current_target)
        self.Find_path()
        self.Update_Path()
        self.Movement()
        self.Apply_Movement()




# enemies = pygame.sprite.Group()
# for i in range(20):
#     enemies.add(Courtyard_Enemies(random.choice(enemy_spawns)))

