import pygame
import pickle

try:
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = []

highscore_list = data

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
 #funktion for timer (points)
def Timer():
    global highscore_list
    #Calculate the time in seconds
    timer = pygame.time.get_ticks() // 1000
    #Check if the timer has reached 10 seconds
    if timer >= 60:
        #Calculate the number of minutes and seconds
        minutes = timer // 60
        seconds = timer % 60

        #If the seconds are less than 10, format them with a leading zero
        if seconds < 10:
            seconds_str = f"0{seconds}"
        else:
            seconds_str = str(seconds)

        #Format the timer string as "m:ss"
        timer = f"{minutes}:{seconds_str}"

    else:
        #Convert the timer value to a string
        timer = str(timer)

    #Render the timer label
    font = pygame.font.SysFont("Arial", 32)
    text_color = (255, 255, 255)
    timer_surface = font.render(f"Time:{timer}", True, text_color)
    scoreboard_surface = font.render(highscore_list,True,text_color)

    #Blit the timer label onto the screen
    screen.blit(timer_surface, (850, 175))
    screen.blit(scoreboard_surface, (850, 25))
    highscore_list = timer
class Enemy():
    class Enemy():
        def __init__(self):
            self.images_demon_right = []
            self.images_demon_left = []
            self.images_death = []
            self.index = 0
            self.demonDmg = 50
            self.demonHealth = 100
            self.demonDead = False
            self.demonDeadAnimations = True
            self.counter = 0
            self.imageDemon = None
            self.rectDemon = None
            self.turned = False
            self.vel_x = 2
            self.widthDemon = 0
            self.heightDemon = 0

        def demon(self, x, y):
            self.images_demon_right = []
            self.images_demon_left = []
            self.images_death = []
            self.index = 0
            self.demonDmg = 50
            self.demonHealth = 100
            self.demonDead = False
            self.demonDeadAnimations = True
            self.counter = 0
            #the tile that the demon starts in (the x coordinates)
            self.startTile=x

            for num in range(0, 4):
                demon_run_right = pygame.image.load(f"assets/demon/run/{num}.png")
                demon_run_right = pygame.transform.scale(demon_run_right, (60, 80))
                demon_run_left = pygame.transform.flip(demon_run_right, True, False)
                self.images_demon_right.append(demon_run_right)
                self.images_demon_left.append(demon_run_left)

            for num in range(0, 6):
                death = pygame.image.load(f"assets/death/{num}.png")
                death = pygame.transform.scale(death, (60, 80))
                self.images_death.append(death)

            self.imageDemon = self.images_demon_right[self.index]

            self.rectDemon = self.imageDemon.get_rect()
            self.rectDemon.x = x
            self.rectDemon.y = y
            self.turned = False
            self.vel_x = 2
            self.widthDemon = self.imageDemon.get_width()
            self.heightDemon = self.imageDemon.get_height()

        def demonAnimations(self):
            self.counter += 1
            animation_cooldown = 5

            if self.counter > animation_cooldown:
                self.counter = 0
                self.index += 1

                if self.demonDead == False:
                    if self.index >= len(self.images_demon_right):
                        self.index = 0

                    if self.turned == False:
                        self.imageDemon = self.images_demon_right[self.index]
                    if self.turned:
                        self.imageDemon = self.images_demon_left[self.index]

            if self.demonHealth <= 0:
                if self.index >= len(self.images_death):
                    self.demonDeadAnimations = False
                    self.index = 0

                self.imageDemon = self.images_death[self.index]
                self.demonDead = True

            if self.demonDeadAnimations:
                screen.blit(self.imageDemon, self.rectDemon)

        def update(self):
            self.demonAnimations()
            #changes the end coordinates for the demon depending on where it started
            if self.startTile == 8 * tile_size or 9 * tile_size:
                endTile = 15 * tile_size
            if self.startTile == 2 * tile_size:
                endTile = 5 * tile_size
            if self.startTile == 22 * tile_size:
                endTile = 24 * tile_size


            if not self.demonDead:
                if self.turned == False:
                    if self.rectDemon.x <= endTile:
                        self.rectDemon.x += self.vel_x
                    else:
                        self.turned = True
                if self.turned:
                    if self.rectDemon.x >= self.startTile:
                        self.rectDemon.x -= self.vel_x
                    else:
                        self.turned = False

    #creates two instances of the enemy class (creates two demons at different coordinates)
    demon1 = Enemy()
    demon1.demon(9 * tile_size, 480)

    #Creates the second demon
    demon2 = Enemy()
    demon2.demon(8 * tile_size, screen_height-8*tile_size)

    #Creates the third demon
    demon3 = Enemy()
    demon3.demon(2 * tile_size, screen_height - 10 * tile_size)

    #Creates the fiourth demon
    demon4 = Enemy()
    demon4.demon(22 * tile_size, screen_height - 13 * tile_size)

