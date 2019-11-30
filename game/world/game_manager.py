from game.world.body_factory import BodyFactory
from game.world.world import World


class GameManager:
    _instance = None

    def __init__(self):
        self._w = World()
        self._factory = BodyFactory(self._w)
        self._player = self._factory.create_player(150, 100)
        self._factory.create()

    def remove_actor(self, actor):
        if isinstance(actor, list) or isinstance(actor, tuple):
            for a in actor:
                self._w.remove_actor(a)
        else:
            self._w.remove_actor(actor)

    def add_actor(self, actor):
        if isinstance(actor, list) or isinstance(actor, tuple):
            for a in actor:
                self._w.add_actor(a)
        else:
            self._w.add_actor(actor)

    def get_player_pos(self):
        return self._player.pos

    def update(self, delta):
        self._w.step(delta)

    def draw(self, render):
        """
        :param render: то чем отрисовать объекты
        """
        if render is not None:
            render.draw_world(render.draw_world(self._w))

    def move(self, d=None):
        pass

    def direction(self, d=None):
        pass

    def click(self):
        pass

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance
