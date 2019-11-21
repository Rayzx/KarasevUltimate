from game.render.render import Render
from game.ui_manager.screen_interface import Screen
from game.world.world import World


class Screen_Menu(Screen):

    def show(self):
        pass

    def update(self, delta: float):
        pass

    def render(self):
        pass

    def destroy(self):
        pass

    def call(self, event):
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
