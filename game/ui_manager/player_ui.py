from game.ui_manager.widgets import ProgressBar
import pygame

class PlayerUI():

    def __init__(self,player):
        self.isShow = 1
        self._player = player
        self._widgets = [ProgressBar(50, 50, 400, 50, 100, pygame.color.THECOLORS['red'],pygame.color.THECOLORS['gray70']) ]

    def update(self):
        for i in self._widgets:
            i.update(self._player.health)


    def draw(self):
        if (self.isShow == 1):
            for i in self._widgets:
                i.draw()
