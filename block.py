from pygame import *
from pygame.locals import *

PLATFORM_WIDTH = 25
PLATFORM_HEIGHT = 25
PLATFORM_COLOR = "#FF6262"

class Platform(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(Color(PLATFORM_COLOR))
		self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)