from game.ui_manager.mode_interface import Mode


class UIManager:
    _manager = None

    def __init__(self):
        UIManager._manager = self
        self._screen = None
        self._ready = False
        self._done = True

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

    def _get_done(self):
        return self._done

    def _set_done(self, value):
        self._done = value

    @classmethod
    def instance(cls):
        """
        :return: экземпляр менеджера
        """
        if cls._manager is None:
            cls._manager = UIManager()
        return cls._manager

    done = property(_get_done, _set_done, doc='Флаг на то живо ли сейчас приложение')
