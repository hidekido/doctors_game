import pygame
from pygame import *
from block import *
from player import *
import os

WINHEIGHT = 768
WINWIDTH = 1024
DISPLAY = (WINWIDTH, WINHEIGHT)
BACKGROUND_COLOR = "#444444"
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Amazing Doctor Strange")
bg = Surface((WINWIDTH,WINHEIGHT))
bg.fill(Color(BACKGROUND_COLOR))
entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться
DIR = os.path.dirname(__file__)
black = (0,0,0)

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
    hero = Player(55,55) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = False
    lvlinit()
    timer = pygame.time.Clock()
    mainLoop = True
    while mainLoop:
        for event in pygame.event.get():
            if event.type == QUIT:
                mainLoop = False
        screen.blit(bg, (0,0))
        for e in entities:
            screen.blit(e.image, (e.x,e.y))
        pygame.display.update()
    pygame.quit() 

if __name__ == '__main__':
	main()

