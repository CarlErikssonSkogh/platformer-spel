import pygame, pickle


try:
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = []

highscore_list = data
from pygame.locals import *
pygame.init()

#variables
screen_width = 1000
screen_height= 600
name = ""
active=highscoreFlag=False
menueDone=False
y_spacing=20
timerStart = 0
finishedGame=False


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

def Name():
    global name, active, menueDone
    font = pygame.font.SysFont("Arial",50)
    controlsFont = pygame.font.SysFont("Arial", 28)
    text_color = (0, 0, 0)
    input_surface = font.render(f"Name:{name}", True, text_color)
    background = pygame.Rect(0,0,1000,600)
    instructions_surface = font.render("Press Enter When Done", True, text_color)
    controls_surface = controlsFont.render("E = Dash, A = Move left, D = Move right, SPACE = Jump/Doublejump, M1 = attack", True, text_color)
    objective_text = "Your objective is to eliminate all the monsters and escape through the door"
    objective_surface = controlsFont.render(objective_text, True, text_color)

    #blits the name box in the middle of the screen
    name_width, name_height = input_surface.get_size()
    instructions_width, instructions_height = instructions_surface.get_size()

    name_x = (screen_width - name_width) // 2
    name_y = (screen_height - name_height) // 2
    instructions_x = (screen_width - instructions_width) // 2
    instructions_y = (screen_width - instructions_width) // 2

    input_rect = pygame.Rect(name_x,name_y, input_surface.get_width(), input_surface.get_height())

    pygame.draw.rect(screen, (255, 255, 255), background)
    screen.blit(controls_surface, (90, 0))
    screen.blit(objective_surface, (60, 100))
    screen.blit(input_surface, (name_x, name_y))
    screen.blit(instructions_surface,(instructions_x, instructions_y+100))
    pygame.draw.rect(screen, text_color, input_rect, 1)



    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if input_rect.collidepoint(mouse_pos):
        if mouse_click[0] == 1:  #Left mouse button clicked
            active = True

    if active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Name entered:", name)
                    active = False
                    menueDone = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name)<7:
                    name += event.unicode

#function for timer (points)
def Timer():
    global timer, timerStart
    #Calculate the time in seconds

    #timerStart prevents the timer from going when in the menue
    if menueDone == False:
        timerStart = pygame.time.get_ticks() // 1000
    if menueDone and finishedGame == False:
        timer = pygame.time.get_ticks() // 1000 - timerStart
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
        #Blit the timer label onto the screen
        screen.blit(timer_surface, (850, 175))



def highscoreList():
    global timer, name, highscore_list

    #sorts the highscore
    #if enemy.allDemonsDead:

    if len(highscore_list)==0:
        highscore_list = [[name,timer]]
    else:
        highscore_list.append([name,timer])


    #saves highscore in a pickle file
    data = highscore_list
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)



#draws highscore on the screen
def blitHighscore():
    global highscore_list, y_spacing
    font = pygame.font.SysFont("Arial", 20)
    text_color = (255, 255, 255)
    list_rect = pygame.Rect(870, 0, 200, 250)
    name_surface = font.render("Name", True, text_color)
    time_surface = font.render("Time", True, text_color)

    for i in range(len(highscore_list)):
        scoreboard_surface = font.render(f"{i+1}:   {highscore_list[i][0]} : {highscore_list[i][1]}", True, text_color)
        screen.blit(scoreboard_surface, (835, 25 + i * 20))
        y_spacing += 20

    screen.blit(name_surface, list_rect)
    screen.blit(time_surface, (list_rect.x + 75, list_rect.y))

#sort highscore_list
def sort_highscore_list():
    global highscore_list
    for i in range(len(highscore_list)):
        for j in range(i + 1, len(highscore_list)):
            if highscore_list[i][1] > highscore_list[j][1]:
                highscore_list[i], highscore_list[j] = highscore_list[j], highscore_list[i]
    #List can't contain more than 5 lists
    if len(highscore_list) == 6:
        highscore_list.pop(5)

