import math
import random as rnd

import pygame

from game.world.actor.actors import Dynamic
import resources.resource_manager as tm


class Ball(Dynamic):

    def __init__(self):
        super().__init__()
        self.texture = tm.Texture_Name.Circle
        self.color = pygame.color.THECOLORS['orange4']
        self.rect = pygame.Rect((rnd.randint(0, 1000), 450.0, 50, 50))
        self._time = 0.0

    def update(self, delta: float):
        self._time += delta
        self._rect.x += 4 * math.sin(self._time)
        self._rect.y += 2 * math.cos(self._time)
