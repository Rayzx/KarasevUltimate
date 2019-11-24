import pygame
import pymunk

from game.world.actor.actors import Dynamic
import resources.resource_manager as rm
from game.world.manager import Manager


class Player(Dynamic):
    """
    """

    def __init__(self, x=0, y=0):
        super().__init__(x=x,
                         y=y,
                         t=rm.Image_Name.Polygon,
                         vertices=center([[-10, -10], [-10, 10], [10, 10], [10, -10], [5, -20]]),
                         color='red')
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.body.velocity_func = speed_update_body
        self.body.velocity = (100, 0)
        self.body.angular_velocity = 0

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


class Ghost(Dynamic):
    pass


class Bullet(Dynamic):

    def __init__(self, x, y, velocity, max_time=-1):
        super().__init__(x=x,
                         y=y,
                         t=rm.Image_Name.Circle,
                         vertices=5,
                         color=pygame.color.THECOLORS['blue'])
        self.shape.sensor = True
        self.body.velocity = velocity
        self._time = 0.0
        self._max_time = max_time

    def update(self, delta: float):
        if self._max_time != -1:
            self._time += delta
            if self._time >= self._max_time:
                Manager.remove_actor(self)


class Barrel(Dynamic):
    """
        бочка при попабании снаряда взрывается
    """

    def __init__(self, x, y, t, vertices, color):
        super().__init__(x=x,
                         y=y,
                         t=t,
                         vertices=center(vertices),
                         color=color)
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.life = 1

    def update(self, delta: float):
        if self.life == 0:
            Manager.explosion(self.pos, 10)
            Manager.remove_actor(self)


class Box(Dynamic):
    """
     при попадании снаряда(ов) ломается
    """

    def __init__(self, x, y, t, vertices, color, strength=2):
        super().__init__(x=x,
                         y=y,
                         t=t,
                         vertices=center(vertices),
                         color=color)
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.body.velocity_func = speed_update_body
        self.life = strength

    def update(self, delta: float):
        if self.life == 0:
            Manager.remove_actor(self)


max_velocity = 2000
min_velocity = 1
coefficient_of_friction = 3


def speed_update_body(body, gravity, damping, dt):
    if isinstance(body, pymunk.Body) and isinstance(body.velocity, pymunk.Vec2d):
        ll = body.velocity.length
        if ll == 0:
            return
        v = -body.velocity / ll
        v *= body.mass * body.shapes.pop().friction * coefficient_of_friction
        v += gravity
        pymunk.Body.update_velocity(body, v, damping, dt)

        if ll > max_velocity:
            scale = max_velocity / ll
            body.velocity = body.velocity * scale
        if ll < 1:
            body.velocity = body.velocity * 0


def center(vertices):
    x, y = 0.0, 0.0
    for v in vertices:
        x += v[0]
        y += v[1]
    x /= len(vertices)
    y /= len(vertices)
    for v in vertices:
        v[0] -= x
        v[1] -= y
    return vertices
