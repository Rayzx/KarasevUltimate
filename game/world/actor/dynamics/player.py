import pygame
import pymunk

from game.world.actor.actors import Dynamic
import resources.resource_manager as tm


class Player(Dynamic):

    def __init__(self):
        super().__init__()
        self.texture = tm.Texture_Name.Circle
        self.color = pygame.color.THECOLORS['orange4']
        self.rect = pygame.Rect(500, 450.0, 50, 50)
        body = pymunk.Body(100, 100)
        self._body = pymunk.Circle(body, 10, (0, 0))
        self._time = 0.0

    def set_direction(self, angle: float):
        pass

    def move(self):
        pass
