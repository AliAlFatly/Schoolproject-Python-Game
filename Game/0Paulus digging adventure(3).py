import pygame
import random
import sys
from os import path
import time

WIDTH = 1200
HEIGHT = 800
FPS = 60
ikFPS = 60
FONT_NAME = "arial"
ikFONT_NAME = pygame.font.match_font('arial')



#player properties
player_acc = 10
player_friction = 0.3
player_gravity = 30
player_jump = 220
enemy_speed = 15
x_boundry = 25
y_boundry = 75
Boundries = 1
TILESIZE = 25
TILEBUTTONS = 50
aafFalling = 30
vjFalling = 10
remainder = 9
rekenwaard = 1
aafHP = 100
aafHS_FILE  = "aafHS.txt"
chHS_FILE = 'chHS.txt'

aafBackGround = pygame.image.load('aafBackGround.png')
player_speed = 25
ch_speed = 10
chCarOne_speed = 5
chCarTwo_speed = 7
chCarThree_speed = 5
chCarFour_speed = 2.5

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)
randomcolor = (77,77,77)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
BGCOLOR = BROWN

game_title = "Paulus Forest Adventure"
vec = pygame.math.Vector2
vj_title = "Paulus Fruity Adventure"
ch_title = "Paulus Rushing Adventure"

ikTITLE = "Paulus' Forest Adventure"

#IK settings:
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
IKTILESIZE = 50
GRIDWIDTH = WIDTH / IKTILESIZE
GRIDHEIGHT = HEIGHT / IKTILESIZE

WALL_IMG = 'tree_1_0.png'

# Player settings
ikPLAYER_HEALTH = 100
ikPLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
ikPLAYER_IMG = 'mainCharacter_1.png'
ikPLAYER_HIT_RECT = pygame.Rect(0, 0, 40, 40)
ikPLAYER_LIVES = 3

#Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 1000
BULLET_LIFETIME = 50
BULLET_RATE = 500
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'boswachter_0.png'
MOB_SPEED = 150
MOB_HIT_RECT = pygame.Rect(0, 0, 40, 40)
MOB_HEALTH = 50
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 200

# Currency settings
COIN_IMG = 'coin.png'

COIN_WORTH = 10
CUM_COIN_COUNT = 0

# Background settings
BG_IMG = 'background.png'

# Life Settings
LIFE_IMG = 'life.png'

# wall settings
WALL_HEALTH = 40
#game_folder = sys.path.dirname(__file__)
#img_folder = sys.path.join(game_folder, "imagename")
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#game ali start here:
class aafMAP:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class aafCamera():
        def __init__(self, width, height):
            self.aafCamera = pygame.Rect(0 ,0 ,width ,height)
            self.width = 401 * 25
            self.height = 60 * 25

        def apply(self, entity):
            return entity.rect.move(self.aafCamera.topleft)

        def update(self, target):
            x = - target.rect.x + int(WIDTH / 2)
            y = - target.rect.y + int(HEIGHT / 2)

            #limit scrolling to map size
            x = min(0, x) #left
            y = min(0, y) #top
            x = max(-(self.width - WIDTH), x) #right
            y = max(-(self.height - HEIGHT), y) #bottom
            self.aafCamera = pygame.Rect(x, y, self.width, self.height)

