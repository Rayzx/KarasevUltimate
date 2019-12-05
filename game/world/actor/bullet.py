from game.core.Tools import Pool, Poolable
from game.world.actor.actors import Dynamic, Actor
from game.world.game_manager import GameManager
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
        self._alive = False
        self.shape.collision_type = Actor.collision_type['NoCollision']
        self.shape.elasticity = 1
        self.body.velocity = velocity
        self._time = 0.0
        self._max_time = max_time

    def update(self, delta: float):
        if self._alive:
            self._time += delta
            if self._max_time != -1 and self._time >= self._max_time:
                BulletManager.instance().return_bullet(self)
            elif self.life <= 0 or self.body.velocity.get_length_sqrd() < 10000:
                BulletManager.instance().return_bullet(self)

    def collision(self, actor=None):
        if not isinstance(actor,Bullet):
            self.life = self.life - 1

    def revive(self):
        self.visible = True
        self.body.sensor = False
        self.life = 1
        self._alive = True
        self._time = 0

    def reset(self):
        self._alive = False
        self.visible = False
        self.body.velocity = (0, 0)
        self.body.sensor = True
        self._max_time = -1
        self.shape.collision_type = Actor.collision_type['NoCollision']


class BulletManager:
    _instance = None

    def __init__(self):
        def new_bullet():
            b = Bullet(0, 0, (0, 0))
            GameManager.instance().add_actor(b)
            return b
        self.bullet_pool = Pool(new_object=new_bullet)

    def get_bullet(self) -> Bullet:
        b = self.bullet_pool.obtain()
        b.revive()
        return b

    def return_bullet(self, bullet):
        self.bullet_pool.free(bullet)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BulletManager()
        return cls._instance
