import abc
import math

from game.core.Tools import Pool, Poolable
from game.world.actor.actors import Dynamic, Actor
from game.world.manager import Manager
import resources.resource_manager as rm


class Bullet(Dynamic, Poolable):

    def __init__(self, x, y, velocity, max_time=-1.0):
        super().__init__(x=x,
                         y=y,
                         t=rm.Image_Name.Circle,
                         vertices=5,
                         color='green',
                         mass=0.001)
        self.visible = False
        self.body.sensor = True
        self.shape.collision_type = Actor.collision_type['NoCollision']
        self.shape.elasticity = 1
        self.body.velocity = velocity
        self._time = 0.0
        self._max_time = max_time

    def update(self, delta: float):
        if self.visible:
            self._time += delta
            if self._max_time != -1 and self._time >= self._max_time:
                BulletManager.instance().return_bullet(self)
            elif self.life <= 0 or self.body.velocity.get_length_sqrd() < 10000:
                BulletManager.instance().return_bullet(self)

    def collision(self, actor=None):
        self.life = self.life - 1

    def reset(self):
        self.visible = False
        self.body.velocity = (0, 0)
        self.body.sensor = True
        self.shape.collision_type = Actor.collision_type['NoCollision']


class BulletManager:
    _instance = None

    def __init__(self):
        def new_bullet():
            b = Bullet(0, 0, (0, 0))
            Manager.instance().add_actor(b)
            return b

        self.bullet_pool = Pool(new_object=new_bullet)

    def get_bullet(self) -> Bullet:
        b = self.bullet_pool.obtain()
        b.visible = True
        b.body.sensor = False
        b.life = 1
        b.shape.collision_type = Actor.collision_type['Bullet']
        return b

    def return_bullet(self, bullet):
        self.bullet_pool.free(bullet)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BulletManager()
        return cls._instance


class Gun:
    @abc.abstractmethod
    def shot(self, pos, velocity, data=None):
        pass


class DefaultGun(Gun):
    def shot(self, pos, velocity, data=None):
        b = BulletManager.instance().get_bullet()
        b.body.position = pos
        b.body.velocity = velocity


class Explosion(Gun):
    _instance = None

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
