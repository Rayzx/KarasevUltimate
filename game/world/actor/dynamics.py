import math

import pymunk
from game.world.actor.actors import Dynamic, Actor
import resources.resource_manager as rm
from game.world.actor.gun import DefaultGun, Explosion
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
        self.shape.collision_type = Actor.collision_type['Player']

        self.body.velocity_func = Dynamic.speed_update_body
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0

        self.gun = DefaultGun()

    def set_direction(self, angle: float):
        """

        :param angle:
        :return:
        """
        self.body.angle = angle

    def shot(self):
        dx = math.cos(self.body.angle)
        dy = math.sin(self.body.angle)
        self.gun.shot((self.pos[0] + 20 * dx, self.pos[1] + 20 * dy),
                      (dx * 100, dy * 100), {'color': 'green'})

    def move(self):
        pass

    def update(self, delta: float):
        # self.body.angular_velocity = 0.5
        pass


class Ghost(Dynamic):
    pass


class Barrel(Dynamic):
    """
        бочка при попабании снаряда взрывается
    """

    def __init__(self, x, y, t, vertices, color, blife = 1):
        super().__init__(x=x,
                         y=y,
                         t=t,
                         vertices=center(vertices),
                         color=color)
        self.shape.collision_type = Actor.collision_type['Environment']
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.blife = blife
        self.body.velocity_func = Dynamic.speed_update_body
        self.gun = Explosion.instance()

    def update(self, delta: float):
        if self.life <= 0:
            self.gun.shot(self.pos, 100, {'n': 28, 'radius': self.shape.radius, 'blife':self.blife})
            Manager.instance().remove_actor(self)

    def collision(self, actor=None):
        self.life = self.life - 1


class Box(Dynamic):
    """
     при попадании снаряда(ов) ломается
    """

    def __init__(self, x, y, t, vertices, color, life=1):
        super().__init__(x=x,
                         y=y,
                         t=t,
                         vertices=center(vertices),
                         color=color)
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.shape.collision_type = Actor.collision_type['Environment']

        self.body.velocity_func = speed_update_body

        self.life = life

    def update(self, delta: float):
        if self.life <= 0:
            Manager.instance().remove_actor(self)

    def collision(self, actor=None):
        self.life = self.life - 1

def center(vertices):
    if isinstance(vertices, int):
        return vertices
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
