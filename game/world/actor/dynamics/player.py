import pygame
import pymunk
from pymunk import Vec2d

from game.world.actor.actors import Dynamic
import resources.resource_manager as tm


class Player(Dynamic):
    """
    """
    def __init__(self):
        super().__init__()

        self.texture = tm.Texture_Name.Circle
        self.color = pygame.color.THECOLORS['orange4']
        self.rect = pygame.Rect(500, 450.0, 50, 50)
        self.body = pymunk.Body(100, 100)
        self.body.position = Vec2d(200, 200)
        self.shape = pymunk.Circle(self.body, 10, self.body.position)
        self._time = 0.0

    def set_direction(self, angle: float):
        """

        :param angle:
        :return:
        """
        pass

    def move(self):
        """

        :return:
        """
        pass