#blits the endscreen with congratulations, time, name and placement
def blitEndScreen():
    global highscore_list, timer
    font = pygame.font.SysFont("Arial", 32)
    text_color = (0, 0, 0)
    background = pygame.Rect(0, 0, 1000, 600)
    congrats_surface = font.render("Congratulations", True, text_color)
    name_surface = font.render(f"Name: {name}", True, text_color)
    time_surface = font.render(f"Time: {timer}", True, text_color)
    for index in range(len(highscore_list)):
        if name in highscore_list[index][0]:
            placement_surface = font.render(f"You placed in the top {index+1}", True, text_color)
        else:
            placement_surface = font.render(f"You didn't reach the leaderboard", True, text_color)

    #blits everything in the middle
    congrats_width, congrats_height = congrats_surface.get_size()

    congrats_x = (screen_width - congrats_width) // 2
    congrats_y = (screen_height - congrats_height) // 2

    pygame.draw.rect(screen,(255,255,255),background)
    screen.blit(congrats_surface,(congrats_x,congrats_y))
    screen.blit(time_surface,(congrats_x,congrats_y+150))
    screen.blit(name_surface, (congrats_x, congrats_y+100))
    screen.blit(placement_surface, (congrats_x, congrats_y+200))

def Door():
    global timer,  highscoreFlag, finishedGame
    #draws the door
    rectCoordinates = (tile_size*23,screen_height-13.5*tile_size)
    rectSize = (2*tile_size,2.5*tile_size)
    if enemy.allDemonsDead:
        color=(255,255,255)
    else:
        color=(0,0,0)
    pygame.draw.rect(screen,color,(rectCoordinates,rectSize))
    pygame.draw.rect(screen, (0,0,0), (rectCoordinates, rectSize),5)

    #if player collides with door
    if player.rect.colliderect(rectCoordinates, rectSize):
        if enemy.allDemonsDead:
            if highscoreFlag == False:
                highscoreList()
                finishedGame=True
                highscoreFlag = True







class Enemy():
    def __init__(self):
        self.allDemonsDead = False
    def demon(self, x, y):
        self.turned = False
        self.widthDemon = 0
        self.heightDemon = 0
        self.imageDemon = None
        self.rectDemon = None
        self.images_demon_right = []
        self.images_demon_left = []
        self.images_death = []
        self.index = 0
        self.demonDmg = 50
        self.demonHealth = 100  # ska vara 100
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
        self.vel_x=2
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
        #movementspeed
        #if the demon is within 200 pixels of the player and on the same y-coordinate it will get double the movementspeed
        if self.rectDemon.x-player.rect.x < 0 and self.rectDemon.x-player.rect.x >= -200 and self.rectDemon.y==player.rect.y:
            self.vel_x =4
        elif self.rectDemon.x-player.rect.x > 0 and self.rectDemon.x-player.rect.x <= 200 and self.rectDemon.y==player.rect.y:
            self.vel_x =4
        else:
            self.vel_x = 2
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
        if player.death==False:
            if self.hitCounterDemon < 50:
                self.hitCounterDemon += 1
            if self.hitCounterPlayer < 50:
                self.hitCounterPlayer += 1
            hitCooldown = 50

            #Combat with demon1
            if self.hitCounterDemon >= hitCooldown:
                if not demon1.demonDead:
                    if player.rect.colliderect(demon1.rectDemon.x, demon1.rectDemon.y, demon1.widthDemon, demon1.heightDemon):
                        self.hitCounterDemon = 0
                        player.health -= demon1.demonDmg
                        #Prevents the player from dashing through the enemy at high speed
                        player.dx = 0
                        if demon1.turned == False:
                            demon1.turned = True
                            demon1.rectDemon.x -= 20
                            player.rect.x += 50
                        else:
                            demon1.turned = False
                            demon1.rectDemon.x += 20
                            player.rect.x -= 50

            if self.hitCounterPlayer >= hitCooldown:
                if player.rect_attack.colliderect(demon1.rectDemon.x, demon1.rectDemon.y, demon1.widthDemon, demon1.heightDemon) and player.attacked:
                    self.hitCounterPlayer = 0
                    demon1.demonHealth -= player.playerDmg

            #Combat with demon2
            if self.hitCounterDemon >= hitCooldown:
                if not demon2.demonDead:
                    if player.rect.colliderect(demon2.rectDemon.x, demon2.rectDemon.y, demon2.widthDemon, demon2.heightDemon):
                        self.hitCounterDemon = 0
                        player.health -= demon2.demonDmg
                        #Prevents the player from dashing through the enemy at high speed
                        player.dx = 0
                        if demon2.turned == False:
                            demon2.turned = True
                            demon2.rectDemon.x -= 20
                            player.rect.x += 50
                        else:
                            demon2.turned = False
                            demon2.rectDemon.x += 20
                            player.rect.x -= 50

            if self.hitCounterPlayer >= hitCooldown:
                if player.rect_attack.colliderect(demon2.rectDemon.x, demon2.rectDemon.y, demon2.widthDemon, demon2.heightDemon) and player.attacked:
                    self.hitCounterPlayer = 0
                    demon2.demonHealth -= player.playerDmg

            # Combat with demon3
            if self.hitCounterDemon >= hitCooldown:
                if not demon3.demonDead:
                    if player.rect.colliderect(demon3.rectDemon.x, demon3.rectDemon.y,demon3.widthDemon, demon3.heightDemon):
                        self.hitCounterDemon = 0
                        player.health -= demon3.demonDmg
                        # Prevents the player from dashing through the enemy at high speed
                        player.dx = 0
                        if demon3.turned == False:
                            demon3.turned = True
                            demon3.rectDemon.x -= 20
                            player.rect.x += 50
                        else:
                            demon3.turned = False
                            demon3.rectDemon.x += 20
                            player.rect.x -= 50

            if self.hitCounterPlayer >= hitCooldown:
                if player.rect_attack.colliderect(demon3.rectDemon.x, demon3.rectDemon.y,demon3.widthDemon,demon3.heightDemon) and player.attacked:
                    self.hitCounterPlayer = 0
                    demon3.demonHealth -= player.playerDmg

            #Combat with demon4
            if self.hitCounterDemon >= hitCooldown:
                if not demon4.demonDead:
                    if player.rect.colliderect(demon4.rectDemon.x, demon4.rectDemon.y,demon4.widthDemon, demon4.heightDemon):
                        self.hitCounterDemon = 0
                        player.health -= demon4.demonDmg
                        # Prevents the player from dashing through the enemy at high speed
                        player.dx = 0
                        if demon4.turned == False:
                            demon4.turned = True
                            demon4.rectDemon.x -= 20
                            player.rect.x += 50
                        else:
                            demon4.turned = False
                            demon4.rectDemon.x += 20
                            player.rect.x -= 50

            if self.hitCounterPlayer >= hitCooldown:
                if player.rect_attack.colliderect(demon4.rectDemon.x, demon4.rectDemon.y,demon4.widthDemon,demon4.heightDemon) and player.attacked:
                    self.hitCounterPlayer = 0
                    demon4.demonHealth -= player.playerDmg
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
        self.images_death_right = []
        self.images_death_left = []
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

        #death
        for num in range(0, 6):
            img_death_right = pygame.image.load(f"characters/samurai/death/{num}.png")
            img_death_right = pygame.transform.scale(img_death_right, (80, 80))
            img_death_left = pygame.transform.flip(img_death_right, True, False)
            self.images_death_right.append(img_death_right)
            self.images_death_left.append(img_death_left)

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
        self.death = False
        self.respawnTimer = 0

        self.deathFlag=True

    def healthbar(self,x,y):
        self.healthbarRect_x=x
        self.healthbarRect_y=y
        self.healthbarHeight=35
        self.healthbarColor=(255,0,0)

        pygame.draw.rect(screen, self.healthbarColor, (self.healthbarRect_x, self.healthbarRect_y, self.health,self.healthbarHeight))
        pygame.draw.rect(screen, (0,0,0),(self.healthbarRect_x, self.healthbarRect_y, 200, self.healthbarHeight),5)

    #function that activates when the player dies
    def playerDeath(self):
        respawnCooldown=20
        self.respawnTimer += 0.1

        self.dashed = False #is needed because player continues dash while dead otherwise

        #label with respawn timer
        font = pygame.font.SysFont("Arial", 50)
        text_color = (255, 255, 255)
        respawnTimer_surface = font.render(f"Respawn: {round(20-self.respawnTimer,1)}", True, text_color)
        text_width, text_height = respawnTimer_surface.get_size()
        text_x = (screen_width - text_width) // 2
        text_y = (screen_height - text_height) // 2
        screen.blit(respawnTimer_surface, (text_x, text_y))

        #deathFlag only occurs once even though playerDeath is called in a while loop ( in update() )
        if self.deathFlag:
            self.index=0
            self.death = True
            self.deathFlag = False
        if self.respawnTimer >= respawnCooldown:
            self.death = False

            #Reset enemy positions and attributes
            demon1.demon(9 * tile_size, 480)
            demon2.demon(8 * tile_size, screen_height - 8 * tile_size)
            demon3.demon(2 * tile_size, screen_height - 10 * tile_size)
            demon4.demon(22 * tile_size, screen_height - 13 * tile_size)

            #reset player
            player.rect.x = 100
            player.rect.y = screen_height - 40
            player.health = 200
            player.rect_attack.y = self.rect.y - 5
            player.dx = 0
            player.vel_y=0

            #resets timer and flag
            self.respawnTimer=0
            self.deathFlag = True

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
        if self.death:
            animation_cooldown = 10
        else:
            animation_cooldown = 7

        #get keypresses
        key = pygame.key.get_pressed()

        #movement

        if self.death==False:
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


                self.idle = False

            #if key a or d is not pushed down
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
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
        self.counter += 1
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
            if self.inAir and self.death==False:
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
        if self.dashed and self.death==False:
            if self.dash_counter > animation_cooldown and self.dash_index < len(self.images_dash_right):
                self.dash_index += 1
                if self.dash_index >= len(self.images_dash_right):
                    self.dash_index = 0
                if self.direction == 1:
                    self.image_dash = self.images_dash_right[self.dash_index]
                if self.direction == -1:
                    self.image_dash = self.images_dash_left[self.dash_index]
        #death animation
        if self.death:

            if self.index >= len(self.images_death_right):
                self.index=5
            if self.direction == 1:
                self.image = self.images_death_right[self.index]
            if self.direction == -1:
                self.image = self.images_death_left[self.index]

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
            self.rect_attack.x = self.rect.x + 60
        if self.direction == -1:
            self.rect_attack.x = self.rect.x - 100


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
[2,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,1,0,2],
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
    Door()
    Timer()
    player.update()
    sort_highscore_list()
    blitHighscore()
    if player.health<=0:
        player.playerDeath()

    #updates every demon
    demon1.update()
    demon2.update()
    demon3.update()
    demon4.update()
    if menueDone == False:
        Name()
    #checks if all the demons are dead
    if demon1.demonDead and demon2.demonDead and demon3.demonDead and demon4.demonDead:
        enemy.allDemonsDead = True
    #Render
    screen.blit(screen, (0, 0))


    combat.update()

    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             run = False
             break
        if player.death==False:
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
    if finishedGame:
        blitEndScreen()

    pygame.display.update()
pygame.quit()
print(highscore_list)

"""Fixa:minuter fungerar ej på scorebaord då den tror att 1:01 minuter < 10 sekunder"""
