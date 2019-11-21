import abc

from game.render.render import Render
from game.world.world import World


class Screen:
    """
        общий интерфейс(декоратар) с которым работает ui_manager
        его реализует
    """

    @abc.abstractmethod
    def show(self):
        """
            вызывается при приклеплении экрана к менеджеру
        """
        pass

    @abc.abstractmethod
    def update(self, delta: float):
        """
            вызывается каждый раз, когда надо обновить экран
        :param delta: шаг по времени
        """
        pass

    @abc.abstractmethod
    def render(self):
        """
            вызывается каждый раз, когда надо отрисовать экран
        """
        pass

    @abc.abstractmethod
    def destroy(self):
        """
            вызывается при уничтожении экрана
        """
        pass

    def call(self, event):
        pass


class Screen_Menu(Screen):
    def show(self):
        pass

    def update(self, delta: float):
        pass

    def render(self):
        pass

    def destroy(self):
        pass


class Screen_Game(Screen):

    def __init__(self):
        self._world = World()
        self._render = Render()

    def show(self):
        pass

    def update(self, delta: float):
        self._world.step(delta)

    def render(self):
        self._render.draw_world(self._world)

    def destroy(self):
        pass

    def call(self, event):
        pass