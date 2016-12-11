import pygame
from pytmx import tmxloader


class Map(pygame.Surface):
	def __init__(self, file, rect):
		self.tiledmap = tmxloader.load_pygame(file)
		self.size = self.tiledmap.width * self.tiledmap.tilewidth, self.tiledmap.height * self.tiledmap.tileheight
		pygame.Surface.__init__(self, self.size)
		self.rect = rect.copy()
		self.tiles = []

	def render(self, surface):
		## Usability Variables
		layers = xrange(0, len(self.tiledmap.tilelayers))
		tile_w = self.tiledmap.tilewidth
		tile_h = self.tiledmap.tileheight
		get_tile_image = self.tiledmap.getTileImage

		## Draw Background
		for layer in layers:
			for x in xrange(0, self.tiledmap.width):
				for y in xrange(0, self.tiledmap.height):
					tile = get_tile_image(x, y, layer)

					if tile:
						if self.tiledmap.tilelayers[layer].name == 'bg':
							self.blit(tile, (x * tile_w, y * tile_h))
						# else:
						# 	self.tiles.append(Tile(tile, (x * tile_w, y * tile_h), (tile_w, tile_h)))

		## Blit Background to Screen
		surface.blit(self, self.rect)

		## Create Sprites from Objects
		for obj_group in self.tiledmap.objectgroups:
			for obj in obj_group:
				for layer in layers:
					if not self.tiledmap.tilelayers[layer].name == 'bg':
						x = obj.x / tile_w
						y = obj.y / tile_h

						tile = get_tile_image(x, y, layer)
						if tile:
							self.tiles.append(Tile(tile, (obj.x, obj.y), (obj.width, obj.height)))

	# def move(self, pos, surface, rect):
	# 	self.rect.move_ip(pos, 0)
	# 	# scale(self.subsurface(self.rect), rect.size, surface.subsurface(rect))

	# 	# return surface.convert()


class Tile(pygame.sprite.DirtySprite):
	def __init__(self, file, pos, size):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface(size).convert()
		self.rect = pygame.Rect(pos, size)
		self.draw(size, file)

	def update(self, pos):
		self.rect.move_ip(pos, 0)
		self.dirty = 1

	def draw(self, size, file):
		for x in xrange(0, size[0], 32):
			for y in xrange(0, size[1], 32):
				self.image.blit(file, (x, y))
