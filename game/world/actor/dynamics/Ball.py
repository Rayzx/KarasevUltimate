import math
import random as rnd

import pygame

from game.world.actor.actors import Dynamic
from resources.resource_manager import Resource_Type


class Ball(Dynamic):

    def __init__(self):
        self.sprite = pygame.sprite.Sprite()
        self._type = Resource_Type.Circle
        self._rect = pygame.Rect((rnd.randint(100, 800), 450.0, 200, 200))
        self.time = 0.0

    def update(self, delta: float):
        self.time += delta
        self._rect.x += 4 * math.sin(self.time)
        self._rect.y += 2 * math.cos(self.time)

    def get_type(self):
        return self._type

    def get_rect(self):
        return self._rect


if __name__ == '__main__':
    Ball()
