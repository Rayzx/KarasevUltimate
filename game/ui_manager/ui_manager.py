from game.ui_manager.mode_interface import Mode


class UIManager:
    _manager = None

    def __init__(self):
        UIManager._manager = self
        self._screen = None
        self._ready = False

    def set_screen(self, screen: Mode):
        """
        :type screen: экран, который надо установить
        """
        if screen is not None:
            self._ready = True
            self._screen = screen
            screen.show()
        else:
            self._screen.destroy()
            self._ready = True
            self._screen = screen
            screen.show()
        return True

    def get_screen(self):
        return self._screen

    def update(self, delta: float):
        """

        :param delta:
        """
        if self._ready:
            self._screen.update(delta)

    def render(self):
        if self._ready:
            self._screen.render()

    @classmethod
    def instance(cls):
        """
        :return: экземпляр менеджера
        """
        if cls._manager is None:
            cls._manager = UIManager()
        return cls._manager
