import abc
import math

import pygame

from game.world.actor.bullet import BulletManager


class Gun:

    def __init__(self):
        self._reload_time = 0.1
        self._time = 0
        self._collision = 0
        self._color = 'red'

    @abc.abstractmethod
    def shot(self, pos, velocity):
        pass

    def update(self, delta):
        self._time += delta

    def set_collision_type(self, ct):
        self._collision = ct

    def set_color(self, color):
        self._color = color


class DefaultGun(Gun):

    def shot(self, pos, velocity):
        if self._time >= self._reload_time:
            b = BulletManager.instance().get_bullet()
            b.shape.collision_type = self._collision
            if isinstance(self._color, str):
                c = pygame.color.THECOLORS[self._color]
            else:
                c = self._color
            b.color = c
            b.body.position = pos
            b.body.velocity = velocity
            self._time = 0


class TripleGun(Gun):
    _rotated = (math.cos(math.pi / 10), math.sin(math.pi / 10))

    def shot(self, pos, velocity):
        if self._time >= self._reload_time:
            x = velocity[0]
            y = velocity[1]
            velocity[0] = self._rotated[0] * x + self._rotated[1] * y
            velocity[1] = -self._rotated[1] * x + self._rotated[0] * y
            if isinstance(self._color, str):
                c = pygame.color.THECOLORS[self._color]
            else:
                c = self._color

            for i in range(3):
                b = BulletManager.instance().get_bullet()
                b.shape.collision_type = self._collision
                b.color = c
                b.body.position = pos
                b.body.velocity = velocity

                x = velocity[0]
                y = velocity[1]
                velocity[0] = self._rotated[0] * x - self._rotated[1] * y
                velocity[1] = self._rotated[1] * x + self._rotated[0] * y
            self._time = 0


class Explosion(Gun):
    _instance = None

    def __init__(self):
        super().__init__()
        self._collision = 6
        self._n = 18
        self._radius = 10
        self._dx = math.cos(2 * math.pi / self._n)
        self._dy = math.sin(2 * math.pi / self._n)

    def shot(self, pos, velocity):
        """
        :param pos: позиция
        :param velocity: скорость: число
        :return:
        """
        radius = self._radius
        n = self._n
        dx = self._dx
        dy = self._dy

        force = velocity[0] / radius

        xx = radius
        yy = 0
        for i in range(n):
            b = BulletManager.instance().get_bullet()
            b.shape.collision_type = self._collision
            b.color = 'red'
            b.body.position = (pos[0] + xx, pos[1] + yy)
            b.body.velocity = (xx * force, yy * force)
            x = xx
            xx = x * dx + yy * dy
            yy = -x * dy + yy * dx

    def set_n(self, n):
        self._n = n
        self._dx = math.cos(2 * math.pi / self._n)
        self._dy = math.sin(2 * math.pi / self._n)

    def set_radius(self, radius):
        self._radius = radius

    @classmethod
    def instance(cls) -> Gun:
        if cls._instance is None:
            cls._instance = Explosion()
        return cls._instance
