import pygame
from pygame import *
from block import *
from player import *
import os

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


entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться

DIR = os.path.dirname(__file__)
total_level_width = 1
total_level_height = 1

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)



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
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)



def lvlinit():
    f = open("%s\\levels\\1.txt" % DIR, 'r')
    level = []
    line = f.readline()
    while line != '':
        line = line[1:-2]
        level += [line]
        line = f.readline()
    level[-1] += '-'
    x = y = 0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
    

def main():
    pygame.display.set_caption("Amazing Doctor Strange")
    bg.fill(Color(BACKGROUND_COLOR))
    hero = Player(55,55) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = False
    entities.add(hero)
    lvlinit()
    camera = Camera(camera_configure, total_level_width, total_level_height)
    timer = pygame.time.Clock()
    portalin = None
    mainLoop = True
    while mainLoop:
        timer.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
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

        if click[0] == 1:
            if portalin != None:
                entities.remove(portalin)
            portalin = BlockTeleport(mouse[0],mouse[1])
            entities.add(portalin)

        screen.blit(bg, (0,0))
        if portalin != None:
            portalin.update()
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        hero.update(left,right,up,platforms)
        pygame.display.update()
    pygame.quit() 

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",60)
        TextSurf, TextRect = text_objects("Amazing Doctor Strange", largeText)
        TextRect.center = ((width/2),100)
        screen.blit(TextSurf, TextRect)

        button("Start game!",412,300,200,50,green,bright_green,main)
        button("Records",412,400,200,50,green,bright_green,)
        button("Quit",412,500,200,50,red,bright_red,quit)
        

        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
	game_intro()

