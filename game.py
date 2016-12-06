import pygame
from pygame import *
from block import *

WINHEIGHT = 768
WINWIDTH = 1024
DISPLAY = (WINWIDTH, WINHEIGHT)
BACKGROUND_COLOR = "#444444"
def main():
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY)
	pygame.display.set_caption("Amazing Doctor Strange")
	bg = Surface((WINWIDTH,WINHEIGHT))
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