class aafbackground(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('aafBackGround.png')
    #    self.image = pygame.surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = ( 25, 75)

class aafkader(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('aafKaderGroen.png')
    #    self.image = pygame.surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

class aafEnemy(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemyOne
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pygame.image.load('aafPaulusIdleImage.png')
        #self.image.set_colorkey(BLACK)
        self.image = pygame.image.load("Rat.png")
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 100
        self.counter_right = 2000
        self.counter_left = 2000
        self.right = True
        self.left = False

    def move_right(self):
        self.vx += enemy_speed

    def move_left(self):
        self.vx += -enemy_speed

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                    self.right = False
                    self.left = True
                if self.vx < 0:
                    self.x = hits[0].rect.right
                    self.left = False
                    self.right = True
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_lava(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                    self.right = False
                    self.left = True
                if self.vx < 0:
                    self.x = hits[0].rect.right
                    self.left = False
                    self.right = True
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

        #rekt_by_lava = pygame.sprite.spritecollide(self, self.game.lava, False)
        #if rekt_by_lava:
        #    self.kill

    def collide_with_Player(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.player_hp -= 3

    def gravity(self):
        self.vx, self.vy = 0, player_gravity

    def update(self):
        self.gravity()
        if self.right:
            self.move_right()
            self.image = pygame.image.load("Rat.png")
        if self.left:
            self.move_left()
            self.image = pygame.image.load("RatT.png")
        self.x += self.vx #* self.game.dt
        self.y += self.vy #* self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.collide_with_lava('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_lava('y')
        self.collide_with_Player()
            #self.rect.right = 0
            #self.rect.x += -enemy_speed

class aafGEnemy(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemyOne
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pygame.image.load('aafPaulusIdleImage.png')
        #self.image.set_colorkey(BLACK)
        self.image = pygame.image.load("GhostO.png")
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 100
        self.counter_right = 2000
        self.counter_left = 2000
        self.right = True
        self.left = False

    def move_right(self):
        self.vx += enemy_speed

    def move_left(self):
        self.vx += -enemy_speed

    def collide_with_lava(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                    self.right = False
                    self.left = True
                if self.vx < 0:
                    self.x = hits[0].rect.right
                    self.left = False
                    self.right = True
                self.vx = 0
                self.rect.x = self.x

    def collide_with_Player(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.player_hp -= 6

    def gravity(self):
        self.vx, self.vy = 0, player_gravity

    def update(self):
        if self.right:
            self.move_right()
            self.image = pygame.image.load("GhostO.png")
        if self.left:
            self.move_left()
            self.image = pygame.image.load("GhostT.png")
        if self.vx > 35:
            self.vx = 35
        if self.vx < -35:
            self.vx = -35

        self.x += self.vx #* self.game.dt
        self.y += self.vy #* self.game.dt
        self.rect.x = self.x
        self.collide_with_lava('x')
        self.rect.y = self.y

        self.collide_with_Player()
            #self.rect.right = 0
            #self.rect.x += -enemy_speed

class aafGhost(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemyOne
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("GhostO.png")
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 100
        self.counter_right = 2000
        self.counter_left = 2000
        self.right = True
        self.left = False
        self.up = False
        self.Down = True

    def move_right(self):
        self.vx += enemy_speed * 0.4

    def move_left(self):
        self.vx += -enemy_speed * 0.4

    def move_up(self):
        self.vy += enemy_speed * 0.4

    def move_down(self):
        self.vy += -enemy_speed * 0.4

    def collide_with_lava(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                #if self.vx > 0:
                #    self.respwn()
                #if self.vx < 0:
                #    self.respwn()
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                    self.right = False
                    self.left = True
                if self.vx < 0:
                    self.x = hits[0].rect.right
                    self.left = False
                    self.right = True
                self.vx = 0
                self.rect.x = self.x

        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                if self.vy > 0:
                #    self.respwn()
                    self.Down = False
                    self.up = True
                if self.vy < 0:
                #    self.respwn()
                    self.up = False
                    self.down = True

        #rekt_by_lava = pygame.sprite.spritecollide(self, self.game.lava, False)
        #if rekt_by_lava:
        #    self.kill

    def collide_with_Player(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.player_hp -= 5

    def respwn(self):
        self.rect.x = 25 * random.randrange(5, 400)
        self.rect.y = 25 * random.randrange(9, 44)
        self.rand = random.randrange(1,4)
        if self.rand == 1:
            self.right = True
            self.up = True
            self.left = False
            self.down = False
        elif self.rand == 2:
            self.right = True
            self.up = False
            self.left = False
            self.down = True
        elif self.rand == 3:
            self.right = False
            self.up = True
            self.left = True
            self.down = False
        else:
            self.right = False
            self.up = False
            self.left = True
            self.down = True

    def update(self):
        self.collide_with_lava('x')
        self.collide_with_lava('y')
        if self.right:
            self.move_right()
        if self.left:
            self.move_left()
        if self.up:
            self.move_up()
        if self.Down:
            self.move_down()

        if self.vx > 5:
            self.vx = 5
        if self.vx < -5:
            self.vx = -5
        if self.vy > 5:
            self.vy = 5
        if self.vy < -5:
            self.vy = -5

        self.x += self.vx #* self.game.dt
        self.y += self.vy #* self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_Player()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafPaulusIdleImage.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) *25
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE



    def get_keys(self):
        self.vx, self.vy = 0, player_gravity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.half_jump()
        if keys[pygame.K_SPACE]:
            self.jump()
            #self.vy = -player_speed
        #if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            #self.vy = player_speed
        #if self.vx != 0 and self.vy != 0:
        #    self.vx *= 0.7071
        #    self.vy *= 0.7071

    def jump(self):
        #self.jumpy = jump_acceleration(up(), 20)
        #jump = jump_acceleration(up(self),20)
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.ijs, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
        self.rect.y -= 1
        if hits:
            self.vy = -player_jump

    def half_jump(self):
        #self.jumpy = jump_acceleration(up(), 20)
        #jump = jump_acceleration(up(self),20)
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.ijs, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
        self.rect.y -= 1
        if hits:
            self.vy = -(player_jump / 2)

            #self.jump_acceleration(20)

        #jump only if check standing on a platform = True
        #self.rect.y += 1
        #hits = pygame.sprite.spritecollide(self, self.Game.platforms, False)
        #self.rect.y -= 1
        #if hits:
        #    self.vel.y = -player_jump

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def l_c(self, dir):
        if dir == 'x':
            self.rect.x += 1
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            self.rect.x -= 1
            if hits:
                return True
        if dir == 'y':
            self.rect.y += 1
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            self.rect.y -= 1
            if hits:
                return True

    def rekt_by_lava(self):
        rekt_by_lava = self.l_c('x') or self.l_c('y')
        if rekt_by_lava:
            self.game.player_hp -= 2

    def collide_with_spikes(self):
        Impailed_by_Spikes = pygame.sprite.spritecollide(self, self.game.Spikes, False)
        if Impailed_by_Spikes:
            self.game.playing = False

    def update(self):
        self.get_keys()
        self.x += self.vx #* self.game.dt
        self.y += self.vy #* self.game.dt


        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')


        self.rekt_by_lava()
        self.collide_with_spikes()

class aafPlayer(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.groups = game.all_sprites, game.Players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafPaulusIdleImage.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y * 25
        self.rect.x = x * 25
        self.change_x = 0
        self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            if self.change_y < 23:
                self.change_y += 1.8
            else:
                self.change_y = 23

    def coli(self):
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def get_keys(self):

        #for event in pygame.event.get():
        #    if event.type == pygame.KEYDOWN:
        #        if event.key == pygame.K_LEFT or pygame.K_a:
        #            self.go_left()
        #        if event.key == pygame.K_RIGHT or pygame.K_d:
        #            self.go_right()
        #        if event.key == pygame.K_UP or pygame.K_SPACE:
        #            self.jump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or pygame.K_a:
                    self.go_left()
                if event.key == pygame.K_RIGHT or pygame.K_d:
                    self.go_right()
                if event.key == pygame.K_UP or pygame.K_SPACE or pygame.K_w:
                    self.jump()

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a) and self.change_x < 0 :
                    self.stop()
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d) and self.change_x > 0 :
                    self.stop()

    def s_m(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) or (keys[pygame.K_LEFT] and keys[pygame.K_d]) or (keys[pygame.K_a] and keys[pygame.K_RIGHT]) or (keys[pygame.K_a] and keys[pygame.K_d]):
            self.stop()
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.go_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.go_right()
        else:
            self.stop()

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False) or pygame.sprite.spritecollide(self, self.game.ijs, False) or pygame.sprite.spritecollide(self, self.game.lava, False)
        self.rect.y -= 1
        if hits:
            self.change_y = -24.2

    def go_left(self):
        self.change_x = -player_speed

    def go_right(self):
        self.change_x = player_speed

    def stop(self):
        self.change_x = 0

    def l_c(self, dir):
        if dir == 'x':
            self.rect.x += 1
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            self.rect.x -= 1
            if hits:
                return True
        if dir == 'y':
            self.rect.y += 1
            hits = pygame.sprite.spritecollide(self, self.game.lava, False)
            self.rect.y -= 1
            if hits:
                return True

    def h_l(self):
        hits = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hits:
            return True

    def rekt_by_lava(self):
        rekt_by_lava = self.l_c('x') or self.l_c('y') or self.h_l()
        if rekt_by_lava:
            self.game.player_hp -= 6

    def collide_with_spikes(self):
        Impailed_by_Spikes = pygame.sprite.spritecollide(self, self.game.Spikes, False)
        if Impailed_by_Spikes:
            self.game.playing = False

    def update(self):
        self.calc_grav()
        self.s_m()


        self.coli()
        self.rekt_by_lava()
        self.collide_with_spikes()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafWall.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Lava(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.lava
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafLava.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class aafSpike(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafSpike.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class aafDirt(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.dirt
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafWall.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(6, 400)
        self.rect.y = 75 - random.randrange(1, 400)

    def collide_with_object(self):
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.player_hp -= 8
            #self.game.playing = False
            self.respwn()
        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()

    def respwn(self):
        self.rect.x = 25 * random.randrange(6, 400)
        self.rect.y = 75 - random.randrange(1, 400)

    def update(self):
        self.rect.y += aafFalling                                                       #update eigenschap, altijd vallen
        self.collide_with_object()

class aafDirtL(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.dirt
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafWall.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(6, 400)
        self.rect.y = 75 - random.randrange(1, 400)

    def collide_with_object(self):
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.player_hp -= 8
            #self.game.playing = False
            self.respwn()
        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()

    def respwn(self):
        self.rect.x = 25 * random.randrange(6, 400)
        self.rect.y = 75 - random.randrange(1, 400)

    def update(self):
        self.rect.y += aafFalling
        self.rect.x += -aafFalling                                                   #update eigenschap, altijd vallen
        self.collide_with_object()

class aafDirtR(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.dirt
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafWall.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(6, 400)
        self.rect.y = 75 - random.randrange(1, 400)

    def collide_with_object(self):
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.player_hp -= 8
            #self.game.playing = False
            self.respwn()
        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()

    def respwn(self):
        self.rect.x = 25 * random.randrange(6, 400)
        self.rect.y = 75 - random.randrange(1, 400)

    def update(self):
        self.rect.y += aafFalling
        self.rect.x += aafFalling                                                   #update eigenschap, altijd vallen
        self.collide_with_object()

class aafijs(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ijs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('aafijs.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class aafTOKEN(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('TOKEN.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def collide_with_object(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.score += random.randrange(2,15)
            self.respwn()

        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()

    def respwn(self):
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def update(self):
        self.collide_with_object()

class aafShroom(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game                                             #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('Shroom.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def collide_with_object(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.score += random.randrange(2,5)
            self.respwn()

        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()
    def respwn(self):
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def update(self):
        self.collide_with_object()

class aafLive(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game                                             #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('life.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def collide_with_object(self):
        if self.game.player_hp > 75:
            hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
            if hitsPlayer:
                self.game.player_hp = 100
                self.respwn()
        else:
            hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
            if hitsPlayer:
                self.game.player_hp += random.randrange(1, 25)
                self.respwn()

        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()
    def respwn(self):
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def update(self):
        self.collide_with_object()

class aafKlaver(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game                                             #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('aafKlaver.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def collide_with_object(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.game.Players, False)
        if hitsPlayer:
            self.game.score += random.randrange(29,59)
            self.respwn()

        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.respwn()

        hitsLava = pygame.sprite.spritecollide(self, self.game.lava, False)
        if hitsLava:
            self.respwn()
    def respwn(self):
        self.rect.x = 25 * random.randrange(20, 400)
        self.rect.y = 25 * random.randrange(9, 44)

    def update(self):
        self.collide_with_object()

class Game:
    #generator = 30
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(aafTitle)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1500,100)
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = aafMAP(path.join(self.game_folder, 'map.txt'))
        with open(path.join(self.game_folder, aafHS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        # start a new game
        self.score = 0
        self.timer = int(0)
        self.player_hp = 100
        self.total_hp = "/100"
        self.frames = "{:.2f}".format(self.clock.get_fps())
        self.draw_debug = False
        self.paused = False


        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.lava = pygame.sprite.Group()
        self.wallss = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.aafkader_sprite = pygame.sprite.Group()
        self.enemyOne = pygame.sprite.Group()
        self.dirt = pygame.sprite.Group()
        self.ijs = pygame.sprite.Group()
        self.Players = pygame.sprite.Group()
        self.Spikes = pygame.sprite.Group()

        self.background = aafbackground('aafBackGround.png', [0,0])
        self.backgrounds.add(self.background)

        self.aafkader = aafkader('aafKaderGroen.png', [0,0])
        self.aafkader_sprite.add(self.aafkader)


        #self.player = Player(self, 10, 10)

        #for x in range(10, 20):
        #    Wall (self, x, 5)


        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = aafPlayer(self, col, row)
                if tile == 'S':
                    Lava(self, col, row)
                if tile == 'E':
                    self.EO = aafEnemy(self, col, row)
                if tile == 'I':
                    self.IJS = aafijs(self, col, row)
                if tile == 'K':
                    aafSpike(self, col, row)
                if tile == 'G':
                    aafGEnemy(self,col,row)
                    #aafGhost(self,col, row)


        for i in range(30):
            D = aafDirt(self)

        for i in range(10):
            L = aafDirtL(self)

        for i in range(10):
            R = aafDirtL(self)

        for i in range(10):
            T = aafTOKEN(self)

        for i in range(20):
            H = aafShroom(self)

        for i in range(2):
            P = aafLive(self)

        for i in range(1):
            K = aafKlaver(self)

        self.Camera = aafCamera(self.map.width, self.map.height)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            #self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.Camera.update(self.player)
        self.frames = "{:.2f}".format(self.clock.get_fps())
        # check if player hits a platform - only if falling
        self.timer += int(1/FPS)
        #if self.player.rect.right >= WIDTH / 1.3 :
        #    self.player.x -= abs(self.player.vx)
        #    self.score += 10
        if self.player_hp < 1:
            self.playing = False
            self.end = True

    def quit(self):
        self.playing = False

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            print(event)
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    pygame.quit()
                    sys.exit()
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    self.running = False
                if event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused
        #        if event.key == pygame.K_LEFT or pygame.K_a:
        #            aafPlayer.go_left()
        #        if event.key == pygame.K_RIGHT or pygame.K_d:
        #            aafPlayer.go_right()
        #        if event.key == pygame.K_UP or pygame.K_SPACE:
        #            aafPlayer.jump()

        #    if event.type == pygame.KEYUP:
        #        if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a) and self.change_x < 0 :
        #            self.aafPlayer.stop(self.player)
        #        if (event.key == pygame.K_RIGHT) or (event.key == event.key) or (event.key == pygame.K_d) and self.change_x > 0 :
        #            self.aafPlayer.stop(self.player)



                    #self.navigate_menu()

            #    if event.key == pygame.K_LEFT:
            #        self.player.move(dx=-1)
            #    if event.key == pygame.K_RIGHT:
            #        self.player.move(dx=1)
            #    if event.key == pygame.K_UP:
            #        self.player.move(dy=-1)
            #    if event.key == pygame.K_DOWN:
            #        self.player.move(dy=1)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(WHITE)
        self.backgrounds.draw(self.screen)
        #self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.Camera.apply(sprite))

        self.aafkader_sprite.draw(self.screen)
        pygame.draw.rect(gameDisplay, GREEN, (25 * 28, 0, 500 - ((((100 - self.player_hp)/100)*500)), 74))
        self.draw_text(str(self.score), 34, WHITE, 125, 19)
        self.draw_timer(str(self.frames), 34, WHITE, 295, 19)
        self.draw_timer(str(self.player_hp), 34, WHITE, 950, 19)
        self.draw_timer(str(self.total_hp), 34, WHITE, 1000, 19)
        if self.paused:
            self.draw_text(('Paused'), 60, RED, WIDTH/2, HEIGHT/2)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(aafTitle, 48, WHITE, WIDTH / 2, 15)

        self.screen.blit(pygame.image.load('Rat.png'), ( 35, 150 ))
        self.screen.blit(pygame.image.load('GhostO.png'), ( 105, 145 ))
        self.draw_text("The evil cave rat/ghost will move left and right, getting hit by it will reduce ur health", 22,WHITE, 520, 155 )
        self.screen.blit(pygame.image.load('aafSpike.png'), ( 35, 220 ))
        self.draw_text("The deadly cave spike will  one shot you, if you get it you will instantly die!", 22,WHITE, 490, 225 )
        self.screen.blit(pygame.image.load('aafWall.png'), ( 50, 300 ))
        self.draw_text("Hitting the cave rocks will prevent you from moving further, getting hit by fallen rocks will reduce ur health", 22,WHITE, 616, 300 )
        self.screen.blit(pygame.image.load('aafLava.png'), ( 50, 350 ))
        self.draw_text("Hot burning blocks of lava, touching it or standing on it will reduce ur health untile you die a horrible death!", 22,WHITE, 620, 350 )
        #self.screen.blit(pygame.image.load('aafWall.png'), ( 35, 800 ))

        self.screen.blit(pygame.image.load('aafPaulusIdleImage.png'), ( 40, 400 ))
        self.draw_text("This is Paulus, <- / a to move to the left, -> / d to move to the right, up / w / space to jump", 22, WHITE, 555, 425)
        self.screen.blit(pygame.image.load('TOKEN.png'), ( 40, 530 ))
        self.screen.blit(pygame.image.load('Shroom.png'), ( 90, 530 ))
        self.draw_text("The mushroom and the token give you score, collecting them will spown another random one", 22, WHITE, 575, 530)
        self.screen.blit(pygame.image.load('life.png'), ( 40, 590 ))
        self.draw_text("The hearts will restore your health, collecting them will spown another random one", 22, WHITE, 535, 590)

        self.draw_text("P to pause, ESC to quit", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 250)
        self.draw_text("PRESS SPACE TO PLAY", 22, WHITE, WIDTH / 2, (HEIGHT * 3 / 4) + 130)
        self.draw_text("High Score: " + str(self.highscore), 22, white, WIDTH / 2, 70)
        pygame.display.flip()
        self.w_f_k()

    def w_f_k(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        waiting = False

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLACK)
        self.draw_text(('GAME OVER'), 60, RED, WIDTH/2, HEIGHT/2)
        self.draw_text(('Press R to restart and ESC to exit'), 60, RED, WIDTH/2 , HEIGHT/2 + 150)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 60, RED, WIDTH / 2, HEIGHT / 2 - 150)
            with open(path.join(self.game_folder, aafHS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 60, RED, WIDTH / 2, HEIGHT / 2 - 150)
        pygame.display.flip()
        self.wait_for_enter()

        return self.wait_for_enter()

    def wait_for_enter(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        return True
                    if event.key == pygame.K_r:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_timer(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
#game ali ended
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#game vincent start here:
class vjbackground(pygame.sprite.Sprite):
    def __init__(self, image_file, location):                       #initator(superfunctie) zorgt ervoor dat je de class kan oproepen
        pygame.sprite.Sprite.__init__(self)                         #initate als een sprite(pygame sprite groups kan nu erop toegepast worden)
        self.image = pygame.image.load("MBG.png")         #de hoofd attribute van de class, de class verbinden aan een foto
    #    self.image = pygame.surface((w, h))                        #staat uit als er geen image bekend is class verbenden aan een pygame.surface breedte hoogte
        self.rect = self.image.get_rect()                           #rectangle maken van de image, handig om de randen van de foto te kennen om de foto te kunnen plaatsen
        self.rect.topleft = ( 25, 75)                               #foto topleft rectangle coordinaten toepassen.

class vjkader(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('aafKaderGroen.png')
    #    self.image = pygame.surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

class vjFruit(pygame.sprite.Sprite):
    def __init__(self, vj):
        pygame.sprite.Sprite.__init__(self)
        self.vj = vj                                                #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('vjFruit.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(1, 45)
        self.rect.y = 75 - random.randrange(1, 150)


    def collide_with_walls(self):
        hits = pygame.sprite.spritecollide(self, self.vj.vjwalls, False)                    #collision
        if hits:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.vj.Players, False)
        if hitsPlayer:
            self.vj.score += 10
            self.respwn()

    def respwn(self):
        randomnumber_x = random.randrange(1, 45)
        randomnumber_y = random.randrange(1, 150)
        self.rect.x = 25 * randomnumber_x
        self.rect.y = 75 - randomnumber_y

    def update(self):
        self.rect.y += vjFalling                                                       #update eigenschap, altijd vallen
        self.collide_with_walls()                                                      #collision functie die eerder gedefiend is runnen

class vjSteen(pygame.sprite.Sprite):
    def __init__(self, vj):
        self.groups = vj.all_sprites, vj.stenen
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.vj = vj                                                #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('aafWall.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(1, 45)
        self.rect.y = 75 - random.randrange(1, 450)



    def collide_with_walls(self):
        hits = pygame.sprite.spritecollide(self, self.vj.vjwalls, False)                    #collision
        if hits:
            self.respwn()

    def respwn(self):
        randomnumber_x = random.randrange(1, 45)
        randomnumber_y = random.randrange(1, 450)
        self.rect.x = 25 * randomnumber_x
        self.rect.y = 75 - randomnumber_y

    def update(self):
        self.rect.y += vjFalling                                                       #update eigenschap, altijd vallen
        self.collide_with_walls()

class vjWall(pygame.sprite.Sprite):
    def __init__(self, vj, x, y):
        self.groups = vj.all_sprites, vj.vjwalls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.vj = vj
        self.image = pygame.image.load('vjDirt.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class vjPlayer(pygame.sprite.Sprite):
    def __init__(self, vj, x, y):
        self.groups = vj.all_sprites, vj.Players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.vj = vj
        self.image = pygame.image.load('aafPaulusIdleImage.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def get_keys(self):
        self.vx, self.vy = 0, player_gravity                                            #x,y versnelling (y = zwaarte kracht)
        keys = pygame.key.get_pressed()                                                 #opnemen van ingedrukte keys onder de variable keys en vervolgens gebruiken voor de beweging
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = player_speed

    def collide_with_walls(self, dir):
        if dir == 'x':                                                                          #directie
            hits = pygame.sprite.spritecollide(self, self.vj.vjwalls, False)                    #als x directie
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width                                #collision = speler x := object linkerkant - speler breedte(want x is aan linkerkant)
                if self.vx < 0:
                    self.x = hits[0].rect.right                                                 #collision = speler x := object rechterkant(zonder -breedte want x is al linkerkant)
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':                                                                          #als y directie
            hits = pygame.sprite.spritecollide(self, self.vj.vjwalls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def hit_stone(self):
        hP = pygame.sprite.spritecollide(self, self.vj.stenen, False)
        if hP:
            self.vj.playing = False

    def update(self):
        self.get_keys()
        self.x += self.vx #* self.game.dt
        self.y += self.vy #* self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.hit_stone()

class vj:
    def __init__(self):
        # initialize game window, etc
        pygame.init()                                                           #initiator
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))                  #display onder de variable screen zetten
        pygame.display.set_caption(vj_title)                                     #display title
        self.clock = pygame.time.Clock()                                        #clock onder variable opslaan
        pygame.key.set_repeat(500,100)                                          #ingedrukte sleutel
        self.running = True                                                     #gameloop variable
        self.font_name = pygame.font.match_font(FONT_NAME)                      #tekst style(arial)
        self.load_data()                                                        #functie uitvoeren

    def load_data(self):                                                        #loaden van eerder voorgemaakt omgeving
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'vjmap.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # start a new game
        self.score = 0
        self.timer = int(0)
        self.frames = "{:.2f}".format(self.clock.get_fps())
        self.all_sprites = pygame.sprite.Group()                                #hoofdgroep, groepen maken voor het tekenen en voor collision
        self.vjkader_sprite = pygame.sprite.Group()
        self.F = pygame.sprite.Group()
        self.S = pygame.sprite.Group()
        self.vjwalls = pygame.sprite.Group()
        self.background = vjbackground("MBG.png", [0,0])
        self.all_sprites.add(self.background)
        self.Players = pygame.sprite.Group()
        self.stenen = pygame.sprite.Group()

        self.vjkader = vjkader('aafKaderGroen.png', [0,0])                      #instantie maken van een class
        self.vjkader_sprite.add(self.vjkader)                                   #instantie toevoegen aan groep

        for i in range(8):
            f = vjFruit(self)
            self.all_sprites.add(f)
            self.F.add(f)

        for i in range(3):
            s = vjSteen(self)
            self.all_sprites.add(s)
            self.S.add(s)

        for row, tiles in enumerate(self.map_data):                             #list crearen uit map.txt
            for col, tile in enumerate(tiles):
                if tile == '1':
                    vjWall(self, col, row)
                if tile == 'P':
                    self.player = vjPlayer(self, col, row)

        self.run()                                                              #runt run functie



    def run(self):                                                              #run functie
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            #self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):                                                           #update functie
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        self.timer += int(1/FPS)
        self.frames = "{:.2f}".format(self.clock.get_fps())
        #if self.player.rect.right >= WIDTH / 1.3 :
        #    self.player.x -= abs(self.player.vx)
        #    self.score += 10


    def quit(self):                                                             #quite functie
        #pygame.quit()
        #sys.exit()
        self.playing = False



    def events(self):                                                           #input nemen
        # Game Loop - events
        for event in pygame.event.get():
            print(event)
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()





            #    if event.key == pygame.K_LEFT:
            #        self.player.move(dx=-1)
            #    if event.key == pygame.K_RIGHT:
            #        self.player.move(dx=1)
            #    if event.key == pygame.K_UP:
            #        self.player.move(dy=-1)
            #    if event.key == pygame.K_DOWN:
            #        self.player.move(dy=1)

    def draw(self):                                                             #renderen
        # Game Loop - draw
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.vjkader_sprite.draw(self.screen)
        self.draw_text(str(self.score), 34, WHITE, 125, 19)
        self.draw_timer(str(self.frames), 34, WHITE, 295, 19)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_timer(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
#game vincent ended
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#game kin tiu start here:
class chCamera():
        def __init__(self, width, height):
            self.chCamera = pygame.Rect(0 ,0 ,width ,height)
            self.width = 92 * 25
            self.height = HEIGHT

        def apply(self, entity):
            return entity.rect.move(self.chCamera.topleft)

        def update(self, target):
            x = - target.rect.x + int(WIDTH / 2)
            y = - target.rect.y + int(HEIGHT / 2)

            #limit scrolling to map size
            x = min(0, x) #left
            y = min(0, y) #top
            #x = max(-(self.width - WIDTH), x) #right
            y = max(-(self.height - HEIGHT), y) #bottom
            x = max(-(self.width - WIDTH), x) #bottom
            self.chCamera = pygame.Rect(x, y, self.width, self.height)

class chbackground(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('chachtergrond.png')
    #    self.image = pygame.surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = ( 25, 75)

class chCarOne(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites, ch.S
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.image.load('chCarOne.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def collide_with_walls(self):
        hits = pygame.sprite.spritecollide(self, self.ch.chwalls, False)                    #collision
        if hits:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.ch.chPlayers, False)
        if hitsPlayer:
            self.ch.playing = False

    def respwn(self):
        self.rect.y = 800

    def update(self):
        self.rect.y += -chCarOne_speed                                                      #update eigenschap, altijd vallen
        self.collide_with_walls()

class chCarTwo(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites, ch.S
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.image.load('chCarTwo.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def collide_with_walls(self):
        hits = pygame.sprite.spritecollide(self, self.ch.chwalls, False)                    #collision
        if hits:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.ch.chPlayers, False)
        if hitsPlayer:
            self.ch.playing = False

    def respwn(self):
        self.rect.y = 800

    def update(self):
        self.rect.y += -chCarTwo_speed                                                      #update eigenschap, altijd vallen
        self.collide_with_walls()

class chCarThree(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites, ch.S
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.image.load('chCarThree.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def collide_with_walls(self):
        hits = pygame.sprite.spritecollide(self, self.ch.chwalls, False)                    #collision
        if self.rect.y == 850:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.ch.chPlayers, False)
        if hitsPlayer:
            self.ch.playing = False

    def respwn(self):
        self.rect.y = 0

    def update(self):
        self.rect.y += chCarThree_speed                                                      #update eigenschap, altijd vallen
        self.collide_with_walls()

class chCarFour(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites, ch.S
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.image.load('chCarFour.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def collide_with_walls(self):
        hits = pygame.sprite.spritecollide(self, self.ch.chwalls, False)                    #collision
        if self.rect.y == 850:
            self.respwn()

        hitsPlayer = pygame.sprite.spritecollide(self, self.ch.chPlayers, False)
        if hitsPlayer:
            self.ch.playing = False

    def respwn(self):
        self.rect.y = 0

    def update(self):
        self.rect.y += chCarFour_speed                                                      #update eigenschap, altijd vallen
        self.collide_with_walls()

class chWall(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites, ch.chwalls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(randomcolor)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class chEdge(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites, ch.edge
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class chTOKEN(pygame.sprite.Sprite):
    def __init__(self, ch):
        pygame.sprite.Sprite.__init__(self)
        self.ch = ch                                                #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('TOKEN.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(1, 90)
        self.rect.y = 25 * random.randrange(4, 31)

    def collide_with_Player(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.ch.chPlayers, False)
        if hitsPlayer:
            self.ch.score += random.randrange(3,10)
            self.respwn()

    def respwn(self):
        self.rect.x = 25 * random.randrange(1, 90)
        self.rect.y = 25 * random.randrange(4, 31)

    def update(self):
        self.collide_with_Player()

class chShroom(pygame.sprite.Sprite):
    def __init__(self, ch):
        pygame.sprite.Sprite.__init__(self)
        self.ch = ch                                                #de game bekend maken bij de class zodat je de game elementen kan beschikken en zo class kan toevoegen aan groepen
        self.image = pygame.image.load('Shroom.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 25 * random.randrange(1, 90)
        self.rect.y = 25 * random.randrange(4, 31)

    def collide_with_Player(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.ch.chPlayers, False)
        if hitsPlayer:
            self.ch.score += random.randrange(2,4)
            self.respwn()

    def respwn(self):
        self.rect.x = 25 * random.randrange(1, 90)
        self.rect.y = 25 * random.randrange(4, 31)

    def update(self):
        self.collide_with_Player()

class chPlayer(pygame.sprite.Sprite):
    def __init__(self, ch, x, y):
        self.groups = ch.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ch = ch
        self.image = pygame.image.load('chPlayer.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -ch_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = ch_speed
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.vy = -ch_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = ch_speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.ch.chwalls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.ch.chwalls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_edge(self):
        death = pygame.sprite.spritecollide(self, self.ch.edge, False)
        if death:
            self.ch.playing = False

        def collide_with_ship(self):
            flew = pygame.sprite.spritecollide(self, self.ch.SHIP, False)
            if flew:
                self.vy = -chflew_speed


    def update(self):
        self.get_keys()
        self.x += self.vx #* self.game.dt
        self.y += self.vy #* self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_edge()

class ch:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(ch_title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = aafMAP(path.join(self.game_folder, 'ch.txt'))
        with open(path.join(self.game_folder, chHS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        # start a new game
        self.score = 0
        self.timer = int(0)
        self.frames = "{:.2f}".format(self.clock.get_fps())
        self.all_sprites = pygame.sprite.Group()
        self.aafkader_sprite = pygame.sprite.Group()
        self.paused = False

        self.chwalls = pygame.sprite.Group()
        self.edge = pygame.sprite.Group()
        self.chkader_sprite = pygame.sprite.Group()

        self.S = pygame.sprite.Group()
        self.A = pygame.sprite.Group()
        self.B = pygame.sprite.Group()
        self.C = pygame.sprite.Group()

        self.T = pygame.sprite.Group()
        self.SH = pygame.sprite.Group()

        self.chBackground = pygame.sprite.Group()
        self.chB = chbackground("chachtergrond.png", [25, 75])
        self.all_sprites.add(self.chB)
        #self.chBackground.add(self.chB)

        self.chPlayers = pygame.sprite.Group()

        self.aafkader = aafkader('aafKaderGroen.png', [0,0])
        self.aafkader_sprite.add(self.aafkader)

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.WALL = chWall(self, col, row)
                    self.all_sprites.add(self.WALL)
                    self.chwalls.add(self.WALL)

                if tile == 'S':
                    self.s = chCarOne(self, col, row)
                    self.all_sprites.add(self.s)
                    self.S.add(self.s)

                if tile == 'A':
                    self.a = chCarTwo(self, col, row)
                    self.all_sprites.add(self.a)
                    self.A.add(self.a)

                if tile == 'B':
                    self.b = chCarThree(self, col, row)
                    self.all_sprites.add(self.b)
                    self.B.add(self.b)

                if tile == 'C':
                    self.c = chCarFour(self, col, row)
                    self.all_sprites.add(self.c)
                    self.C.add(self.c)

                if tile == 'P':
                    self.player = chPlayer(self, col, row)
                    self.all_sprites.add(self.player)
                    self.chPlayers.add(self.player)

                if tile == 'E':
                    self.EDGE = chEdge(self, col, row)
                    self.all_sprites.add(self.EDGE)
                    self.edge.add(self.EDGE)

        for i in range(16):
            t = chTOKEN(self)
            self.all_sprites.add(t)
            self.T.add(t)

        for i in range(16):
            sh = chShroom(self)
            self.all_sprites.add(sh)
            self.SH.add(sh)


        #for i in range(2):
        #    a = vrachtauto(self)
        #    self.all_sprites.add(f)
        #    self.A.add(f)

        self.Camera = chCamera(self.map.width, self.map.height)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            #self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.Camera.update(self.player)
        self.frames = "{:.2f}".format(self.clock.get_fps())
        self.timer += int(1/FPS)

    def quit(self):
        #pygame.quit()
        #sys.exit()
        self.playing = False

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            print(event)
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.quit()
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def draw(self):
        # Game Loop - draw
        self.screen.fill(WHITE)
        #pygame.draw.rect(gameDisplay, RED, (25,0,50, HEIGHT))
        #pygame.draw.rect(gameDisplay, GREEN, (75,0,500, HEIGHT))
        #pygame.draw.rect(gameDisplay, RED, (575,0,300, HEIGHT))
        #pygame.draw.rect(gameDisplay, BLUE, (875,0,50, HEIGHT))
        #pygame.draw.rect(gameDisplay, GREEN, (925,0,250, HEIGHT))
        #pygame.draw.rect(gameDisplay, RED, (25,0,50, HEIGHT))

        #self.all_sprites.draw(self.screen)
        #self.chBackground.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.Camera.apply(sprite))

        self.aafkader_sprite.draw(self.screen)
        self.draw_text(str(self.score), 34, WHITE, 125, 19)
        self.draw_timer(str(self.frames), 34, WHITE, 295, 19)
        if self.paused:
            self.draw_text(('Paused'), 60, RED, WIDTH/2, HEIGHT/2)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(aafTitle, 48, WHITE, WIDTH / 2, 15)


        self.screen.blit(pygame.image.load('chCarThree.png'), ( 35, 220 ))
        self.draw_text("avoid getting hit by a car or going to the edges on the top/down sides or you will instantly die!", 22,WHITE, 570, 225 )
        self.screen.blit(pygame.image.load('chPlayer.png'), ( 40, 400 ))
        self.draw_text("This is Paulus, <- / a = left, -> / d = right, up / w = uo, down / s = down", 22, WHITE, 485, 425)
        self.screen.blit(pygame.image.load('TOKEN.png'), ( 40, 530 ))
        self.screen.blit(pygame.image.load('Shroom.png'), ( 90, 530 ))
        self.draw_text("The mushroom and the token give you score, collecting them will spwn another random one", 22, WHITE, 570, 530)



        self.draw_text("P to pause, ESC to quit", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 250)
        self.draw_text("PRESS SPACE TO PLAY", 22, WHITE, WIDTH / 2, (HEIGHT * 3 / 4) + 130)
        self.draw_text("High Score: " + str(self.highscore), 22, white, WIDTH / 2, 70)
        pygame.display.flip()
        self.w_f_k()

    def w_f_k(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        waiting = False

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLACK)
        self.draw_text(('GAME OVER'), 60, RED, WIDTH/2, HEIGHT/2)
        self.draw_text(('Press R to restart and ESC to exit'), 60, RED, WIDTH/2 , HEIGHT/2 + 150)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 60, RED, WIDTH / 2, HEIGHT / 2 - 150)
            with open(path.join(self.game_folder, chHS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 60, RED, WIDTH / 2, HEIGHT / 2 - 150)
        pygame.display.flip()
        self.wait_for_enter()
    #    self.wait_for_ESC()

        return self.wait_for_enter()

    def wait_for_enter(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        return True
                    if event.key == pygame.K_r:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_timer(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
#game kin tiu ended
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#game alex start here:

# game options/settings
ayTITLE = "Paulus Climbing Adventure"
ayFPS = 60
HS_FILE = "highscore.txt"
SPRITESHEET = "sprites.png"

ayPLAYER_ACC = 0.8
ayPLAYER_FRICTION = -0.12
ayPLAYER_GRAV = 0.8
ayPLAYER_JUMP = 25


#starting platform ( positie x, positie y, groote balk, dikte balk)
ayPLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (350, HEIGHT - 300, 100, 20),
                 (700, 200, 100, 20),
                 (300, 100, 50, 20),
                 (500, 250, 80, 20),
                 (250, 300, 40, 20),
                 (650, 200, 70, 20),
                 (800, 300, 100, 20),
                 (350, 500, 80, 20),
                 (800, 700, 100, 20)
                 ]


#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
brown = (210, 105, 30)
lightblue = BGCOLOR
class ayPlayer(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load('aafPaulusIdleImage.png')
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        #jump only if standing on a platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -ayPLAYER_JUMP

    def update(self):
        self.acc = vec(0, ayPLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -ayPLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = ayPLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * ayPLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

class ayPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ayGame:
    def __init__(self):
        # pass doet niks, is een placeholder, geen error
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(ayTITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        #load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,'images')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load image
        #self.spritesheet = aySpritesheet(path.join(img_dir, SPRITESHEET))
    def new(self):
        # reset the game
        self.score = 0
        self.frames = "{:.2f}".format(self.clock.get_fps())
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = ayPlayer(self)
        self.all_sprites.add(self.player)
        self.aafkader_sprite = pygame.sprite.Group()
        self.aafkader = aafkader('aafKaderGroen.png', [0,0])
        self.aafkader_sprite.add(self.aafkader)

        for plat in ayPLATFORM_LIST:
            p = ayPlatform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    #Game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(ayFPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.frames = "{:.2f}".format(self.clock.get_fps())
        # check if player hits a platform - only falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        #Die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

    def quit(self):
        pygame.quit()
        sys.exit()
        self.playing = False

    def events(self):
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    self.running = False

            while len(self.platforms) < 12:
                width = random.randrange(50, 100)
                p = ayPlatform(random.randrange(0, WIDTH - width),
                             random.randrange(-75, -30),
                             width, 20)
                self.platforms.add(p)
                self.all_sprites.add(p)

    def draw(self):
        self.screen.fill(lightblue)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, white, WIDTH / 2, 15)
        self.aafkader_sprite.draw(self.screen)
        self.draw_text(str(self.score), 34, WHITE, 125, 19)
        self.draw_text(str(self.frames), 34, WHITE, 295, 19)

        # flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(ayTITLE, 48, white, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, white, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, white, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, white, WIDTH / 2, 15)
        pygame.display.flip()
        self.w_f_k()

    def w_f_k(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        waiting = False

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, white, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, white, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press R to restart and ESC to exit', 22, white, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, white, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, white, WIDTH / 2, HEIGHT / 2 + 40)
        pygame.display.flip()

        return self.wait_for_enter()

    def wait_for_enter(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        return True
                    if event.key == pygame.K_r:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
#game alex ended
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#game ivo start here:
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class ikMap:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * IKTILESIZE
        self.height = self.tileheight * IKTILESIZE

class ikCamera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int((WIDTH / 2) + 25)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

def collide_with_ikwalls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, sprite.ik.walls, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, sprite.ik.walls, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class ikPlayer(pygame.sprite.Sprite):
    def __init__(self, ik, x, y):
        self.groups = ik.all_sprites, ik.Players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = ik.ikPLAYER_IMG
        self.rect = self.image.get_rect()
        self.hit_rect = ikPLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * IKTILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = ikPLAYER_HEALTH
        self.score = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vec(ikPLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vec(-ikPLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                Bullet(self.ik, self.pos, dir)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.ik.dt) % 360
        self.image = pygame.transform.rotate(self.ik.ikPLAYER_IMG, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.ik.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_ikwalls(self, self.ik.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ikwalls(self, self.ik.walls, 'y')
        self.rect.center = self.hit_rect.center

class Mob(pygame.sprite.Sprite):
    def __init__(self, ik, x, y):
        self.groups = ik.all_sprites, ik.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = ik.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * IKTILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0

    def avoid_mobs(self):
        for mob in self.ik.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.ik.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pygame.transform.rotate(self.ik.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.x += 0.00001
        self.acc.y += 0.00001
        self.acc.scale_to_length(MOB_SPEED)
        self.acc += self.vel * -1
        self.vel += self.acc * self.ik.dt
        self.pos += self.vel * self.ik.dt + 0.5 * self.acc * self.ik.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_ikwalls(self, self.ik.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ikwalls(self, self.ik.walls, 'y')
        self.rect.center = self.hit_rect.center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, ik, pos, dir):
        self.groups = ik.all_sprites, ik.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = ik.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.ik.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class ikWall(pygame.sprite.Sprite):
    def __init__(self, ik, x, y):
        self.groups = ik.all_sprites, ik.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = ik.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * IKTILESIZE
        self.rect.y = y * IKTILESIZE
        self.health = WALL_HEALTH

    def update(self):
        if self.health == 0:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, ik, x, y):
        self.groups = ik.all_sprites, ik.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = ik.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * IKTILESIZE
        self.rect.y = y * IKTILESIZE

class ikTOKEN(pygame.sprite.Sprite):
    def __init__(self, ik):
        self.groups = ik.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = pygame.image.load('coin.png')
        self.rect = self.image.get_rect()
        self.rect.x = 50 * random.randrange(2, 62)
        self.rect.y = 50 * random.randrange(2, 29)

    def collide_with_object(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.ik.Players, False)
        if hitsPlayer:
            self.ik.coin_count += random.randrange(2,15)
            self.respwn()

        hits = pygame.sprite.spritecollide(self, self.ik.walls, False)
        if hits:
            self.respwn()

    def respwn(self):
        self.rect.x = 50 * random.randrange(2, 62)
        self.rect.y = 50 * random.randrange(2, 29)

    def update(self):
        self.collide_with_object()

class ikSHROOM(pygame.sprite.Sprite):
    def __init__(self, ik):
        self.groups = ik.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.ik = ik
        self.image = pygame.image.load('Shroom.png')
        self.rect = self.image.get_rect()
        self.rect.x = 50 * random.randrange(2, 62)
        self.rect.y = 50 * random.randrange(2, 29)

    def collide_with_object(self):
        hitsPlayer = pygame.sprite.spritecollide(self, self.ik.Players, False)
        if hitsPlayer:
            self.ik.coin_count += random.randrange(2,6)
            self.respwn()

        hits = pygame.sprite.spritecollide(self, self.ik.walls, False)
        if hits:
            self.respwn()

    def respwn(self):
        self.rect.x = 50 * random.randrange(2, 62)
        self.rect.y = 50 * random.randrange(2, 29)

    def update(self):
        self.collide_with_object()

class ikBackground(pygame.sprite.Sprite):
    def __init__(self, ik, x, y):
        self.groups = ik.all_sprites, ik.backgrounds
        pygame.sprite.Sprite.__init__(self, self.groups) # call sprite initializer
        self.ik = ik
        self.image = ik.bg_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * IKTILESIZE
        self.rect.y = y * IKTILESIZE

class Lives(pygame.sprite.Sprite):
    def __init__(self, ik, x, y):
        self.groups = ik.all_sprites, ik.backgrounds
        pygame.sprite.Sprite.__init__(self, self.groups) # call sprite initializer
        self.ik = ik
        self.image = ik.life_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * IKTILESIZE
        self.rect.y = y * IKTILESIZE

def draw_ikPLAYER_HEALTH(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 74
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = ORANGE
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives):
    HEARTS = lives

    while HEARTS == 3:
        surf.blit(pygame.image.load(LIFE_IMG), (x, y))
        surf.blit(pygame.image.load(LIFE_IMG), (x + 100, y))
        surf.blit(pygame.image.load(LIFE_IMG), (x + 200, y))
        HEARTS -= 1

    while HEARTS == 2:
        surf.blit(pygame.image.load(LIFE_IMG), (x, y))
        surf.blit(pygame.image.load(LIFE_IMG), (x + 100, y))
        HEARTS -= 1

    while HEARTS == 1:
        surf.blit(pygame.image.load(LIFE_IMG), (x, y))
        HEARTS -= 1

    while HEARTS == 0:
        surf.blit(pygame.image.load(LIFE_IMG), (x, y))
        HEARTS -= 1

class ik:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(ikTITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.lives = ikPLAYER_LIVES
        self.score = 0

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = ikMap(path.join(game_folder, 'map2.txt'))
        self.ikPLAYER_IMG = pygame.image.load(ikPLAYER_IMG).convert_alpha()
        self.mob_img = pygame.image.load(MOB_IMG).convert_alpha()
        self.wall_img = pygame.image.load(WALL_IMG).convert_alpha()
        self.bullet_img = pygame.image.load(BULLET_IMG).convert_alpha()
        self.coin_img = pygame.image.load(COIN_IMG).convert_alpha()
        self.bg_img = pygame.image.load(BG_IMG).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.frames = "{:.2f}".format(self.clock.get_fps())
        self.coin_count = 0
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.background = ikBackground(self, 0, 0)
        self.Players = pygame.sprite.Group()
        self.paused = False
        self.aafkader_sprite = pygame.sprite.Group()
        self.aafKader = aafkader('aafKaderGroen.png', [0, 0])
        self.aafkader_sprite.add(self.aafKader)

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    ikWall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = ikPlayer(self, col, row)

        for i in range(15):
            T = ikTOKEN(self)

        for i in range(15):
            S = ikSHROOM(self)

        #self.player = ikPlayer(self, 36, 24)
        self.camera = ikCamera(self.map.width, self.map.height)

    def respawn(self):
        if self.lives > 1:
            self.lives -= 1
            self.score += self.coin_count
            self.new()
            self.run()
        else:
            self.score += self.coin_count
            self.playing = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        self.score += self.coin_count
        self.playing = False

    def update(self):
        # update portion of the game loop:
        self.all_sprites.update()
        self.camera.update(self.player)
        self.frames = "{:.2f}".format(self.clock.get_fps())
        # Player hits coins
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.coin_count += COIN_WORTH
            hit.kill()

        # mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.respawn()
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit walls
        hits = pygame.sprite.groupcollide(self.walls, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE

    def draw_grid(self):
        for x in range(0, WIDTH, IKTILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, IKTILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        #pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)

        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # HUD functions
        self.aafkader_sprite.draw(self.screen)
        # health
        draw_ikPLAYER_HEALTH(self.screen, 25 * 28, 0, self.player.health / ikPLAYER_HEALTH)
        self.draw_text(str(self.player.health), 34, WHITE, 950, 19)
        self.draw_text(str('/100'), 34, WHITE, 1000, 19)
        # score
        self.draw_text(str(self.coin_count), 34, WHITE, 125, 19)
        self.draw_text(str(self.frames), 34, WHITE, 295, 19)
        #pause
        if self.paused:
            self.draw_text(('Paused'), 60, RED, WIDTH/2, HEIGHT/2)

        #lives
        draw_lives(self.screen, 400, 15, self.lives)

        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        # start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(ikTITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.screen.blit(pygame.image.load(ikPLAYER_IMG), (WIDTH / 2 + 50, (HEIGHT / 2) - 70 ))
        self.screen.blit(pygame.image.load(MOB_IMG), (WIDTH / 2 - 50, (HEIGHT / 2) - 70 ))
        self.draw_text("This lil' fella (right) is your guy! He's now looking to the right, away from his enemy. He will kill you!", 22,WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Arrows / W-A-S-D to move", 22,WHITE, WIDTH / 2, (HEIGHT / 2) + 50)
        self.draw_text("Up / W to go forward, Down / S to walk backwards", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 100)
        self.draw_text("Left / A and Right / D to turn", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 150)
        self.draw_text("Space to cut wood (keep it pressed for 2 seconds)", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 200)
        self.draw_text("P to pause, ESC to quit", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 250)
        self.draw_text("PRESS SPACE TO PLAY", 22, WHITE, WIDTH / 2, (HEIGHT * 3 / 4) + 130)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        waiting = False

    def show_go_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("SCORE: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("PRESS SPACE OR ESC", 22,WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



#game ivo ended
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#game menu starts here
pygame.init()
#menu_Background = pygame.image.load("aafBackGround.png")
menu_Background = pygame.image.load("MBG.png")
menu_KaderGroenF = pygame.image.load("menuKader.png")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def click_left_click():
    while pygame.mouse.get_pressed()==(True, False, False):
        return True

def click_middle_click():
    while pygame.mouse.get_pressed()==(False, True, False):
        return True

def click_right_click():
    while pygame.mouse.get_pressed()==(False, False, True):
        return True

#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################

def menu_background(x,y):
    gameDisplay.blit(menu_Background, (x_menu_background,y_menu_background))

x_menu_background = 25
y_menu_background = 75

def menu_kaderGroenF(x,y):
    gameDisplay.blit(menu_KaderGroenF, (x_menu_kaderGroenF,y_menu_kaderGroenF))

x_menu_kaderGroenF = 0
y_menu_kaderGroenF = 0

Menu_running = False

def menu_buttons(x,y):
    gameDisplay.blit(Buttons, (x_buttons,y_buttons))

#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################

def mouse_over_aaf():
    mx, my = pygame.mouse.get_pos()
    if mx > 100 and mx < 400 and my > 125 and my < 195:
        return True
    else:
        return False

def mouse_over_VJ():
    mx, my = pygame.mouse.get_pos()
    if mx > 100 and mx < 400 and my > 225 and my < 295:
        return True
    else:
        return False

def mouse_over_CH():
    mx, my = pygame.mouse.get_pos()
    if mx > 100 and mx < 400 and my > 325 and my < 395:
        return True
    else:
        return False

def mouse_over_IK():
    mx, my = pygame.mouse.get_pos()
    if mx > 100 and mx < 400 and my > 425 and my < 495:
        return True
    else:
        return False

def mouse_over_AY():
    mx, my = pygame.mouse.get_pos()
    if mx > 100 and mx < 400 and my > 525 and my < 595:
        return True
    else:
        return False

def mouse_over_EXIT():
    mx, my = pygame.mouse.get_pos()
    if mx > 100 and mx < 400 and my > 625 and my < 695:
        return True
    else:
        return False

#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
font_name_menu = pygame.font.match_font(FONT_NAME)

def draw_textm(text, size, color, x, y):
    font = pygame.font.Font(font_name_menu, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################


Buttons = pygame.Surface((300, 75))
Buttons.fill(BLUE)

x_buttons = 150
y_buttons = 150

Menu_running = True
aaf = False
VJB = False
chB = False
ikB = False
ayB = False


Default_inter_o = "hallo, this is Paulus advnture, Paulus is a forest"
Default_inter_t = "gnome who's goal is to collect mushrooms and "
Default_inter_th = "golden coins, are you willing to help Paulus"
Default_inter_f = "in his adventures to survive and collect?"
Default_inter_fi = "are you willing to help Paulus achieve his goals?"


Menu_intro_o = Default_inter_o
Menu_intro_t = Default_inter_t
Menu_intro_th = Default_inter_th
Menu_intro_f = Default_inter_f
Menu_intro_fi = Default_inter_fi


#aaf_text = "Help Paulus survive the dark and dangaurse cave" #\n  assist Paulus in collecting reagent for a survival couse.
aaf_text_o = "While Paulus was traveling he fall into"
aaf_text_t = "a cave, inside he found lots of mushrooms"
aaf_text_th = "and coins, help Paulus survive the dark"
aaf_text_f = "and dangerous cave! and assist hem in "
aaf_text_fi = "collecting mushrooms and shiny"

vj_text_o = "Paulus needs food to survive in the wild."
vj_text_t = "Help Paulus collect fruit but watch out"
vj_text_th = "for the falling rocks!"
vj_text_f = ""
vj_text_fi = ""

ch_text_o = "Paulus was very hungry and he went to look for some "
ch_text_t = "food along the street. Fortunately he found some "
ch_text_th = "mushrooms and coins, however the traffic is"
ch_text_f = "dangerous!, be ware being hit by a moving"
ch_text_fi = "vehicle, while you help Paulus collect?"

ik_text_o =    "Paulus finds himself in a forest picking mushrooms"
ik_text_t =  "for a living. In the grass he also finds gold coins,"
ik_text_th = " earning him quite some cash. Unfortunately the forest"
ik_text_f =  "wardens have spotted his presence and "
ik_text_fi = "are trying to kill him. Run!"

ay_text_o = "Paulus lost himself in the forest."
ay_text_t = "The only way to find his home again"
ay_text_th = "is to  get himself up on the top of the tree."
ay_text_f = "Will he see his home again? Let's Jump!"
ay_text_fi = ""



EXIT_text = "Are you sure you want to end the game?"
EXIT_e = ""

aafTitle = "Cave Adventure"
vjTitle = "Fruity Adventure"
ayTitle = "Climbing Adventure"
ikTitle = "Forest Adventure"
chTitle = "Rushing Adventure"
exitTitle = "Exit"
headTitle = "Paulus' Adventures"

AAF = Game()
VJ = vj()
CH = ch()
IK = ik()
AY = ayGame()

gr = True
while gr:
    Menu_running = True
    aaf = False
    VJB = False
    chB = False
    ikB = False
    ayB = False
    while Menu_running:

        pygame.display.set_caption(headTitle)
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Menu_running = False
                    aaf = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    Menu_running = False
                    VJB = True
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Menu_running = False
                pygame.quit()
                sys.exit()

        gameDisplay.fill(WHITE)
        menu_background(x_menu_background, y_menu_background)
        menu_kaderGroenF(x_menu_kaderGroenF, y_menu_kaderGroenF)

        draw_textm(str(Menu_intro_o), 34, RED, 800, 125)
        draw_textm(str(Menu_intro_t), 34, RED, 800, 175)
        draw_textm(str(Menu_intro_th), 34, RED, 800, 225)
        draw_textm(str(Menu_intro_f), 34, RED, 800, 275)
        draw_textm(str(Menu_intro_fi), 34, RED, 800, 325)


        if mouse_over_aaf() == True:
            Menu_intro_o = aaf_text_o
            Menu_intro_t = aaf_text_t
            Menu_intro_th = aaf_text_th
            Menu_intro_f = aaf_text_f
            Menu_intro_fi = aaf_text_fi
            pygame.draw.rect(gameDisplay, GREEN, (100, 125, 345, 65))
            if click_left_click():
                Menu_running = False
                aaf = True
        else:
            pygame.draw.rect(gameDisplay, RED, (100, 125, 345, 65))


        if mouse_over_VJ() == True:
            Menu_intro_o = vj_text_o
            Menu_intro_t = vj_text_t
            Menu_intro_th = vj_text_th
            Menu_intro_f = vj_text_f
            Menu_intro_fi = vj_text_fi
            pygame.draw.rect(gameDisplay, GREEN, (100, 225, 345, 65))
            if click_left_click():
                Menu_running = False
                VJB = True
        else:
            pygame.draw.rect(gameDisplay, RED, (100, 225, 345, 65))

        if mouse_over_CH() == True:
            Menu_intro_o = ch_text_o
            Menu_intro_t = ch_text_t
            Menu_intro_th = ch_text_th
            Menu_intro_f = ch_text_f
            Menu_intro_fi = ch_text_fi
            pygame.draw.rect(gameDisplay, GREEN, (100, 325, 345, 65))
            if click_left_click():
                Menu_running = False
                chB = True
        else:
            pygame.draw.rect(gameDisplay, RED, (100, 325, 345, 65))

        if mouse_over_IK() == True:
            Menu_intro_o = ik_text_o
            Menu_intro_t = ik_text_t
            Menu_intro_th = ik_text_th
            Menu_intro_f = ik_text_f
            Menu_intro_fi = ik_text_fi

            pygame.draw.rect(gameDisplay, GREEN, (100, 425, 345, 65))
            if click_left_click():
                Menu_running = False
                ikB = True
        else:
            pygame.draw.rect(gameDisplay, RED, (100, 425, 345, 65))

        if mouse_over_AY() == True:
            Menu_intro_o = ay_text_o
            Menu_intro_t = ay_text_t
            Menu_intro_th = ay_text_th
            Menu_intro_f = ay_text_f
            Menu_intro_fi = ay_text_fi
            pygame.draw.rect(gameDisplay, GREEN, (100, 525, 345, 65))
            if click_left_click():
                Menu_running = False
                ayB = True
        else:
            pygame.draw.rect(gameDisplay, RED, (100, 525, 345, 65))

        if mouse_over_EXIT() == True:
            Menu_intro_o = EXIT_text
            Menu_intro_t = EXIT_e
            Menu_intro_th = EXIT_e
            Menu_intro_f = EXIT_e
            Menu_intro_fi = EXIT_e

            pygame.draw.rect(gameDisplay, GREEN, (100, 625, 345, 65))
            if click_left_click():
                Menu_running = False
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(gameDisplay, RED, (100, 625, 345, 65))

        if mouse_over_aaf() == False and mouse_over_VJ() == False and mouse_over_CH() == False and mouse_over_IK() == False and mouse_over_AY() == False and mouse_over_EXIT() == False:
            Menu_intro_o = Default_inter_o
            Menu_intro_t = Default_inter_t
            Menu_intro_th = Default_inter_th
            Menu_intro_f = Default_inter_f
            Menu_intro_fi = Default_inter_fi



        draw_textm(str(aafTitle), 34, WHITE, 250, 132)
        draw_textm(str(vjTitle), 34, WHITE, 250, 232)
        draw_textm(str(chTitle), 34, WHITE, 271, 332)
        draw_textm(str(ikTitle), 34, WHITE, 255, 432)
        draw_textm(str(ayTitle), 34, WHITE, 267, 532)
        draw_textm(str(exitTitle), 34, WHITE, 250, 632)

        draw_textm(str(headTitle), 55 , RED, WIDTH / 2, 5)

        pygame.display.update()
        clock.tick(10)

    while aaf or VJB or chB or ikB or ayB:
        while aaf:
            AAF.show_start_screen()
            while aaf:
                AAF.new()
                AAF.show_go_screen()
                if AAF.show_go_screen():
                    aaf = False
                    Menu_running = True

        while VJB:
            VJ.new()
            VJB = False
            Menu_running = True

        while chB:
            CH.show_start_screen()
            while chB:
                CH.new()
                CH.show_go_screen()
                if CH.show_go_screen():
                    chB = False
                    Menu_running = True

        while ikB:
            g = ik()
            g.show_start_screen()
            ikbe = True
            while ikbe:
                g.new()
                g.run()
                g.show_go_screen()
                ikbe = False
            ikB = False
            Menu_running = True

        while ayB:
            AY.show_start_screen()
            while ayB:
                AY.new()
                AY.show_go_screen()
                if AY.show_go_screen():
                    ayB = False
                    Menu_running = True


#new(self)


#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################
pygame.quit()
