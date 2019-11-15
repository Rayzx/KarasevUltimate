from abc import ABC

from game.render.drawable import Drawable


class Actor(Drawable, ABC):

    def update(self, delta: float):
        pass


class Static(Actor, ABC):
    pass


class Dynamic(Actor, ABC):
    pass


class Item(Actor, ABC):
    pass
