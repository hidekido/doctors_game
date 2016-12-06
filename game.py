import pygame
from pygame import *
from block import *

WINHEIGHT = 768
WINWIDTH = 1024
DISPLAY = (WINWIDTH, WINHEIGHT)
BACKGROUND_COLOR = "#444444"
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Amazing Doctor Strange")
bg = Surface((WINWIDTH,WINHEIGHT))

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


def main():
	bg.fill(Color(BACKGROUND_COLOR))
	mainLoop = True
	while mainLoop:
		for event in pygame.event.get():
			if event.type == QUIT:
				mainLoop = False
		screen.blit(bg, (0,0)) 
		pygame.display.update()
	pygame.quit() 

if __name__ == '__main__':
	main()

