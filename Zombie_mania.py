import pygame
from pygame.locals import *
import sys
import random
import time
import math

pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 800
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60
LOOP = True
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie mania")

#Importing images
PlayerImage = pygame.transform.scale((pygame.image.load("C:\\Users\\Rayan Kasam\\Documents\\MyCode\\Zombie Mania\\Player.png").convert_alpha()),((HEIGHT/7),(HEIGHT/7)))
ZombieImage = pygame.transform.scale((pygame.image.load("C:\\Users\\Rayan Kasam\\Documents\\MyCode\\Zombie Mania\\Zombie.png").convert_alpha()),((HEIGHT/7),(HEIGHT/7))) 
Background = pygame.image.load("C:\\Users\\Rayan Kasam\\Documents\\MyCode\\Zombie Mania\\Map_Backround.png").convert_alpha()
all_sprites = pygame.sprite.Group()
Zombies = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
def angle(Point1, Point2): # Gives angle between 2 points
    x_Point1, y_Point1 = Point1
    x_Point2, y_Point2 = Point2

    if x_Point1 - x_Point2 != 0:
            if (x_Point1 - x_Point2) < 0: # Was having issues with cases where delta x was negative so made an exception
                return(180+(180/math.pi)*(math.atan((-(y_Point1 - y_Point2))/(x_Point1 - x_Point2))))
            else:
                return((180/math.pi)*(math.atan((-(y_Point1 - y_Point2))/(x_Point1 - x_Point2))))
    else:
        return 90
def ZombieSpawn(wave):
    for x in range(wave+1):
        zomb = Zombie((0,0))
        C = True
        while C:
            rand = random.randint(1,4)
            
            if rand == 1:
                zomb.rect.center=(0,(random.uniform(0,HEIGHT)))  
            elif rand == 2:
                zomb.rect.center=((random.uniform(0,WIDTH)),0)
            elif rand == 3:
                zomb.rect.center=(WIDTH,(random.uniform(0,HEIGHT)))
            else:
                zomb.rect.center=((random.uniform(0,WIDTH)),HEIGHT)
            if pygame.sprite.spritecollideany(zomb,Zombies):
                C = True
            else:    
                for entity in all_sprites:
                    if entity == zomb:
                        continue
                    if (abs(zomb.rect.centerx - entity.rect.centerx) < 50) and (abs(zomb.rect.centery - entity.rect.centery) < 50):
                        C = True
                C = False
        all_sprites.add(zomb)
        Zombies.add(zomb)
def terminate():
    pygame.quit()
    sys.exit()
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = PlayerImage
        self.rect = self.image.get_rect(center = pos)
        self.angle = 0
        self.pos = vec((WIDTH/2, HEIGHT/2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
    def move(self):
        self.acc = vec(0,0)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC
        if pressed_keys[K_s]:
            self.acc.y = ACC
        if pressed_keys[K_w]:
            self.acc.y = -ACC
        self.acc.x += self.vel.x * FRIC
        self.vel.x += self.acc.x
        self.pos.x += self.vel.x + 0.5 * self.acc.x

        self.acc.y += self.vel.y * FRIC
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y

        self.image = pygame.transform.rotate(PlayerImage, angle(pygame.mouse.get_pos(),self.rect.center))
        self.rect.center = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
P1 = Player((100,100))
all_sprites.add(P1)
playerGroup.add(P1)
class Zombie(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = ZombieImage
        self.rect = self.image.get_rect(center = pos)
        self.angle = 0
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def move(self):
        self.acc = vec(0,0)
        if pygame.sprite.spritecollideany(self,bulletGroup):
            self.kill()
            P1.score += 1 
        theta = angle(self.rect.center,P1.rect.center) + 180

        self.pos.x, self.pos.y = self.rect.center

        self.acc.x = 0.5*math.sin(theta)
        self.acc.x += self.vel.x * FRIC
        self.vel.x += self.acc.x
        self.pos.x += self.vel.x + 0.5 * self.acc.x

        self.acc.y = 0.5*math.cos(theta)
        self.acc.y += self.vel.y * FRIC
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y

        self.image = pygame.transform.rotate(ZombieImage, theta)
        self.rect.center = self.pos
class bullet(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255,255,51))
        self.rect = self.surf.get_rect()
        self.pos = vec(position)

        t = (((pygame.mouse.get_pos()[1]-self.pos.y)**2)+((pygame.mouse.get_pos()[0]-self.pos.x)**2))**(1/2)
        scalar = (100**2/(t**2))

        theta =(180/math.pi)*(math.atan((pygame.mouse.get_pos()[1]-self.pos.y)/(pygame.mouse.get_pos()[0]-self.pos.x)))
        self.image = pygame.transform.rotate(self.surf,theta)

        self.vel = vec(scalar*(pygame.mouse.get_pos()[0]-self.pos.x),scalar*(pygame.mouse.get_pos()[1]-self.pos.y))
    def move(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        if self.pos.x > WIDTH or self.pos.x < 0 or self.pos.y > HEIGHT or self.pos.y < 0:
            self.kill()

        self.rect.center = self.pos
P1 = Player((100,100))
all_sprites.add(P1)
    
wave = 0
while LOOP:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            b = bullet(P1.pos)
            all_sprites.add(b)
            bulletGroup.add(b)
    f = pygame.font.SysFont("msgothic", 30)
    g = f.render(str(P1.score),True, (255,0,0))
    displaysurface.blit(g, (WIDTH-20, 10))
    text = f.render(("WAVE "+str(wave)),True, (255,255,255))
    displaysurface.blit(text, (0, 0))
    if(pygame.sprite.spritecollideany(P1,Zombies)): # Game Over
        
        


        displaysurface.fill((255,102,102))
        pygame.display.flip()
        
        for entity in all_sprites: # Sprite removal
            entity.kill()
        all_sprites.draw(displaysurface)
        font = pygame.font.SysFont("Verdana", 50)
        hsFont = pygame.font.SysFont("times new roman",20)
        text = font.render(str(("SCORE " + str(P1.score))),True, (255,255,255))

        highScoreRead = int((open("Zombie Mania\Highscore.txt","r")).readline())

        newHighScore = False
        highScore = 0
        if highScoreRead < P1.score:
            newHighScore = True
            highScore = P1.score

            highScoreWrite = open("Zombie Mania\Highscore.txt","w")
            highScoreWrite.write(str(P1.score))
            highScoreWrite.close() 
        else:
            highScore = highScoreRead
        if newHighScore:
            hsText = hsFont.render(str(f"NEW HIGHSCORE IS {highScore}!!!"),True, (255,255,255))
        else:
            hsText = hsFont.render(str(f"The highscore to beat is {highScore}"),True, (255,255,255))
        t = time.time()
        while (time.time()-t)<3:
            displaysurface.fill((255,102,102))
            displaysurface.blit(text, (WIDTH/3, (HEIGHT/2)-(HEIGHT/4)))
            displaysurface.blit(hsText, (WIDTH/3, (HEIGHT/2)))
            pygame.display.update()
        terminate()
        
    if len(Zombies) == 0:
        ZombieSpawn(wave)
        wave += 1
    for entity in all_sprites:
        entity.move()
    pygame.display.update()
    FramePerSec.tick(FPS)
    displaysurface.blit(Background,(0,0))
    all_sprites.draw(displaysurface)