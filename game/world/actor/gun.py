import abc
import math

import pygame

from game.world.actor.bullet import BulletManager


class Gun:
    @abc.abstractmethod
    def shot(self, pos, velocity, data=None):
        pass

    def update(self, delta):
        pass

    def set_collision_type(self, ct):
        pass

    def set_color(self, color):
        pass


class DefaultGun(Gun):

    def __init__(self):
        self._reload_time = 0.1
        self._time = 0
        self._collision = 0
        self._color = 'red'

    def shot(self, pos, velocity, data=None):
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

    def update(self, delta):
        self._time += delta

    def set_collision_type(self, ct):
        self._collision = ct

    def set_color(self, color):
        self._color = color


class Explosion(Gun):
    _instance = None

    def __init__(self):
        self._collision = 6

    def shot(self, pos, velocity, data=None):
        """
        :param pos: позиция
        :param velocity: скорость: число
        :param data: словарь с полями 'n' - колличество пуль и 'radius' радиус тела
        :return:
        """
        if isinstance(data, dict):
            radius = data['radius']
            n = data['n']
            dx = math.cos(2 * math.pi / n)
            dy = math.sin(2 * math.pi / n)

            force = velocity / radius

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

    @classmethod
    def instance(cls) -> Gun:
        if cls._instance is None:
            cls._instance = Explosion()
        return cls._instance
