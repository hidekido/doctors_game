import pygame
from pygame import *
from block import *
from player import *
from pygame.locals import *
import os
import random
import math


WINHEIGHT = 768
WINWIDTH = 1024
width = 1024
height = 768
DISPLAY = (WINWIDTH, WINHEIGHT)
BACKGROUND_COLOR = "#444444"
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption('Start menu')
clock = pygame.time.Clock()
bg = Surface((WINWIDTH,WINHEIGHT))
activegame = True

entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться

DIR = os.path.dirname(__file__)
total_level_width = 1
total_level_height = 1
energy_color = "#1fd3dc"
black = (0,0,0)
white = (255,255,255)
red = (255,56,85)
green = (79,255,175)
bright_red = (255,81,90)
bright_green = (142,255,200)





class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WINWIDTH / 2, -t+WINHEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WINWIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WINHEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h) 

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)



def lvlinit():
    l = random.randint(0,2)
    levels = ["%s\\levels\\1.txt","%s\\levels\\2.txt","%s\\levels\\3.txt"]
    f = open(levels[l] % DIR, 'r')
    level = []
    line = f.readline()
    while line != '':
        if line[-1] == '\"':
            line = line[1:-1]
        else:
            line = line[1:-2]
        level += [line]
        line = f.readline()
    x = y = 0 # координаты
    b = random.randint(0,2) #номер блока
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y,b)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

def closegame():
    global activegame 
    activegame = False

def main():
    entities.empty()
    platforms.clear()
    timer = pygame.time.Clock()
    pygame.display.set_caption("Amazing Doctor Strange")
    bg.fill(Color(BACKGROUND_COLOR))
    hero = Player(55,55) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = False
    portalFaze = 0
    global activegame
    entities.add(hero)
    lvlinit()
    camera = Camera(camera_configure, total_level_width, total_level_height)
    portalin = None
    energy = 20
    av_portals = 3
    cr_time = 0
    portalout = None
    portalsLife = None
    timer.tick(10000)
    click = [0,0,0]
    score = 0
    lives = 3
    pygame.event.clear()
    while activegame:
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if portalFaze == 1:
                entities.remove(portalin)
                platforms.remove(portalin)
            elif portalFaze ==2:
                entities.remove(portalin)
                platforms.remove(portalin)
                entities.remove(portalout)
                platforms.remove(portalout)
                portalout = None
            portalin = BlockTeleport(mouse[0]-32,mouse[1]-48)
            if portalin.collide(platforms) == False and av_portals > 0:
                platforms.append(portalin)
                entities.add(portalin)
                portalFaze = 1
            else:
                portalFaze = 0
                portalin = None
        
        if click[2] == 1:
            if portalFaze == 1:
                portalout = BlockTeleport(mouse[0]-32,mouse[1]-48,portalin.truex,portalin.truey,1)
                if portalout.collide(platforms) == False and av_portals > 0 :
                    portalin.act = 1
                    portalin.goX = mouse[0]-32
                    portalin.goY = mouse[1]-48
                    portalin.alter = portalout
                    portalout.alter = portalin
                    platforms.append(portalout)
                    entities.add(portalout)
                    portalFaze = 2
                    portalsLife = 600
                    av_portals -= 1
                else:
                    portalout = None

        if portalsLife != None:
            portalsLife -= 1
            if portalsLife<=0:
                entities.remove(portalin)
                platforms.remove(portalin)
                entities.remove(portalout)
                platforms.remove(portalout)
                portalin = None
                portalout = None
                portalsLife = None
                portalFaze = 0

        if cr_time == 120:
            crystal = Crystal(random.randrange(32, width-32),random.randrange(32, height-32))
            while crystal.collide(platforms) != False:
                crystal = Crystal(random.randrange(32, width-32),random.randrange(32, height-32))
            cr_time = 0
            entities.add(crystal)
            platforms.append(crystal)



        cr_time += 1

        for p in platforms:
            if isinstance(p, block.Crystal):
                if p.collide_player(hero) == True:
                    entities.remove(p)
                    platforms.remove(p)
                    energy += 2
                elif p.life <= 0:
                    entities.remove(p)
                    platforms.remove(p)
                else:
                    p.life -= 1

        energySur = Surface((32, 20*32))
        energySur.fill(Color(BACKGROUND_COLOR))
        energyIm = Surface((32, energy*32))
        energyIm.fill(Color(energy_color))
        
        if energy > 20:
            energy = 20
        energy -= 0.008
        if energy <= 0:
            activegame = False
        
        screen.blit(bg, (0,0))
        hero.update(left,right,up,platforms)
        if portalin != None:
            portalin.update()
        if portalout != None:
            portalout.update()
        
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        screen.blit(energySur, (960,0))
        screen.blit(energyIm, (960,(20-energy)*32))
        button("Back to menu",768,672,256,47,red,bright_red,closegame)

        pygame.draw.rect(screen, black, (768,715,256,53))

        font = pygame.font.SysFont("comicsansms",20)
        Text = font.render("Portals: "+str(av_portals), True, white)      
        screen.blit(Text, (768,720))

        font = pygame.font.SysFont("comicsansms",20)
        Text = font.render("Lives: "+str(lives), True, white)      
        screen.blit(Text, (768,740))

        pygame.display.update()
        score += 0.1
        score = math.ceil(score)
    activegame = True
    while  activegame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        timer.tick(60)
        screen.blit(bg, (0,0))

        font = pygame.font.SysFont("comicsansms",60)
        Text = font.render("Score: "+str(score), True, white)      
        screen.blit(Text, (380,300))

        font = pygame.font.SysFont("comicsansms",40)
        Text = font.render("Do you want to save the result?", True, white)      
        screen.blit(Text, (225,400))

        button("Yes",360,600,100,100,green,bright_green,)
        button("No",560,600,100,100,red,bright_red,closegame)

        pygame.display.update()
    activegame = True
    intro  = False


    

