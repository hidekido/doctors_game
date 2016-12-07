from pygame import *
from pygame.locals import *
import pyganim
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
tp_width = 64
tp_height = 96
tp_color = "#444444"
PLATFORM_COLOR = "#FF6262"
DIR = os.path.dirname(__file__)

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % DIR),
            ('%s/blocks/portal1.png' % DIR)]

class Platform(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(Color(PLATFORM_COLOR))
		self.image = image.load("%s/blocks/platform.png" % DIR)
		self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockTeleport(sprite.Sprite):
	def __init__(self, x, y, goX = 55, goY = 55, act = 0):
		sprite.Sprite.__init__(self)
		self.image = Surface((tp_width, tp_height))
		self.image.fill(Color("#444444"))
		self.truex = x - x%32
		self.truey = y - y%32
		self.rect = Rect(self.truex, self.truey, tp_width, tp_height)
		self.goX = goX # координаты назначения перемещения
		self.goY = goY # координаты назначения перемещения
		boltAnim = []
		for anim in ANIMATION_BLOCKTELEPORT:
			boltAnim.append((anim, 0.3))
		self.boltAnim = pyganim.PygAnimation(boltAnim)
		self.boltAnim.play()
		
	def update(self):
		self.image.fill(Color("#444444"))
		self.boltAnim.blit(self.image, (0, 0))