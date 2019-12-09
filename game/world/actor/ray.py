import math

import pymunk

from game.core.Tools import Poolable, Pool
from game.world.actor.actors import Actor, MyBody
from game.world.game_manager import GameManager

"""
пример испольховния Ray в классе Box (лень было писать противников)

"""

class Ray(Poolable, Actor):

    def __init__(self):
        super().__init__()
        self.body = MyBody(1, pymunk.moment_for_circle(1, 1, 0, (0, 0)),
                           body_type=pymunk.Body.DYNAMIC)
        self.body.data = self
        self.shape = pymunk.Circle(self._body, 1)

        self.shape.collision_type = Actor.collision_type['Bullet']
        self.shape.sensor = True

        self.visible = False

        self.end = None
        self.callback = None
        self._coll_actor = None

    def update(self, delta: float):
        if self.life == 0:
            self.callback(self._coll_actor)
            RayManager.instance().return_ray(self)

    def reset(self):
        self.end = None
        self.callback = None
        GameManager.instance().remove_actor(self)

    def collision(self, actor=None):
        if not isinstance(actor, Ray):
            self.life = 0
            self._coll_actor = actor


class RayManager:
    _instance = None

    def __init__(self):
        def new_ray():
            b = Ray()
            return b

        self.ray_pool = Pool(new_object=new_ray)

    def _get_ray(self) -> Ray:
        b = self.ray_pool.obtain()
        GameManager.instance().add_actor(b)
        return b

    def return_ray(self, ray):
        self.ray_pool.free(ray)

    def ray_cast(self, start, end, callback):
        ray = self._get_ray()
        ray.body.position = start
        ray.end = end
        x = -start[0] + end[0]
        y = -start[1] + end[1]
        l = math.sqrt(x ** 2 + y ** 2)
        x *= 1000 / l
        y *= 1000 / l
        ray.body.velocity = (x, y)
        ray.callback = callback

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = RayManager()
        return cls._instance
