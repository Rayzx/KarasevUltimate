import math

from game.world.actor.actors import Item, Dynamic
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import Structure
from game.world.actor.effect import BoostEffect
from game.world.game_manager import GameManager


class Heal(Item):

    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[5, 0], [0, -5], [-5, 0], [0, 5]]),
                         color='green')
        self._heal_point = 10

    def collision(self, actor=None):
        if isinstance(actor, Dynamic) and not isinstance(actor, Bullet):
            actor.life += self._heal_point
            GameManager.instance().remove_actor(self)


class Boost(Item):
    def __init__(self, x, y, angle=0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[-10, 8], [10, 0], [-10, -8]]),
                         color='blue')
        self.velocity = [800 * math.cos(angle), 800 * math.sin(angle)]
        self.body.angle = angle

    def collision(self, actor=None):
        if isinstance(actor, Dynamic):
            effect = BoostEffect(actor)
            actor.add_effect(effect)
        return True
