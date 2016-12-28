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

CRYSTAL_WIDTH = 25
CRYSTAL_HEIGHT = 25
CRYSTAL_COLOR = "#FF6262"


ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % DIR),
            ('%s/blocks/portal1.png' % DIR)]

class Platform(sprite.Sprite):
	def __init__(self, x, y, r):
		sprite.Sprite.__init__(self)
		self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(Color(PLATFORM_COLOR))
		dirs = ["%s/blocks/platform1.png","%s/blocks/platform2.png","%s/blocks/platform3.png"]
		self.image = image.load(dirs[r] % DIR)
		self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockTeleport(sprite.Sprite):
	def __init__(self, x, y, goX = None, goY = None, act = 0, alter = None):
		sprite.Sprite.__init__(self)
		self.alter = alter
		self.act = act
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

	def collide(self, platforms):
		for p in platforms:
			if sprite.collide_rect(self, p):
				return True
		return False
class Crystal(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = Surface((CRYSTAL_WIDTH, CRYSTAL_HEIGHT))
		self.life = 150
		self.image.fill(Color(CRYSTAL_COLOR))
		self.image = image.load("%s/blocks/crystal.png" % DIR)
		self.rect = Rect(x, y, CRYSTAL_WIDTH, CRYSTAL_HEIGHT)
	def collide(self, platforms):
		for p in platforms:
			if sprite.collide_rect(self, p):
				return True
		return False

	def collide_player(self, player):
		if sprite.collide_rect(self, player):
			return True
		return False
