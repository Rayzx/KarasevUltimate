import pygame
import pymunk

from game.world.actor.actors import Dynamic
import resources.resource_manager as rm


class Player(Dynamic):
    """
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = rm.Image_Name.Polygon
        self.color = pygame.color.THECOLORS['red']
        self.rect = pygame.Rect(500, 450.0, 50, 50)
        self.body = pymunk.Body(10, pymunk.moment_for_circle(10, 0, 10), body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(200, 200)
        # self.shape = pymunk.Circle(self.body, 10)
        self.shape = pymunk.Poly(self.body, [(-10, -10), (-10, 10), (10, 10), (10, -10), (5, -20)])
        self.shape.elasticity = 1
        self.shape.friction = 0.5
        self.body.velocity_func = speed_limit
        self.body.angular_velocity =0

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

    def update(self, delta: float):
        # self.body.angular_velocity = 0.5
        pass


class Ball(Dynamic):
    """

    """

    def __init__(self):
        super().__init__()
        pass


def speed_limit(body, gravity, damping, dt):
    max_velocity = 2000
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity:
        scale = max_velocity / l
        body.velocity = body.velocity * scale
