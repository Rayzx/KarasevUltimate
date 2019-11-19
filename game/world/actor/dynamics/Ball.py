import math
import random as rnd

import pygame

from game.world.actor.actors import Dynamic
import resources.resource_manager as tm


class Ball(Dynamic):

    def __init__(self):
        self._type = tm.Texture_Name.Circle
        self._rect = pygame.Rect((rnd.randint(000, 1000), 450.0, 50, 50))
        self._time = 0.0

    def update(self, delta: float):
        self._time += delta
        self._rect.x += 4 * math.sin(self._time)
        self._rect.y += 2 * math.cos(self._time)

    def get_type(self):
        return self._type

    def get_rect(self):
        return self._rect

    def get_color(self):
        return tm.Colors.red
