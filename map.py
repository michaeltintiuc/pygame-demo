import os
import random
import pygame
from pygame.locals import *


class Background:
    def __init__(self, count=0):
        self.size = (800, 600)
        self.tiles = (8, 6)
        self.tile_size = 100
        self.count = count
        self.wall_trigger = self.gen_walls(self.count)
        self.walls = []
        self.img = pygame.image.load(os.path.join('images/bg.jpg')).convert()
        self.surface = pygame.Surface(self.size).convert()

    def draw(self):
        i = 0
        for x in range(self.tiles[0]):
            for y in range(self.tiles[1]):
                if self.wall_trigger[i]:
                    self.walls.append((x, y))
                    self.surface.blit(self.img, (self.tile_size * x + 1, self.tile_size * y + 1), (self.tile_size, 0, self.tile_size, self.tile_size))
                else:
                    self.surface.blit(self.img, (self.tile_size * x + 1, self.tile_size * y + 1), (0, 0, self.tile_size, self.tile_size))

                i += 1

    def redraw(self, count):
        self.wall_trigger = self.gen_walls(count)
        self.draw()

    def gen_walls(self, count=0):
        count_no = (self.tiles[0] * self.tiles[1]) - count
        walls_no = [0 for i in range(count_no)]
        walls_yes = [1 for i in range(count)]

        walls = walls_no + walls_yes
        random.shuffle(walls)

        return walls
