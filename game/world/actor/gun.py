import abc
import math

import pygame
from game.world.actor.data_actor import *
from game.core.data_manager import AudioManager, SoundName
from game.world.actor.bullet import BulletManager


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

    def __init__(self, bulType=0):
        super().__init__()
        self.reload_time = 0.5
        self.bulType = bulType

    def shot(self, pos, velocity):
        if self.time >= self.reload_time:
            b = None
            if self.bulType == 0:
                b = BulletManager.instance().get_bullet()
            if self.bulType == 1:
                b = BulletManager.instance().get_expBullet()
            AudioManager.instance().play_sound(SoundName.Sound6)

            b.shape.collision_type = self.collision
            if isinstance(self.color, str):
                c = pygame.color.THECOLORS[self.color]
            else:
                c = self.color
            b.color = c
            b.body.position = pos
            b.body.velocity = velocity
            self.time = 0
            return True


class TripleGun(Gun):
    _rotated = (math.cos(math.pi / 10), math.sin(math.pi / 10))

    def __init__(self, bulType=0):
        super().__init__()
        self.reload_time = 0.5
        self.bulType = bulType

    def shot(self, pos, velocity):
        if self.time >= self.reload_time:
            AudioManager.instance().play_sound(SoundName.Sound5)
            x = velocity[0]
            y = velocity[1]
            velocity[0] = self._rotated[0] * x + self._rotated[1] * y
            velocity[1] = -self._rotated[1] * x + self._rotated[0] * y
            if isinstance(self.color, str):
                c = pygame.color.THECOLORS[self.color]
            else:
                c = self.color
            bullets = None
            if self.bulType == 0:
                bullets = BulletManager.instance().get_bullet(3)
            if self.bulType == 1:
                bullets = BulletManager.instance().get_expBullet(3)
            for b in bullets:
                b.shape.collision_type = self.collision
                b.color = c
                b.body.position = pos
                b.body.velocity = velocity

                x = velocity[0]
                y = velocity[1]
                velocity[0] = self._rotated[0] * x - self._rotated[1] * y
                velocity[1] = self._rotated[1] * x + self._rotated[0] * y
            self.time = 0
            return True


class Explosion(Gun):
    _instance = None

    def __init__(self, n=18, ct=collision_type[CollisionType.Bullet]):
        """
        :n: count of beams
        :collision_type: CollisionType.Bullet - damage all
                         CollisionType.PlayerBullet - no damage player
                          CollisionType.EnemyBullet - no damage enemy
        """
        super().__init__()

        self._collision = ct
        self._n = n
        self._radius = 10
        self._dx = math.cos(2 * math.pi / self._n)
        self._dy = math.sin(2 * math.pi / self._n)
        self.reload_time = -1

    def shot(self, pos, velocity):
        """
        :param pos: позиция
        :param velocity: скорость: число module
        """
        if self.time > self.reload_time:
            AudioManager.instance().play_sound(SoundName.Sound4)

            n = self._n
            dx = self._dx
            dy = self._dy

            xx = velocity[0]
            yy = velocity[1]
            bullets = BulletManager.instance().get_bullet(n)
            for b in bullets:
                b.shape.collision_type = self._collision
                b.color = self.color
                b.body.position = (pos[0], pos[1])
                b.body.velocity = (xx, yy)
                x = xx
                xx = x * dx + yy * dy
                yy = -x * dy + yy * dx
            return True

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
