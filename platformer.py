import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height= 600

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
        img = pygame.image.load("characters/samurai/Idle/00_Idle.png")
        self.image = pygame.transform.scale(img, (100,120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def update(self):
        dx = 0
        dy = 0
        #get keypresses
        key = pygame.key.get_pressed()
        if self.rect.bottom == screen_height:
            if key[pygame.K_SPACE] and self.jumped == False:
                    self.vel_y = -15
                    self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_a]:
            dx -= 3
        if key[pygame.K_d]:
            dx += 3

        #add gravity
        self.vel_y += 1
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
player = Player(100, screen_height-140)
world = World(world_data)

run = True
while run:

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