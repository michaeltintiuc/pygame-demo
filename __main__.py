import sys
import pygame
from pygame.locals import *
from gfx import *
from character import *


class Game(object):
	def __init__(self, fps=60):
		## Set the variables
		self.size = (800, 640)
		self.screen = pygame.display.set_mode(self.size, 0, 32)
		self.rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()
		self.padding = (12 * 32, self.size[0] - 11 * 32)
		self.speed = 4
		self.run = True

		## Initiate classes and Sprite Groups
		self.map = Map('images/map.tmx', self.rect)
		self.character = Character((160, 64))
		self.sprite_group_all = pygame.sprite.LayeredDirty()
		self.sprite_group_map = pygame.sprite.LayeredDirty()

		## Perform startup tasks
		self.map.render(self.screen)
		self.sprite_group_all.add(self.map.tiles, self.character)
		self.sprite_group_map.add(self.map.tiles)
		self.sprite_group_all.clear(self.screen, self.map)

		## Update and start loop
		pygame.display.flip()
		self.loop(fps)

	## Main Loop
	def loop(self, fps):
		while self.run:
			self.handle_events()

			## Death
			if self.character.rect.bottom >= 640:
				self.character.rect.left = 160
				self.character.rect.bottom = 64
				self.sprite_group_map.update(self.map.rect.left)
				self.map.rect.left = 0

			rects = self.sprite_group_all.draw(self.screen)

			if rects:
				pygame.display.update(rects)

			self.clock.tick(fps)
			pygame.display.set_caption("FPS: %i" % self.clock.get_fps())

	## Event Handler
	def handle_events(self):
		keystate = pygame.key.get_pressed()
		self.key_hold(keystate)

		for event in pygame.event.get():
			if event.type == QUIT:
				self.run = False

			elif event.type == KEYDOWN:
				self.key_down(event.key)

			elif event.type == KEYUP:
				self.key_up(event.key)

			elif event.type == MOUSEMOTION:
				self.mouse_motion(event.buttons, event.pos, event.rel)

	## Key Up Event
	def key_up(self, key):
		if key == K_ESCAPE:
			self.run = False

		if key == K_SPACE:
			self.character.can_jump = True

	## Key Up Event
	def key_down(self, key):
		pass

	## Key Press Event
	def key_hold(self, key):
		displace = 0

		## Right
		if key[K_d]:
			if not self.character.d_right:
				self.character.d_right = True

			if self.character.rect.left > self.padding[0]:
				if self.map.rect.left < self.size[0]:
					self.character.x = 0
					displace = self.speed

					if not self.character.collide_x:
						self.map.rect.move_ip(self.speed, 0)
						self.sprite_group_map.update(-self.speed)

				elif self.character.rect.right < self.size[0]:
					self.character.x = self.speed

			elif self.character.rect.right < self.size[0]:
				self.character.x = self.speed
		## Left
		elif key[K_a]:
			if self.character.d_right:
				self.character.d_right = False

			if self.character.rect.right < self.padding[0]:
				if self.map.rect.left > 0:
					self.character.x = 0
					displace = -self.speed

					if not self.character.collide_x:
						self.map.rect.move_ip(-self.speed, 0)
						self.sprite_group_map.update(self.speed)

				elif self.character.rect.left > 0:
					self.character.x = -self.speed

			elif self.character.rect.left > 0:
				self.character.x = -self.speed
		else:
			self.character.moving = False

		## Jump
		if key[K_SPACE]:
			if self.character.on_ground and self.character.y == 0 and self.character.can_jump:
				self.character.y = -24
				self.character.can_jump = False
			elif self.character.can_jump and not self.character.jump_count:
				self.character.y += -16
				self.character.jump_count = 1
				self.character.can_jump = False

		## Update
		self.character.update(self.sprite_group_map, displace)

	## Mouse Move Event
	def mouse_motion(self, buttons, pos, rel):
		pass

if __name__ == '__main__':
	pygame.init()

	Game(60)

	pygame.quit()
	sys.exit()
