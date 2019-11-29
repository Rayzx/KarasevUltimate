class Manager:
    _instance = None

    def __init__(self):
        self._w = None
        self._player = None

    def remove_actor(self, actor):
        if isinstance(actor, list) or isinstance(actor, tuple):
            for a in actor:
                self._w.instance().remove_actor(a)
        else:
            self._w.instance().remove_actor(actor)

    def add_actor(self, actor):
        if isinstance(actor, list) or isinstance(actor, tuple):
            for a in actor:
                self._w.instance().add_actor(a)
        else:
            self._w.instance().add_actor(actor)

    def get_body(self):
        pass

    def get_shape(self):
        pass

    def set_world(self, world):
        self._w = world

    def set_player(self, player):
        self._player = player

    def get_player_pos(self):
        return self._player.pos

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Manager()
        return cls._instance


class BodyFactory:
    pass
