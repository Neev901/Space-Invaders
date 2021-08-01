import pygame,random,math
from random import choice
from pygame import mixer
#Initialize Pygame
pygame.init()
#Create A Screen
screen = pygame.display.set_mode((1900,1000))
background = pygame.image.load('bg.jpg')

#BG SOUND
# mixer.music.load('background.wav')
# mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invader!")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

#Player
playerIMG = pygame.image.load('spaceship2.png')    
playerX = 920
playerY = 850

playerX_change = 0

#Enemy
enemy_IMGs = []
enemyXs = []
enemyYs = []
enemyX_changes = []
enemyY_changes = []
enemy_movable = [] 

for i in range(10):
    choices = [pygame.image.load('enemy.png'),pygame.image.load('enemy2.png')]
    enemy_IMGs.append(choice(choices))
    enemyXs.append(random.randint(21,1765))
    enemyYs.append(random.randint(50,149))
    enemyX_changes.append(4)
    enemyY_changes.append(80)
    enemy_movable.append(True)

#Enemy
#Ready - You cannot see the bullet on the screen
#Fire - The bullet is moving
bulletIMG = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 850
bulletY_change = 5  
bulletState = "ready"
score_val = 0
noe = 10

font = pygame.font.Font('freesansbold.ttf', 40)

def show_score(x,y):
    score = font.render("Score : " + str(score_val), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerIMG, (x,y))

def enemy(x,y,i):
    screen.blit(enemy_IMGs[i], (x,y))

def fire(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletIMG,(x+30,y+50))

def collide(enemyX,enemyY,bulletX,bulletY):
    d = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))  
    if d < 80:
        return True  

#Game Loop
running = True

while running:

    #RGB Setter
    screen.fill((0,0,0))
    #Background Image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #?to check if the keystroke pressed it right arrow key or the left arrow key
        if event.type == pygame.KEYDOWN:#?KEYDOWN --> KEYSTROKE(Pressing the key)
            if event.key == pygame.K_LEFT:
                playerX_change = -2.6

            if event.key == pygame.K_RIGHT:
                playerX_change = 2.6
            
            if bulletY == 850:
                if event.key == pygame.K_SPACE:
                    if bulletState == "ready":
                        bsound = mixer.Sound('laser.wav')   
                        bsound.play()
                        bulletX = playerX
                        fire(bulletX,bulletY)
            
             
    playerX += playerX_change     

    for i in range(noe):
        if enemy_movable[i] == True:
            if enemyXs[i] <= 20:
                enemyX_changes[i] = 4
                enemyYs[i] += enemyY_changes[i]

            elif enemyXs[i] >= 1766:
                enemyX_changes[i] = -4
                enemyYs[i] += enemyY_changes[i]
            
            enemy(enemyXs[i],enemyYs[i],i)
            enemyXs[i] += enemyX_changes[i] 
            collvar = collide(enemyXs[i],enemyYs[i],bulletX,bulletY)  
            govar = collide(enemyXs[i],enemyYs[i],playerX,playerY) 

        if govar:
            running = False        

        if collvar:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 850
            bulletState = "ready"
            score_val+=1
            enemy_movable[i] = False 
        
        for i in range(len(enemy_movable)):
            if enemy_movable[i] is True:
                break

            elif i == len(enemy_movable)-1:
                running = False

    if playerX <= 20:
        playerX = 20

    elif playerX >= 1766:
        playerX = 1766

    if bulletY <= 0:
        bulletY = 850
        bulletState = "ready"
        
    if bulletState == "fire":
        fire(bulletX,bulletY)
        bulletY -= bulletY_change
    player(playerX,playerY)
    show_score(10,10)
    pygame.display.update()