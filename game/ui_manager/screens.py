import pygame

from game.render.render import Render, Camera
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
    """
        todo возможно камера не будет работать из-за странного разрешения экрана на винде
        todo перенести получение информации об экране в Core.instance после слияние веток
    """

    def __init__(self):
        self._world = World()
        self._render = Render()
        infoObject = pygame.display.Info()
        self._player = self._world.create_player(200, 200)
        self._camera = Camera(infoObject.current_w, infoObject.current_h)
        self._render.set_camera(self._camera)

    def show(self):
        pass

    def update(self, delta: float):
        self._world.step(delta)
        self._camera.pos = self._player.body.position

    def render(self):
        self._render.draw_world(self._world)

    def destroy(self):
        pass

    def call(self, event):
        pass
