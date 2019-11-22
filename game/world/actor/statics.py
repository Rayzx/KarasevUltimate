import pygame
import pymunk

from game.world.actor.actors import Static
import resources.resource_manager as tm


class Wall(Static):

    def __init__(self, y):
        super().__init__()
        self.texture = tm.Texture_Name.Polygon
        self.color = pygame.color.THECOLORS['orange4']
        self.rect = pygame.Rect(500, 450.0, 50, 50)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pymunk.Vec2d(200, y)
        self.shape = pymunk.Poly(self.body, [(-100, -100), (-100, 100), (100, 100), (100, -100)])
        self.shape.elasticity = 1.1
