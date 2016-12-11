import pygame


class Character(pygame.sprite.DirtySprite):
	img = pygame.image.load('images/charsheet.png')

	def __init__(self, pos):
		## Set Main Sprite vars
		pygame.sprite.DirtySprite.__init__(self)
		self.images = self.parse_sheet(Character.img)
		self.image = self.images[0]
		self.rect = self.image.get_rect(bottomleft=pos)

		## Physics
		self.x = 0
		self.y = 0
		self.gravity = 4

		## Movement
		self.moving = True
		self.collide_x = False
		self.on_ground = False
		self.d_right = True
		self.can_jump = True
		self.jump_count = 0

		## Time
		self.frame = 0
		self.ms = 0
		self.frame_duration = 72
		self.time_end = 0

	def update(self, group, displace=0):
		## Reset
		time_diff = pygame.time.get_ticks() - self.time_end
		self.collide_x = False

		## Save Previous X, Y Positions
		prev_pos_x = self.rect.left - displace
		prev_pos_y = self.rect.bottom

		## Move Character X
		self.rect.left += self.x

		## Check for X Collisions
		if pygame.sprite.spritecollideany(self, group):
			self.collide_x = True
			self.moving = False
			self.rect.left = prev_pos_x

		## Move Character Y
		if self.rect.bottom < 697:
			self.rect.bottom += self.gravity + self.y

			if self.y >= 0:
				self.y = 0
			else:
				self.y += 2

		## Check for Y Collisions
		block = pygame.sprite.spritecollideany(self, group)
		if block:
			if self.rect.top >= block.rect.top:
				self.on_ground = False
			else:
				self.on_ground = True
				self.jump_count = 0

			self.rect.bottom = prev_pos_y
		else:
			self.on_ground = False
			self.moving = True

		## Delay Animation
		for i in xrange(time_diff):
			self.ms += 1
			if self.ms == self.frame_duration:
				self.ms = 0

				if self.on_ground and self.moving:
					self.run()
				elif self.moving:
					self.jump()
				else:
					self.stop()

		self.dirty = 1
		self.moving = True
		self.x = 0
		self.time_end = pygame.time.get_ticks()

	def jump(self):
		if self.d_right:
			self.image = self.images[15]
		else:
			self.image = self.images[14]

	def run(self):
		self.frame += 1

		if self.d_right:
			if self.frame > 6:
				self.frame = 1
		else:
			if self.frame > 13:
				self.frame = 8
			elif self.frame < 7:
				self.frame = 7

		self.image = self.images[self.frame]

	def stop(self):
		if self.d_right:
			self.image = self.images[0]
		else:
			self.image = self.images[7]

		self.moving = False

	def parse_sheet(self, file):
		images = []

		for y in range(0, 3):
			for x in range(0, 7):
				if y > 1 and x > 1:
					continue
				else:
					image = file.subsurface(((32 * x, 57 * y), (32, 57))).convert()
					image.set_colorkey((0, 255, 0))
					image.convert_alpha()
					images.append(image)

		return images