class Combat():
    def __init__(self):
        self.hitCounterDemon = 0
        self.hitCounterPlayer = 0

    def update(self):
        if self.hitCounterDemon < 50:
            self.hitCounterDemon += 1
        if self.hitCounterPlayer < 50:
            self.hitCounterPlayer += 1
        hitCooldown = 50

        #Combat with demon1
        if self.hitCounterDemon >= hitCooldown:
            if not enemy.demon1.demonDead:
                if player.rect.colliderect(enemy.demon1.rectDemon.x, enemy.demon1.rectDemon.y, enemy.demon1.widthDemon, enemy.demon1.heightDemon):
                    self.hitCounterDemon = 0
                    player.health -= enemy.demon1.demonDmg
                    #Prevents the player from dashing through the enemy at high speed
                    player.dx = 0
                    if enemy.demon1.turned == False:
                        enemy.demon1.turned = True
                        enemy.demon1.rectDemon.x -= 20
                        player.rect.x += 50
                    else:
                        enemy.demon1.turned = False
                        enemy.demon1.rectDemon.x += 20
                        player.rect.x -= 50

        if self.hitCounterPlayer >= hitCooldown:
            if player.rect_attack.colliderect(enemy.demon1.rectDemon.x, enemy.demon1.rectDemon.y, enemy.demon1.widthDemon, enemy.demon1.heightDemon) and player.attacked:
                self.hitCounterPlayer = 0
                enemy.demon1.demonHealth -= player.playerDmg
                print(enemy.demon1.demonHealth)

        #Combat with demon2
        if self.hitCounterDemon >= hitCooldown:
            if not enemy.demon2.demonDead:
                if player.rect.colliderect(enemy.demon2.rectDemon.x, enemy.demon2.rectDemon.y, enemy.demon2.widthDemon, enemy.demon2.heightDemon):
                    self.hitCounterDemon = 0
                    player.health -= enemy.demon2.demonDmg
                    #Prevents the player from dashing through the enemy at high speed
                    player.dx = 0
                    if enemy.demon2.turned == False:
                        enemy.demon2.turned = True
                        enemy.demon2.rectDemon.x -= 20
                        player.rect.x += 50
                    else:
                        enemy.demon2.turned = False
                        enemy.demon2.rectDemon.x += 20
                        player.rect.x -= 50

        if self.hitCounterPlayer >= hitCooldown:
            if player.rect_attack.colliderect(enemy.demon2.rectDemon.x, enemy.demon2.rectDemon.y, enemy.demon2.widthDemon, enemy.demon2.heightDemon) and player.attacked:
                self.hitCounterPlayer = 0
                enemy.demon2.demonHealth -= player.playerDmg

        # Combat with demon3
        if self.hitCounterDemon >= hitCooldown:
            if not enemy.demon3.demonDead:
                if player.rect.colliderect(enemy.demon3.rectDemon.x, enemy.demon3.rectDemon.y,enemy.demon3.widthDemon, enemy.demon3.heightDemon):
                    self.hitCounterDemon = 0
                    player.health -= enemy.demon3.demonDmg
                    # Prevents the player from dashing through the enemy at high speed
                    player.dx = 0
                    if enemy.demon3.turned == False:
                        enemy.demon3.turned = True
                        enemy.demon3.rectDemon.x -= 20
                        player.rect.x += 50
                    else:
                        enemy.demon3.turned = False
                        enemy.demon3.rectDemon.x += 20
                        player.rect.x -= 50

        if self.hitCounterPlayer >= hitCooldown:
            if player.rect_attack.colliderect(enemy.demon3.rectDemon.x, enemy.demon3.rectDemon.y,enemy.demon3.widthDemon,enemy.demon3.heightDemon) and player.attacked:
                self.hitCounterPlayer = 0
                enemy.demon3.demonHealth -= player.playerDmg

        #Combat with demon4
        if self.hitCounterDemon >= hitCooldown:
            if not enemy.demon4.demonDead:
                if player.rect.colliderect(enemy.demon4.rectDemon.x, enemy.demon4.rectDemon.y,enemy.demon4.widthDemon, enemy.demon4.heightDemon):
                    self.hitCounterDemon = 0
                    player.health -= enemy.demon4.demonDmg
                    # Prevents the player from dashing through the enemy at high speed
                    player.dx = 0
                    if enemy.demon4.turned == False:
                        enemy.demon4.turned = True
                        enemy.demon4.rectDemon.x -= 20
                        player.rect.x += 50
                    else:
                        enemy.demon4.turned = False
                        enemy.demon4.rectDemon.x += 20
                        player.rect.x -= 50

        if self.hitCounterPlayer >= hitCooldown:
            if player.rect_attack.colliderect(enemy.demon4.rectDemon.x, enemy.demon4.rectDemon.y,enemy.demon4.widthDemon,enemy.demon4.heightDemon) and player.attacked:
                self.hitCounterPlayer = 0
                enemy.demon4.demonHealth -= player.playerDmg
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
        self.images_dash_right = []
        self.images_dash_left = []
        self.index = 0
        self.attackEffect_index = 0
        self.dash_index = 0
        self.counter = 0
        self.dx = 0
        self.dy = 0
        self.dashed = False
        self.health = 200
        self.playerDmg = 50

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

        #dash
        for num in range (0, 6):
            img_dash_left = pygame.image.load(f"characters/samurai/dash/{num}.png")
            img_dash_left = pygame.transform.scale(img_dash_left, (60, 80))
            img_dash_right = pygame.transform.flip(img_dash_left, True, False)
            self.images_dash_right.append(img_dash_right)
            self.images_dash_left.append(img_dash_left)

        self.image = self.images_idle_right[self.index]
        self.image_attackEffect = self.images_attackEffect[self.attackEffect_index]
        self.image_dash = self.images_dash_right[self.dash_index]
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
        self.dash_duration = 200
        self.attackCounter = 50
        self.dash_counter = 0

    def healthbar(self,x,y):
        self.healthbarRect_x=x
        self.healthbarRect_y=y
        self.healthbarHeight=35
        self.healthbarColor=(255,0,0)

        pygame.draw.rect(screen, self.healthbarColor, (self.healthbarRect_x, self.healthbarRect_y, self.health,self.healthbarHeight))
        pygame.draw.rect(screen, (0,0,0),(self.healthbarRect_x, self.healthbarRect_y, 200, self.healthbarHeight),5)
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
    #function for dashing
    def dash(self):
        self.dash_index = 0
        if self.dash_counter <= 0 and self.dashed == False:
            self.vel_y = 0
            self.dashed = True
            if self.direction == 1:
                self.dx = 20
            if self.direction == -1:
                self.dx = -20



    def update(self):
        player.healthbar(50, 15)
        Timer()
        #if the player is falling (gravity = 3) inAir = True
        if self.vel_y == 5:
            self.inAir = True

        #counts the attack cooldown
        if self.attackCounter < 50:
            self.attackCounter += 1
        if self.dashed == False:
            self.dx = 0
            self.dy = 0
        if self.attacked:
            animation_cooldown = 4
        if self.dashed:
            animation_cooldown = 3
        else:
            animation_cooldown = 7

        #get keypresses
        key = pygame.key.get_pressed()

        #movement
        if key[pygame.K_a]:
            if self.attacked == False and self.dashed == False:
                self.dx = -3
                self.direction = -1

            self.counter += 1
            self.idle = False
        if key[pygame.K_d]:
            if self.attacked == False and self.dashed == False:
                self.dx = 3
                self.direction = 1

            self.counter += 1
            self.idle = False

        #if key a or d is not pushed down
        if key[pygame.K_a] == False and key[pygame.K_d] == False:
            self.counter += 1
            self.idle= True

        #limits dashing
        if self.dashed:
            self.dash_counter += 20
            if self.dash_counter > self.dash_duration:
                self.dashed = False

        if self.dashed == False:
            self.dash_counter -= 1
            if self.dash_counter <= 0:
                self.dash_counter = 0

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
        if self.counter > 2.5 and self.attackEffect_index < len(self.images_attackEffect):
            self.attackEffect_index += 1
            if self.attacked:
                if self.attackEffect_index >= len(self.images_attackEffect):
                    self.attackEffect_index = 0
                self.image_attackEffect = self.images_attackEffect[self.attackEffect_index]
        #dashing in both directions
        if self.dashed:
            if self.dash_counter > animation_cooldown and self.dash_index < len(self.images_dash_right):
                self.dash_index += 1
                if self.dash_index >= len(self.images_dash_right):
                    self.dash_index = 0
                if self.direction == 1:
                    self.image_dash = self.images_dash_right[self.dash_index]
                if self.direction == -1:
                    self.image_dash = self.images_dash_left[self.dash_index]

        #add gravity
        if self.dashed == False:
            self.vel_y += 0.3
        if self.vel_y > 5:
            self.vel_y = 5
        self.dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            #check for collision in x-direction
            if tile[1].colliderect(self.rect.x+self.dx, self.rect.y, self.width, self.height):
               self. dx = 0
            #check for collision in y-direction
            if tile[1].colliderect(self.rect.x, self.rect.y+self.dy,self.width, self.height):

                #check if below the ground (jumping)
                if self.vel_y < 0:
                    self.dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0.0
                #check if above the ground (falling)
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    self.jumpedTimes = 0
                    self.vel_y = 0
                    self.inAir = False


        #update player coordinates
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.rect_attack.x += self.dx
        self.rect_attack.y += self.dy

        #draw player onto screen
        if self.direction == 1:
            self.rect_attack.x = self.rect.x + 100
        if self.direction == -1:
            self.rect_attack.x = self.rect.x - 140
        pygame.draw.rect(screen,(255,0,0),self.rect,1)
        pygame.draw.rect(screen, (255, 0, 0), self.rect_attack, 1)

        #denna kontroll måste göras eftersom bild 4 och 5 i attack ej är centrerade, detta gör så att när man kör flip funktionen
        #på dom så kommer spriten att flytta sig till andra sidan istället istället för att förbli centrerad som med andra sprites.
        if self.direction== -1 and self.attacked and self.index == 4:
            screen.blit(self.image, (self.rect.x-140,self.rect.y))

        elif self.direction== -1 and self.attacked and self.index == 5:
            screen.blit(self.image, (self.rect.x - 140, self.rect.y))
        else:
            screen.blit(self.image, self.rect)

        #dash
        if self.dashed:
            if self.direction == 1:
                screen.blit(self.image_dash,(self.rect.x-50,self.rect.y))
            if self.direction == -1:
                screen.blit(self.image_dash, (self.rect.x + 50, self.rect.y))

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

world_data=[
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,1,2,1,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,1,0,0],
[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1],
]

#instances
player = Player(100, screen_height-40)
enemy = Enemy()
combat = Combat()
world = World(world_data)

run = True
while run:
    clock.tick(60)
    screen.blit(bg_img, (0,0))
    screen.blit(bg_img2, (0,0))
    world.draw()
    player.update()
    # Update logic
    enemy.demon1.update()
    enemy.demon2.update()
    enemy.demon3.update()
    enemy.demon4.update()

    # Render
    screen.blit(screen, (0, 0))


    combat.update()

    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             run = False
             break
        #jumping and doublejumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jumpedTimes <2:
                player.jump()
            #if e is pressed the player should dash
            if event.key == pygame.K_e:
                player.dash()
        #mouseclick
        mKey = pygame.mouse.get_pressed()

        if mKey[0]:
            if player.attackCounter >= player.attack_cooldown:
                player.attack()

    pygame.display.update()
pygame.quit()
data = highscore_list
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)