def records_menu():
    pygame.display.set_caption("Records menu")
    rec = True
    while rec:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",60)
        TextSurf, TextRect = text_objects("Records", largeText)
        TextRect.center = ((width/2),100)
        screen.blit(TextSurf, TextRect)

        font = pygame.font.SysFont("comicsansms",40)
        Text = font.render("1) piu piu piu piu piu", True, black)      
        screen.blit(Text, (50,200))

        font = pygame.font.SysFont("comicsansms",40)
        Text = font.render("2) piu piu piu piu", True, black)      
        screen.blit(Text, (50,250))

        font = pygame.font.SysFont("comicsansms",40)
        Text = font.render("3) piu piu piu", True, black)      
        screen.blit(Text, (50,300))

        font = pygame.font.SysFont("comicsansms",40)
        Text = font.render("4) piu piu", True, black)      
        screen.blit(Text, (50,350))

        font = pygame.font.SysFont("comicsansms",40)
        Text = font.render("5) piu", True, black)      
        screen.blit(Text, (50,400))
        
        doc_width = 406
        doc_height = 386
        menu_doc = pygame.image.load('%s/blocks/grades.png' % DIR)
        screen.blit(menu_doc,(512,200))
        

        button("Back to menu",378,600,250,50,green,bright_green,game_intro)
        pygame.display.update()
        clock.tick(15)

def game_intro():
    global intro
    intro  = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",60)
        TextSurf, TextRect = text_objects("Amazing Doctor Strange", largeText)
        TextRect.center = ((width/2),100)
        screen.blit(TextSurf, TextRect)

        doc_width = 406
        doc_height = 380
        menu_doc = pygame.image.load('%s/blocks/menu2.png' % DIR)
        screen.blit(menu_doc,(50,388))

        button("Start game!",668,300,250,50,green,bright_green,main)
        button("Records",668,400,250,50,green,bright_green,records_menu)
        button("Quit",668,500,250,50,red,bright_red,quit)
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    while True:
        game_intro()
        intro  = True

