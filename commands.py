class Commands:
	def __init__(self, terminal=None):
		self.terminal = terminal
		self.engine = self.terminal.engine
		self.map = self.engine.map
		self.character = self.engine.character
		self.list = ('quit', 'help', 'done', 'clear', 'start', 'redraw_bg')

	def quit(self):
		self.terminal.run = False
		self.engine.run = False
		print 'Good-bye...\n'

		return -1

	def help(self):
		for command in self.list:
			print '\t', command

	def done(self):
		self.terminal.run = False
		print 'Terminal stopped\n'

		return -1

	def clear(self):
		print '\n' * 100

	def start(self):
		params = len(self.terminal.input)

		if params < 2:
			print 'Missing parameters - left, top. Example: "start 0 0"\n'
		elif params < 3:
			print 'Missing parameter - top. Example: "start 0 0"\n'
		else:
			try:
				left = abs(int(self.terminal.input[1]))
				top = abs(int(self.terminal.input[2]))
			except ValueError:
				print 'Parameters must be INT\n'
			else:
				if left > self.map.tiles[0]:
					print 'Parameter exceeds horizontal tile count. Maximum allowed is', self.map.tiles[0]
				elif top > self.map.tiles[1]:
					print 'Parameter exceeds vertical tile count. Maximum allowed is', self.map.tiles[1]
				elif (left, top) in self.map.walls_xy:
					print 'Tile unavailable'
				else:
					self.engine.dirty_rect = (self.character.rect[0] * 100, self.character.rect[1] * 100) + self.character.size
					self.engine.update(self.map.surface, (self.character.rect[0] * 100, self.character.rect[1] * 100), (self.character.rect[0] * 100, self.character.rect[1] * 100, 100, 100))
					self.character.draw((left, top))
					position = (left * self.character.size[0], top * self.character.size[1])
					self.engine.dirty_rect = position + self.character.size
					self.engine.update(self.character.surface, position, (0, 0, 100, 100))

	def redraw_bg(self):
		if len(self.terminal.input) < 2:
			print 'Missing parameter - count. Example: "redraw_bg 10"\n'
		else:
			try:
				wall_count = int(self.terminal.input[1])
			except ValueError:
				print 'Parameter must be an INT\n'
			else:
				self.map.draw(wall_count)
				self.engine.dirty_rect = (0, 0) + self.engine.size
				self.engine.update(self.map.surface, (0, 0))
