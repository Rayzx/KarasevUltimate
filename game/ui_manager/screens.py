import math

import pygame
import json
from game.core.core import Core
from game.render.render import Render, Camera
from game.ui_manager.screen_interface import Mode, Button
from game.ui_manager.ui_manager import UIManager
from game.world.game_manager import GameManager


class ModeMenu(Mode):
    def __init__(self):
        f = open('resources/settings.json', 'r')
        self._dict_out = json.loads(f.read())
        f.close()
        self._screen_h = Core.instance().info().current_h
        self._screen_w = Core.instance().info().current_w
        self._buttons = [
            Button(int(self._screen_w / 3), int(self._screen_h / 8), int(self._screen_w / 3), int(self._screen_h / 8),
                   'Новая игра', lambda: UIManager.instance().set_screen(ModeGame())),
            Button(int(self._screen_w / 3), int(self._screen_h / 4) + int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), 'Выбрать разрешение',
                   lambda: UIManager.instance().set_screen(ModeSettings())),
            Button(int(self._screen_w / 3), int(3 * self._screen_h / 8) + 2 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8),
                   'Счетчик fps:{0}'.format((lambda x: "Вкл" if x else "Выкл")(self._dict_out["fps"])), self.toggle)]

    def show(self):
        pass

    def update(self, delta: float):
        pass

    def render(self):
        for button in self._buttons:
            button.draw()

    def destroy(self):
        pass

    def call(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self._buttons:
                button.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for b in self._buttons:
                if b.contain(mouse_pos):
                    b.clicked()

    def toggle(self):
        output_file = open('resources/settings.json', 'r')
        self._dict_out = json.loads(output_file.read())
        self._dict_out["fps"] = not self._dict_out["fps"]
        output_file.close()
        self._buttons[2].text = 'Счетчик fps:{0}'.format((lambda x: "Вкл" if x else "Выкл")(self._dict_out["fps"]))
        output_file = open('resources/settings.json', 'w')
        output_file.write(json.dumps(self._dict_out))
        output_file.close()
        Core.instance().update_settings(self._dict_out)
        UIManager.instance().screen = ModeMenu()


class ModeSettings(Mode):
    def __init__(self):
        self._resolutions = {0: [800, 600], 1: [1280, 720], 2: [1600, 900], 3: [1920, 1080]}
        self._screen_h = pygame.display.Info().current_h
        self._screen_w = pygame.display.Info().current_w
        self._buttons = [
            Button(int(self._screen_w / 3), int(self._screen_h / 10), int(self._screen_w / 3), int(self._screen_h / 8),
                   '800x600', self.reset),
            Button(int(self._screen_w / 3), int(self._screen_h / 5) + int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), '1280x720', self.reset),
            Button(int(self._screen_w / 3), int(3 * self._screen_h / 10) + 2 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), '1600x900', self.reset),
            Button(int(self._screen_w / 3), int(4 * self._screen_h / 10) + 3 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), '1920x1080', self.reset),
            Button(int(self._screen_w / 3), int(5 * self._screen_h / 10) + 4 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), 'Назад',
                   lambda x: UIManager.instance().set_screen(ModeMenu()))]

    def show(self):
        pass

    def render(self):
        for button in self._buttons:
            button.draw()

    def update(self, delta: float):
        pass

    def destroy(self):
        pass

    def reset(self, i):
        if i in self._resolutions:
            output_file = open('resources/settings.json', 'r')
            dict_out = json.loads(output_file.read())
            output_file.close()
            dict_out["width"] = self._resolutions[i][0]
            dict_out["height"] = self._resolutions[i][1]
            output_file = open('resources/settings.json', 'w')
            output_file.write(json.dumps(dict_out))
            output_file.close()
            Core.instance().update_settings(dict_out)
            UIManager.instance().set_screen(ModeSettings())

    def call(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self._buttons:
                button.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(0, len(self._buttons)):
                if self._buttons[i].contain(mouse_pos):
                    self._buttons[i].clicked(i)
                    break


class ModeGame(Mode):

    def __init__(self):
        self._game_manager = GameManager.instance()
        self._render = Render()
        self._screen_h = pygame.display.Info().current_h
        self._camera = Camera(Core.instance().info().current_w, self._screen_h)
        self._render.set_camera(self._camera)
        self._direction = 0

    def show(self):
        pass

    def update(self, delta: float):
        self._game_manager.update(delta)
        self._camera.pos = self._game_manager.get_player_pos()

    def render(self):
        self._game_manager.draw(self._render)

    def destroy(self):
        pass

    def call(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            p = self._game_manager.get_player_pos()
            p = self._camera.transform_coord(p.x, p.y)
            self._game_manager.set_direction(-math.atan2(mouse_pos[1] - p[1], mouse_pos[0] - p[0]))

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._game_manager.click()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self._direction |= 1
            if event.key == pygame.K_d:
                self._direction |= 2
            if event.key == pygame.K_s:
                self._direction |= 4
            if event.key == pygame.K_a:
                self._direction |= 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._direction &= ~1
            if event.key == pygame.K_d:
                self._direction &= ~2
            if event.key == pygame.K_s:
                self._direction &= ~4
            if event.key == pygame.K_a:
                self._direction &= ~8
