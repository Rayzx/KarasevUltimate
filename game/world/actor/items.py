import math

from game.world.actor.actors import Item, Dynamic
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import Structure
from game.world.actor.effect import BoostEffect
from game.world.actor.gun import DefaultGun, TripleGun
from game.world.actor.player import Player
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
            isHeal = actor.heal(1)
            if isHeal:
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


class Nothing(Item):
    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[5, 0], [0, -5], [-5, 0], [0, 5]]),
                         color='white')

    def collision(self, actor=None):
        if isinstance(actor, Dynamic) and not isinstance(actor, Bullet):
            GameManager.instance().remove_actor(self)


class DefaultGunItem(Item):
    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[5, 0], [0, -5], [-5, 0], [0, 5]]),
                         color='green')

    def collision(self, actor=None):
        if isinstance(actor, Player) and not isinstance(actor, Bullet):
            actor.gun = DefaultGun()
            GameManager.instance().remove_actor(self)


class TripleGunItem(Item):
    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[5, 0], [0, -5], [-5, 0], [0, 5]]),
                         color='red')

    def collision(self, actor=None):
        if isinstance(actor, Player) and not isinstance(actor, Bullet):
            actor.gun = TripleGun()
            GameManager.instance().remove_actor(self)


class ExpBulletItem(Item):
    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[5, 0], [0, -5], [-5, 0], [0, 5]]),
                         color='yeallow')

    def collision(self, actor=None):
        if isinstance(actor, Player) and not isinstance(actor, Bullet):
            # уставить тип пули игроку/ его оружию
            GameManager.instance().remove_actor(self)
