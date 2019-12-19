import math

from game.core.data_manager import FileName
from game.world.actor.actors import Item, Dynamic
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import Structure
from game.world.actor.effect import BoostEffect
from game.world.actor.gun import DefaultGun, TripleGun
from game.world.actor.player import Player
from game.world.game_manager import GameManager


class Heal(Item):
    vertex = [[5, 0], [0, -5], [-5, 0], [0, 5]]
    color = 'green'

    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center(self.vertex),
                         color=self.color)
        self._heal_point = 10

    def collision(self, actor=None):
        if isinstance(actor, Dynamic) and not isinstance(actor, Bullet):
            isHeal = actor.heal(1)
            if isHeal:
                GameManager.instance().remove_actor(self)


class Boost(Item):
    vertex = [[5, 0], [0, -5], [-5, 0], [0, 5]]
    color = 'blue'

    def __init__(self, x, y, angle=0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center(self.vertex),
                         color=self.color)
        self.velocity = [800 * math.cos(angle), 800 * math.sin(angle)]
        self.body.angle = angle

    def collision(self, actor=None):
        if isinstance(actor, Dynamic):
            effect = BoostEffect(actor)
            actor.add_effect(effect)
            GameManager.instance().remove_actor(self)
        return True


class Nothing(Item):
    vertex = [[5, 0], [0, -5], [-5, 0], [0, 5]]
    color = 'white'

    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center(self.vertex),
                         color=self.color)

    def collision(self, actor=None):
        if isinstance(actor, Dynamic) and not isinstance(actor, Bullet):
            GameManager.instance().remove_actor(self)


class Portal(Item):
    vertex = [[5, 0], [0, -5], [-5, 0], [0, 5]]
    color = (0, 255, 255)

    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Circle,
                         vertices=30,
                         color=self.color)

    def collision(self, actor=None):
        if isinstance(actor, Player) and not isinstance(actor, Bullet):
            GameManager.update_level(FileName.Boss0)
            # GameManager.instance().remove_actor(self)


class TripleGunItem(Item):
    vertex = [[5, 0], [0, -5], [-5, 0], [0, 5]]
    color = 'red'

    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center(self.vertex),
                         color=self.color)

    def collision(self, actor=None):
        if isinstance(actor, Player) and not isinstance(actor, Bullet):
            actor.changeGun(gun=1)
            GameManager.instance().remove_actor(self)


class ExpBulletItem(Item):
    vertex = [[10, 0], [0, -10], [-10, 0], [0, 10]]
    color = 'yellow'

    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center(self.vertex),
                         color=self.color)

    def collision(self, actor=None):
        if isinstance(actor, Player) and not isinstance(actor, Bullet):
            # уставить тип пули игроку/ его оружию
            actor.changeGun(bullet=1)
            GameManager.instance().remove_actor(self)


class SetterItem(Item):
    def __init__(self, x, y):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=self.center([[-10, 8], [10, 0], [-10, -8]]),
                         color='white')
        self._type_item = 0

    def collision(self, actor=None):
        return True

    def _set_item(self, value):
        value %= 6
        if value == 0:
            self.shape.unsafe_set_vertices(Nothing.vertex)
            self.color = Nothing.color
        if value == 1:
            self.shape.unsafe_set_vertices(Nothing.vertex)
            self.color = Portal.color
        if value == 2:
            self.shape.unsafe_set_vertices(Nothing.vertex)
            self.color = TripleGunItem.color
        if value == 3:
            self.shape.unsafe_set_vertices(Nothing.vertex)
            self.color = ExpBulletItem.color
        if value == 4:
            self.shape.unsafe_set_vertices(Nothing.vertex)
            self.color = Heal.color
        if value == 5:
            self.shape.unsafe_set_vertices(Nothing.vertex)
            self.color = Boost.color
        self._type_item = value

    def _get_item(self):
        return self._type_item

    type_item = property(_get_item, _set_item)
