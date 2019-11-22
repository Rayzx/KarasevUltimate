from game.ui_manager.screen_interface import Screen


class MetaSingleton_Manager(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton_Manager, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Manager(metaclass=MetaSingleton_Manager):
    _manager = None

    def __init__(self):
        Manager._manager = self
        self._screen = None
        self._ready = False

    def _set_screen(self, screen: Screen):
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

    def _get_screen(self):
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
            cls._manager = Manager()
        return cls._manager

    screen = property(_get_screen, _set_screen)
