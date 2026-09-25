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
WALL_NPC_DIALOGUE_1 = ["Hey.. Welcome to my wall.  ","Y-You remember me right?","I'm the advice guy for the knights","And boy do I have advice for you."]
WALL_NPC_DIALOGUE_2 = ["Well as you know, ","The princess is getting married.","And we don't want ANYTHING","Getting in the way."]
WALL_NPC_DIALOGUE_3 = ["Though in all honestly","And dont tell anyone I said this,","when I last saw her, she...","looked somewhat... displeased"]
WALL_NPC_DIALOGUE_4 = ["But oh well, that has nothing","to do with.... us","We have only one duty as knights,","To follow the kings orders."]
WALL_NPC_DIALOGUE_5 = ["Enemies are gathering outside,","Any second now they will attack.","You must protect the princess","And her.... lover"]
WALL_NPC_DIALOGUE_6 = ["Here they come!!"]

wall_dialogues = [WALL_NPC_DIALOGUE_1, WALL_NPC_DIALOGUE_2, WALL_NPC_DIALOGUE_3, WALL_NPC_DIALOGUE_4, WALL_NPC_DIALOGUE_5, WALL_NPC_DIALOGUE_6]
tmx_data = load_pygame("Game Attempts\\Tiled\\tmx\\Courtyard Map Small.tmx")
current_time = 0
camera_offset = vector(0,0)
section = "Courtyard"
Movement_Stopped = False
enemy_spawns = []
grid = dict()
for x in range(80):
    for y in range(45):
        grid[(x,y)] = {"accessible": True,
                       "cost": 1 }

def initialise():
    global camera_offset, player, levels, wall_npc, gui, enemies
    camera_offset = vector(0,0)
    player = pygame.sprite.GroupSingle()
    player.add(Player())
    levels = Levels()
    wall_npc = pygame.sprite.GroupSingle()
    Extract_Tiles(Wall_NPC, "Wall_NPC", wall_npc, 80, "Object")
    gui = pygame.sprite.GroupSingle()
    gui.add(Gui())
    enemies = pygame.sprite.Group()


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
    
def draw_attacks(surface):
    player.sprite.swirl()

def draw_gui(Surface):
    pygame.draw.rect(Surface, (45,45,45), gui.sprite.total_health_rect)
    pygame.draw.rect(Surface, "black", gui.sprite.total_health_rect, 5)
    pygame.draw.rect(Surface, "red", gui.sprite.health_rect)
    pygame.draw.rect(Surface, "black", gui.sprite.health_rect, 5)

def draw_enemies(surface, enemy_group):
    for enemy in enemy_group:
        if enemy.rect.colliderect(surface.get_rect()):
            surface.blit(enemy.image, enemy.rect)

def draw_wall_npc(surface, object):
    offset = (round(camera_offset.x),round(camera_offset.y))
    screen_rect = object.world_rect.move(offset)
    if screen_rect.colliderect(surface.get_rect()):
        surface.blit(object.image, screen_rect)

def draw_flashes(surface):
    if player.sprite.hit_flash == True:
                    pygame.draw.rect(surface, "red", player.sprite.rect)

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
        self.max_health = 100
        self.health = 100
        self.player_dead = False
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
        self.hit_flash = False
        self.got_hit = False
        self.got_hit_time = 0

        self.swirl_image = pygame.image.load("Game Attempts\\Images\\Courtyard\\Player\\Swirl Pixel.png").convert_alpha()
        self.swirl_rect = self.swirl_image.get_rect(center = self.rect.center)
        self.swirl_attributes = {"active": False, "last_used": -10000, "damage": 20, "pos": (0,0)}

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

    def apply_damage(self):
        if self.got_hit == True and self.got_hit_time + 500 < current_time:
            self.got_hit = False

    def swirl(self):
        if self.swirl_attributes["active"] == True:
            if self.swirl_attributes["last_used"] + 500 > current_time:
                self.swirl_rect.center = self.swirl_attributes["pos"] + camera_offset
                Screen.blit(self.swirl_image, self.swirl_rect)
                for enemy in enemies:
                    if self.swirl_rect.colliderect(enemy.rect) and enemy.last_got_hit + 500 <= current_time:
                        enemy.health -= self.swirl_attributes["damage"]
                        enemy.last_got_hit = current_time
            if self.swirl_attributes["last_used"] + 2000 < current_time:
                self.swirl_attributes["active"] = False
        


    def update(self):
        global current_time
        self.hit_flash = False
        if self.health <= 0: self.player_dead = True
        current_time = pygame.time.get_ticks()
        self.Movement()
        self.Apply_Movement()
        self.Check_Boundaries()
        self.Rotate()
        self.apply_damage()

player = pygame.sprite.GroupSingle()
player.add(Player())

