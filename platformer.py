import pygame
from pygame.locals import *

pygame.init()


screen_width = 1000
screen_height= 600

clock = pygame.time.Clock()
fps = 80

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Platformer")

#define game variables
tile_size = 40

#load images
bg_img = pygame.image.load("assets/background/background.png")
bg_img2 = pygame.image.load("assets/background/middleground.png")

def draw_grid():
    for line in range(0,25):
        if line <= 15:
            pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size),(screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, 1280))

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_idle_right = []
        self.images_idle_left = []
        self.images_jump_right = []
        self.images_jump_left = []
        self.images_fall_right = []
        self.images_fall_left = []
        self.index = 0
        self.counter = 0

        #animation
        #jump/fall
        for num in range(0, 2):
            #jump
            img_jump_right = pygame.image.load(f"characters/samurai/jump/{num}.png")
            img_jump_right = pygame.transform.scale(img_jump_right, (60, 80))
            self.images_jump_right.append(img_jump_right)
            img_jump_left = pygame.transform.flip(img_jump_right, True, False)
            self.images_jump_left.append(img_jump_left)

            #fall
            img_fall_right = pygame.image.load(f"characters/samurai/fall/{num}.png")
            img_fall_right = pygame.transform.scale(img_fall_right, (60, 80))
            self.images_fall_right.append(img_fall_right)
            img_fall_left = pygame.transform.flip(img_fall_right, True, False)
            self.images_fall_left.append(img_fall_left)

        #left/right/idle
        for num in range(0, 8):
            img_idle_right = pygame.image.load(f"characters/samurai/idle/{num}.png")
            img_idle_right = pygame.transform.scale(img_idle_right, (60, 80))
            img_idle_left = pygame.transform.flip(img_idle_right, True, False)
            img_right = pygame.image.load(f"characters/samurai/run/{num}.png")
            img_right = pygame.transform.scale(img_right, (60,80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.images_idle_right.append(img_idle_right)
            self.images_idle_left.append(img_idle_left)
        self.image = self.images_idle_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.idle = True
        self.inAir = False
    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 7
        #is character in the air?
        if self.rect.bottom == screen_height:
            self.inAir = False
        else:
            self.inAir = True

        #get keypresses
        key = pygame.key.get_pressed()
        if self.rect.bottom == screen_height:
            if key[pygame.K_SPACE] and self.jumped == False:
                    self.vel_y = -10
                    self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False

        if key[pygame.K_a]:
            dx -= 3
            self.counter += 1
            self.direction = -1
            self.idle = False
        if key[pygame.K_d]:
            dx += 3
            self.counter += 1
            self.direction = 1
            self.idle = False

        #if key a or d is not pushed down
        if key[pygame.K_a] == False and key[pygame.K_d] == False:
            self.counter += 1
            self.idle= True

        #animations
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                 self.index = 0
            #facing right
            if self.inAir == False:
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                    if self.idle:
                        self.image = self.images_idle_right[self.index]
                # facing left
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                    if self.idle:
                        self.image = self.images_idle_left[self.index]
            #jumping/falling right and left
            if self.inAir:
                if self.index >= len(self.images_jump_right):
                    self.index = 0
                    if self.direction == 1:
                        if self.vel_y <= 0:
                            self.image = self.images_jump_right[self.index]
                        if self.vel_y >=0:
                            self.image = self.images_fall_right[self.index]
                    if self.direction == -1:
                        if self.vel_y <=0:
                            self.image = self.images_jump_left[self.index]
                        if self.vel_y >=0:
                            self.image = self.images_fall_left[self.index]
        #add gravity
        self.vel_y += 0.5
        if self.vel_y > 3:
            self.vel_y = 3
        dy += self.vel_y

        #check for collision

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        #draw player onto screen
        screen.blit(self.image, self.rect)

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
class World():
    def __init__(self, data):
        self.tile_list = []
        #load images
        dirt_img = pygame.image.load("assets/tiles (biome 1)/tile001.png")
        void_img = pygame.image.load("assets/tiles (biome 1)/tile014.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(void_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
world_data=[
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

#instances
player = Player(100, screen_height-40)
world = World(world_data)

run = True
while run:

    clock.tick(fps)
    screen.blit(bg_img, (0,0))
    screen.blit(bg_img2, (0,0))
    world.draw()
    player.update()
    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             run = False

    pygame.display.update()

pygame.quit()
"""to do list
1. gör så att skärmen följer efter spelaren ( man kan ej se hela världen genom att stå stilla ) 
"""