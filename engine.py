import pygame
from pygame.locals import *


class Engine():
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game.run = False
            elif event.type == KEYDOWN:
                self.key_down(event.key)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.game.run = False
                self.key_up(event.key)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_up(event.button, event.pos)
            elif event.type == MOUSEMOTION:
                self.mouse_motion(event.buttons, event.pos, event.rel)

    def key_up(self, key):
        if key == K_BACKQUOTE:
            self.terminal.init()

            if not self.terminal.run_cmd() == -1:
                redo = pygame.event.Event(KEYUP, {'key': K_BACKQUOTE})
                pygame.event.post(redo)

    def key_down(self, key):
        pass

    def mouse_up(self, button, pos):
        self.dirty_rect = (self.character.rect[0] * 100, self.character.rect[1] * 100) + self.character.size
        self.update(self.background.surface, (self.character.rect[0] * 100, self.character.rect[1] * 100), (self.character.rect[0] * 100, self.character.rect[1] * 100, 100, 100))
        position_rel = (abs(pos[0] / self.character.size[0]), abs(pos[1] / self.character.size[1]))
        position_abs = (position_rel[0] * self.character.size[0], position_rel[1] * self.character.size[1])
        self.character.draw(position_rel)
        self.dirty_rect = position_abs + self.character.size
        self.update(self.character.surface, position_abs, (0, 0, 100, 100))

    def mouse_motion(self, buttons, pos, rel):
        pass

    def update(self, surface=None, dest=(0, 0), area=None):
        self.draw(surface, dest, area)

        if self.startup:
            pygame.display.update()
            self.startup = False
        elif not self.dirty_rect == None:
            pygame.display.update(self.dirty_rect)
            self.dirty_rect = None

    def draw(self, surface, dest, area):
        if self.startup:
            self.screen.fill(self.fill)
            self.background.draw()
            self.screen.blit(self.background.surface, (0, 0))
        elif not surface == None:
            self.screen.blit(surface, dest, area)
