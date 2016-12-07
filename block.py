from pygame import *
from pygame.locals import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
DIR = os.path.dirname(__file__)

class Platform(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(Color(PLATFORM_COLOR))
		self.image = image.load("%s/blocks/platform.png" % DIR)
		self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)