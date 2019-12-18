from game.ui_manager.widgets import ProgressBar
import pygame


class PlayerUI:

    def __init__(self, player):
        self.isShow = 1
        self._player = player
        self._widgets = [
            ProgressBar(50, 50, 400, 30, 100, pygame.color.THECOLORS['red'], pygame.color.THECOLORS['gray70'])]

    def is_alive(self):
        return self._player.life > 0

    def update(self):
        for i in self._widgets:
            i.update(self._player.life/self._player.maxLife*100)

    def draw(self):
        if self.isShow == 1:
            for i in self._widgets:
                i.draw()
