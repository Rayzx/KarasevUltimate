class GameManager:
    _instance = None

    def __init__(self):
        self._w = None
        self._player = None

    def remove_actor(self, actor):
        self._w.remove_actor(actor)

    def add_actor(self, actor):
        self._w.add_actor(actor)

    def get_player_pos(self):
        return self._player.pos

    def create(self, world, player):
        self._w = world
        self._player = player

    def get_space(self):
        return self._w.get_space()

    @staticmethod
    def update_level(level):
        from game.ui_manager.modes import GameMode as gm
        from game.ui_manager.ui_manager import UIManager as ui
        ui.instance().get_screen().destroy()
        ui.instance().set_screen(gm(level))

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance
