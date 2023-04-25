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
        self.images_attack1_right = []
        self.images_attack1_left = []
        self.images_attackEffect = []
        self.index = 0
        self.attackEffect_index = 0
        self.counter = 0

        #animation
        #attack effect
        for num in range(0,10):
            img_attackEffect = pygame.image.load(f"characters/samurai/attack effect/attackeffect_{num}.png")
            img_attackEffect = pygame.transform.scale(img_attackEffect,(100,100))
            self.images_attackEffect.append(img_attackEffect)

        #attack1 and attack2
        for num in range(0,6):
            img_attack1_right = pygame.image.load(f"characters/samurai/attack1/{num}.png")
            if num < 4:
                img_attack1_right = pygame.transform.scale(img_attack1_right, (60, 80))
            if num > 3:
                img_attack1_right = pygame.transform.scale(img_attack1_right, (200, 80))
            self.images_attack1_right.append(img_attack1_right)
            img_attack1_left = pygame.transform.flip(img_attack1_right, True, False)
            self.images_attack1_left.append(img_attack1_left)
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
        self.image_attackEffect = self.images_attackEffect[self.attackEffect_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect_attack = self.image_attackEffect.get_rect()
        self.rect_attack.x = self.rect.x+100
        self.rect_attack.y = self.rect.y-5
        self.vel_y = 0
        self.jumped = False
        self.jumpedTimes = 0
        self.direction = 1
        self.idle = True
        self.inAir = False
        self.attacked = False
        self.attack_cooldown = 50
        self.attackCounter = 50

    #function for jumping

    def jump(self):
        self.inAir = True
        self.attacked = False
        self.vel_y = -7
        self.jumped = True
        self.jumpedTimes += 1
        if [pygame.K_SPACE] == False:
            self.jumped = False

    #fuction for attacking
    def attack(self):
        if self.inAir == False:
            self.attacked = True
            self.index = 0
            self.attackEffect_index = 0
            self.attackCounter = 0

    def update(self):
        #if the player is falling (gravity = 3) inAir = True
        if self.vel_y == 5:
            self.inAir = True
        #counts the attack cooldown
        if self.attackCounter < 50:
            self.attackCounter += 1

        dx = 0
        dy = 0
        if self.attacked:
            animation_cooldown = 4
        else:
            animation_cooldown = 7

        #get keypresses
        key = pygame.key.get_pressed()

        #movement
        if key[pygame.K_a]:
            if self.attacked == False:
                dx -= 3
                self.direction = -1

            self.counter += 1
            self.idle = False
        if key[pygame.K_d]:
            if self.attacked == False:
                dx += 3
                self.direction = 1

            self.counter += 1
            self.idle = False

        #if key a or d is not pushed down
        if key[pygame.K_a] == False and key[pygame.K_d] == False:
            self.counter += 1
            self.idle= True

        #animations
        #index and cooldowns between each image
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                 self.index = 0

            #facing right
            if self.inAir == False:
                #running right
                if self.direction == 1:
                    self.image = self.images_right[self.index]

                    #idle right
                    if self.idle:
                        self.image = self.images_idle_right[self.index]

                    #attack right
                    if self.attacked:
                        if self.index >= len(self.images_attack1_right):
                            self.index = 0
                            self.attacked = False

                        self.image = self.images_attack1_right[self.index]

                # facing left
                #running left
                if self.direction == -1:
                    self.image = self.images_left[self.index]

                    #idle left
                    if self.idle:
                        self.image = self.images_idle_left[self.index]

                    # attack left
                    if self.attacked:

                        if self.index >= len(self.images_attack1_right):
                            self.index = 0
                            self.attacked = False

                        self.image = self.images_attack1_left[self.index]
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

            #attack effect in both directions
        if self.counter > 2.5 and self.attackEffect_index < 10:
            self.attackEffect_index += 1
            if self.attacked:
                if self.attackEffect_index >= len(self.images_attackEffect):
                    self.attackEffect_index = 0
                self.image_attackEffect = self.images_attackEffect[self.attackEffect_index]

        #add gravity
        self.vel_y += 0.3
        if self.vel_y > 5:
            self.vel_y = 5
        dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            #check for collision in x-direction
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in y-direction
            if tile[1].colliderect(self.rect.x, self.rect.y+dy,self.width, self.height):

                #check if below the ground (jumping)
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0.0
                #check if above the ground (falling)
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.jumpedTimes = 0
                    self.vel_y = 0
                    self.inAir = False


        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        self.rect_attack.x += dx
        self.rect_attack.y += dy

        #draw player onto screen

        if self.direction == 1:
            self.rect_attack.x = self.rect.x + 100
        if self.direction == -1:
            self.rect_attack.x = self.rect.x - 140
        pygame.draw.rect(screen,(255,0,0),self.rect,1)
        pygame.draw.rect(screen, (255, 0, 0), self.rect_attack, 1)

        # denna kontroll måste göras eftersom bild 4 och 5 i attack ej är centrerade, detta gör så att när man kör flip funktionen
        # på dom så kommer spriten att flytta sig till andra sidan istället istället för att förbli centrerad som med andra sprites.
        if self.direction== -1 and self.attacked and self.index == 4:
            screen.blit(self.image, (self.rect.x-140,self.rect.y))

        elif self.direction== -1 and self.attacked and self.index == 5:
            screen.blit(self.image, (self.rect.x - 140, self.rect.y))
        else:
            screen.blit(self.image, self.rect)

        #attack effect
        if self.direction == 1 and self.attacked and self.inAir==False:
            screen.blit(self.image_attackEffect, (self.rect.x+100,self.rect.y-5))
        if self.direction == -1 and self.attacked and self.inAir==False:
            screen.blit(self.image_attackEffect, (self.rect.x-140,self.rect.y-5))

class World():
    def __init__(self, data):
        self.tile_list = []
        #block som ej ska ha någon collision
        self.tile_list_liquid = []
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
            pygame.draw.rect(screen, (255,255,255),tile[1],1)
world_data=[
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,1,1,1,2,2,1,0,0,0,0,0,0,0,0,0,0],
[1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,1,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1],
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
             break
        #jumping and doublejumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jumpedTimes <2:
                player.jump()
        #mouseclick
        mKey = pygame.mouse.get_pressed()

        if mKey[0]:
            if player.attackCounter >= player.attack_cooldown:
                player.attack()

    pygame.display.update()

pygame.quit()
"""to do list
1. gör så att skärmen följer efter spelaren ( man kan ej se hela världen genom att stå stilla ) 
2. fixa så att attack left inte flyttar på sig
3. för att undvika collision skapa en separat tile_list och använd den i def draw(self)
"""