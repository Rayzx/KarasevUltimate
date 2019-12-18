from game.core.tools import Pool, Poolable
from game.world.actor.actors import Dynamic, Structure, Item
from game.world.actor.data_actor import collision_type, CollisionType
from game.world.game_manager import GameManager


# from game.world.actor.gun import Explosion

class Bullet(Dynamic, Poolable):

    def __init__(self, x, y, velocity, max_time=-1.0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Circle,
                         vertices=5,
                         color='green',
                         mass=0.001)
        self.visible = False
        self.body.sensor = True
        self._alive = False
        self.shape.collision_type = collision_type[CollisionType.NoCollision]
        self.shape.elasticity = 1
        self.body.velocity = velocity
        self.damage = 1
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
        if not (isinstance(actor, Bullet) or isinstance(actor, Item)):
            self.life = self.life - 1
            return True
        return False

    def revive(self):
        self.visible = True
        self.body.sensor = False
        self.life = 1
        self._alive = True
        self._time = 0
        self.damage = 1
        self.shape.unsafe_set_radius(5)

    def reset(self):
        GameManager.instance().remove_actor(self)


class ExplosiveBullet(Bullet):
    explosionClass = None

    def __init__(self, x, y, velocity, max_time=1):
        super().__init__(x, y, velocity, max_time)

    def update(self, delta):
        if self._alive:
            self._time += delta
            if self._max_time != -1 and self._time >= self._max_time:
                self.explos()
                BulletManager.instance().return_bullet(self)
            elif self.life <= 0 or self.body.velocity.get_length_sqrd() < 10000:
                self.explos()
                BulletManager.instance().return_bullet(self)
            self.shape.unsafe_set_radius((lambda: 6.0 + self._time * 15.0 if self._time < 2 else 16.0)())

    def explos(self):
        from game.world.actor.gun import Explosion
        exp = Explosion()
        exp.shot(self.pos, [500, 0])

    def reset(self):
        GameManager.instance().remove_actor(self)


class BulletManager:
    _instance = None

    def __init__(self):
        def new_bullet():
            b = Bullet(0, 0, (0, 0))
            return b

        def new_expBullet():
            c = ExplosiveBullet(0, 0, (0, 0))
            return c

        self.bullet_pool = Pool(new_object=new_bullet, n=501)
        self.bulletExplosion_pool = Pool(new_object=new_expBullet, n=500)

    def get_bullet(self, n=1):
        if n > 1:
            bullets = [None] * n
            for i in range(n):
                b = self.bullet_pool.obtain()
                b.revive()
                bullets[i] = b
            GameManager.instance().add_actor(bullets)
            return bullets
        else:
            b = self.bullet_pool.obtain()
            b.revive()
            GameManager.instance().add_actor(b)
            return b

    def get_expBullet(self, n=1):
        if n > 1:
            bullets = [None] * n
            for i in range(n):
                b = self.bulletExplosion_pool.obtain()
                b.revive()
                bullets[i] = b
            GameManager.instance().add_actor(bullets)
            return bullets
        else:
            b = self.bulletExplosion_pool.obtain()
            b.revive()
            GameManager.instance().add_actor(b)
            return b

    def return_bullet(self, bullet):
        if isinstance(bullet, ExplosiveBullet):
            self.bulletExplosion_pool.free(bullet)
        else:
            self.bullet_pool.free(bullet)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BulletManager()
        return cls._instance
