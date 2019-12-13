import abc
import math

import pygame

from game.core.data_manager import AudioManager, SoundName
from game.world.actor.bullet import BulletManager
from game.world.actor.data_actor import Stats


class Gun:

    def __init__(self):
        self.reload_time = 0.1
        self.time = 0
        self.collision = 0
        self.color = 'red'

    @abc.abstractmethod
    def shot(self, pos, velocity):
        pass

    def update(self, delta):
        self.time += delta

    def set_collision_type(self, ct):
        self.collision = ct

    def set_color(self, color):
        self.color = color


class DefaultGun(Gun):

    def __init__(self):
        super().__init__()
        self.reload_time = 0.8

    def shot(self, pos, velocity):
        if self.time >= self.reload_time:
            b = BulletManager.instance().get_bullet()
            b.shape.collision_type = self.collision
            if isinstance(self.color, str):
                c = pygame.color.THECOLORS[self.color]
            else:
                c = self.color
            b.set_stat(Stats.Color, c)
            b.body.position = pos
            b.body.velocity = velocity
            self.time = 0


class TripleGun(Gun):
    _rotated = (math.cos(math.pi / 10), math.sin(math.pi / 10))

    def shot(self, pos, velocity):
        if self.time >= self.reload_time:
            AudioManager.instance().play_sound(SoundName.Sound4)
            x = velocity[0]
            y = velocity[1]
            velocity[0] = self._rotated[0] * x + self._rotated[1] * y
            velocity[1] = -self._rotated[1] * x + self._rotated[0] * y
            if isinstance(self.color, str):
                c = pygame.color.THECOLORS[self.color]
            else:
                c = self.color

            bullets = BulletManager.instance().get_bullet(3)
            for b in bullets:
                b.shape.collision_type = self.collision
                b.set_stat(Stats.Color, c)
                b.body.position = pos
                b.body.velocity = velocity

                x = velocity[0]
                y = velocity[1]
                velocity[0] = self._rotated[0] * x - self._rotated[1] * y
                velocity[1] = self._rotated[1] * x + self._rotated[0] * y
            self.time = 0


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
        AudioManager.instance().play_sound(SoundName.Sound4)

        n = self._n
        dx = self._dx
        dy = self._dy

        force = velocity[0] / radius

        xx = radius
        yy = 0
        bullets = BulletManager.instance().get_bullet(n)
        for b in bullets:
            b.shape.collision_type = self._collision
            b.set_stat(Stats.Color, 'green')
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
