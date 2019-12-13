from game.world.actor.actors import Static, Dynamic, Actor
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import Structure, collision_type, CollisionType
from game.world.actor.gun import Explosion
from game.world.game_manager import GameManager


class Wall(Static):

    def __init__(self, x, y, t=Structure.Circle, vertices=10, color='orange4'):
        super().__init__(x, y, t, self.center(vertices), color)
        self.shape.elasticity = 1
        self.shape.friction = 100

    def set_friction(self, value):
        self.shape.friction = value
        return self

    def set_elasticity(self, value):
        self.shape.elasticity = value
        return self


class Barrel(Dynamic):
    """
        бочка при попабании снаряда взрывается
    """

    def __init__(self, x, y, t, vertices, color):
        super().__init__(x=x,
                         y=y,
                         t=t,
                         vertices=Actor.center(vertices),
                         color=color)
        self.shape.collision_type = collision_type[CollisionType.Environment]
        self.shape.elasticity = 1
        self.shape.friction = 1

        self.body.velocity_func = Dynamic.speed_update_body

        self.gun = Explosion.instance()

    def update(self, delta: float):
        if self.life <= 0:
            if isinstance(self.gun, Explosion):
                self.gun.shot(self.pos, [500, 0])
            GameManager.instance().remove_actor(self)

    def collision(self, actor=None):
        if isinstance(actor, Bullet):
            self.life -= 1
        return True


class Box(Dynamic):
    """
     при попадании снаряда(ов) ломается
    """

    def __init__(self, x, y, t, vertices, color, life=1):
        super().__init__(x=x,
                         y=y,
                         t=t,
                         vertices=Actor.center(vertices),
                         color=color)
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.shape.collision_type = collision_type[CollisionType.Environment]

        self.body.velocity_func = Dynamic.speed_update_body

        self.life = life

    def update(self, delta: float):
        if self.life <= 0:
            GameManager.instance().remove_actor(self)

    def collision(self, actor=None):
        if isinstance(actor, Bullet):
            self.life -= 1
        return True
