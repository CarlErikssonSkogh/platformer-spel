import pygame
from pygame.locals import *

pygame.init()

screen_width = 1280
screen_height= 720

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Platformer")

#define game variables
tile_size = 80

#load images
bg_img = pygame.image.load("assets/background/background.png")
bg_img2 = pygame.image.load("assets/background/middleground.png")

def draw_grid():
    for line in range(0,16):
        if line <= 16:
            pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size),(screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, 1280))

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
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,1],
]

world = World(world_data)

run = True
while run:

    screen.blit(bg_img, (0,0))
    screen.blit(bg_img2, (0,0))

    world.draw()
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             run = False

    pygame.display.update()

pygame.quit()