class Levels():
    def __init__(self):
        self.wave = 0
        self.wave_completed = False
        self.total_enemies = 10 + (self.wave * 2)
        self.completed_time = 0
        self.enemy_count = 0

    def update(self):
        if self.wave > 0:
            self.enemy_count = len(enemies)
            if self.enemy_count <= 0:
                self.completed_time += 1
                if self.completed_time > 1200:
                    self.wave += 1
                    self.total_enemies = 10 + (self.wave * 2)
                    for i in range(0, levels.total_enemies):
                        enemies.add(Courtyard_Enemies(random.choice(enemy_spawns)))
                    self.completed_time = 0
        



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
        self.text_box = pygame.image.load("Game Attempts\\Images\\Courtyard\\Wall NPC\\Text Box Pixel.png").convert_alpha()
        self.box_rect = self.text_box.get_rect(bottomleft = ((self.rect.centerx + 30, self.rect.centery - 50)))
        self.world_rect = self.rect
        self.display_box = False
        self.dialogue_count = 0
        self.current_text_constant = wall_dialogues[self.dialogue_count]
        self.dialogue = []
        for lines in self.current_text_constant:
            self.dialogue += [""]
        self.text_counter = 0
        self.line_counter = 0
        self.text_paused = False
        self.pause_timer = 0
        self.Box_Displayed = False
        self.Remove_display = False
        self.Mouse_Sprite_Collision = False

    def Display_Box(self):
        global Movement_Stopped
        if self.display_box == True:
            Movement_Stopped = True
            Screen.blit(self.text_box, self.box_rect)
        

    def update(self):
        global Movement_Stopped
        self.box_rect.bottomleft = ((self.rect.centerx + 30 + camera_offset.x, self.rect.centery - 50 + camera_offset.y))
        keys = pygame.key.get_pressed()
        if self.dialogue_count >= len(wall_dialogues) and self.Box_Displayed == False:
            Movement_Stopped = False
            self.display_box = False
            self.Box_Displayed = True
            levels.wave = 1
            for i in range(0, levels.total_enemies):
                enemies.add(Courtyard_Enemies(random.choice(enemy_spawns)))
        if self.Box_Displayed == False:
            self.current_text_constant = wall_dialogues[self.dialogue_count]
            if keys[pygame.K_e] and player.sprite.rect.colliderect(self.rect) and self.Remove_display == False:
                self.display_box = True
            if self.pause_timer < 20 and self.Remove_display == False:
                self.Display_Box()
                if self.text_paused == False:
                    Global_Assets.dialogue_producer(self, self.current_text_constant, 2.5)
                Global_Assets.Display_Dialogue(self, 72, 58, 20, Global_Assets.Royal_Font_Small, self.box_rect)
            else:
                self.dialogue_count += 1
                self.line_counter = 0
                self.text_counter = 0
                self.pause_timer = 0
                self.text_paused = False
                self.dialogue.clear()
                for lines in self.current_text_constant:
                    self.dialogue += [""]

wall_npc = pygame.sprite.GroupSingle()
Extract_Tiles(Wall_NPC, "Wall_NPC", wall_npc, 80, "Object")


class Gui(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.total_health_rect = pygame.rect.Rect(100,10,player.sprite.max_health *3,60)
        self.health_rect = pygame.rect.Rect(100,10,player.sprite.health *3,60)

    def update(self):
        self.total_health_rect = pygame.rect.Rect(100,10,player.sprite.max_health *3,60)
        self.health_rect = pygame.rect.Rect(100,10,player.sprite.health *3,60)


gui = pygame.sprite.GroupSingle()
gui.add(Gui())


class Courtyard_Enemies(pygame.sprite.Sprite):
    def __init__(self, world_pos):
        super().__init__()
        self.image = pygame.image.load("Game Attempts\\Images\\Courtyard\\Enemies\\Slimes\\Goof_Slime.png").convert_alpha()
        self.rect = self.image.get_rect(center = world_pos)
        self.world_rect = self.rect.copy()
        self.position = vector(self.rect.center)
        self.grid_pos = get_grid_pos(self.world_rect)
        self.max_health = 100
        self.health = 100
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.ACCELERATION = 0.3
        self.FRICTION = -0.05
        self.last_target_check = 0
        self.path = [self.grid_pos]
        self.current_target = self.grid_pos
        self.vector_distance = vector(0)
        self.damage = 5
        self.last_hit = 0
        self.last_got_hit = 0

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

    def Apply_Damage(self):
        screen_rect = self.world_rect.move(round(camera_offset.x),round(camera_offset.y))
        if screen_rect.colliderect(player.sprite.rect) and self.last_hit + 5000 <= current_time and player.sprite.got_hit == False:
            player.sprite.health -= self.damage
            player.sprite.hit_flash = True
            player.sprite.got_hit = True
            player.sprite.got_hit_time = current_time
            self.last_hit = current_time

    def death(self):
        if self.health <= 0:
            levels.enemy_count -= 1
            self.kill()

    def update(self):
        offset = (round(camera_offset.x),round(camera_offset.y))
        self.rect = self.world_rect.move(offset)
        self.grid_pos = get_grid_pos(self.world_rect)
        self.vector_distance = find_pixel_distance(self.grid_pos, self.current_target)
        self.Find_path()
        self.Update_Path()
        self.Movement()
        self.Apply_Movement()
        self.death()
        self.Apply_Damage()

enemies = pygame.sprite.Group()

