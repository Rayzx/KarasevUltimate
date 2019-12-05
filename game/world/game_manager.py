class GameManager:
    _instance = None

    def __init__(self):
        self._w = None
        self._player = None

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

    def create(self, world, player):
        self._w = world
        self._player = player

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance
