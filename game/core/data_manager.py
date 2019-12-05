import json

import pygame


class Loader:
    pass


class FileManager:
    _instance = None

    def __init__(self):
        self._lib = {}

    def _load_setting(self):
        d = None
        try:
            output_file = open('resources/settings.json', 'r')
            d = json.loads(output_file.read())
            output_file.close()
        except FileNotFoundError as e:
            d = {"width": 800, "height": 600, "fps": True}
            j = json.dumps(d)
            f = open("resources/settings.json", "w")
            f.write(j)
            f.close()
        finally:
            self._lib.update({'setting': d})

    def load(self):
        self._load_setting()

    def save(self):
        pass

    def get(self, name):
        pass

    def set(self, name_dict, name_value, value):
        pass

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = FileManager()
        return cls._instance


class AudioManager:
    _manager = None

    def __init__(self):
        _manager = self
        self.button = ()
        self.button_sounds()

    @classmethod
    def instance(cls):
        """
        :return: экземпляр менеджера
        """
        if cls._manager is None:
            cls._manager = AudioManager()
        return cls._manager

    def button_sounds(self):
        self.button = (pygame.mixer.Sound('resources/sounds/200.ogg'), pygame.mixer.Sound('resources/sounds/210.ogg'),
                       pygame.mixer.Sound('resources/sounds/220.ogg'), pygame.mixer.Sound('resources/sounds/click.ogg'))

    def play_sound(self, sound):
        sound.play(fade_ms=0)
