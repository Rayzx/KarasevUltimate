import pygame
import json
from game.core.core import Core
from game.render.render import Render
from game.ui_manager.screen_interface import Screen, Button
from game.ui_manager.ui_manager import Manager
from game.world.world import World
class Screen_Menu(Screen):
    def __init__(self):
        f = open('resources/settings.json', 'r')
        self._dict_out = json.loads(f.read())
        f.close()
        self._screen_h = pygame.display.Info().current_h
        self._screen_w = pygame.display.Info().current_w
        self._buttons = [Button(int(self._screen_w / 3), int(self._screen_h / 8), int(self._screen_w / 3), int(self._screen_h / 8), 'Новая игра',  lambda : self.manage(Screen_Game)),
                         Button(int(self._screen_w / 3), int(self._screen_h / 4) + int(self._screen_h / 8 * 0.29), int(self._screen_w / 3), int(self._screen_h / 8), 'Выбрать разрешение', lambda: self.manage(Screen_Settings)),
                         Button(int(self._screen_w / 3), int(3 * self._screen_h / 8) + 2 * int(self._screen_h / 8 * 0.29), int(self._screen_w / 3), int(self._screen_h / 8), 'Счетчик fps:{0}'.format((lambda x: "Вкл" if x else "Выкл")(self._dict_out["fps"])), self.toggle)]

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
            for i in range(0, len(self._buttons)):
                if self._buttons[i].collision(mouse_pos):
                    self._buttons[i].clicked()

    def toggle(self):
        output_file = open('resources/settings.json', 'r')
        self._dict_out = json.loads(output_file.read())
        self._dict_out["fps"] = not self._dict_out["fps"]
        print(self._dict_out)
        output_file.close()
        self._buttons[2].text = 'Счетчик fps:{0}'.format((lambda x: "Вкл" if x else "Выкл")(self._dict_out["fps"]))
        output_file = open('resources/settings.json', 'w')
        output_file.write(json.dumps(self._dict_out))
        output_file.close()
        Core().instance().update_settings(self._dict_out)
        Manager.instance().screen = Screen_Menu()

    def manage(self, i):
        Manager.instance().screen = i()
 

class Screen_Settings(Screen):
    def __init__(self):
        self._resolutions = {0: [800, 600], 1: [1280, 720], 2: [1600, 900], 3: [1920, 1080]}
        self._screen_h = pygame.display.Info().current_h
        self._screen_w = pygame.display.Info().current_w
        self._buttons = [Button(int(self._screen_w / 3), int(self._screen_h / 10), int(self._screen_w / 3), int(self._screen_h / 8), '800x600', self.reset),
                         Button(int(self._screen_w / 3), int(self._screen_h / 5) + int(self._screen_h / 8 * 0.29), int(self._screen_w / 3), int(self._screen_h / 8), '1280x720', self.reset),
                         Button(int(self._screen_w / 3), int(3 * self._screen_h / 10) + 2 * int(self._screen_h / 8 * 0.29), int(self._screen_w / 3), int(self._screen_h / 8), '1600x900', self.reset),
                         Button(int(self._screen_w / 3), int(4 * self._screen_h / 10) + 3 * int(self._screen_h / 8 * 0.29), int(self._screen_w / 3), int(self._screen_h / 8), '1920x1080', self.reset),
                         Button(int(self._screen_w / 3), int(5 * self._screen_h / 10) + 4 * int(self._screen_h / 8 * 0.29), int(self._screen_w / 3), int(self._screen_h / 8), 'Назад', lambda x:  self.manage(Screen_Menu))]
    def show(self):
        pass

    def render(self):
        for button in self._buttons:
            button.draw()

    def update(self, delta: float):
        pass

    def manage(self, i):
        Manager.instance().screen = i()

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
            Core().instance().update_settings(dict_out)
            Manager.instance().screen = Screen_Settings()

    def call(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self._buttons:
                button.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(0, len(self._buttons)):
                if (self._buttons[i].collision(mouse_pos)):
                    self._buttons[i].clicked(i)
                    break
            else:
                Manager

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
