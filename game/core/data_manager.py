import json
from enum import Enum

import pygame


class FileName(Enum):
    Setting = 0
    Level_0 = 1
    Level_1 = 2


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
        except FileNotFoundError:
            d = {"width": 800, "height": 600, "fps": True, "debug": False, "wall_debug": False}
            j = json.dumps(d)
            f = open("resources/settings.json", "w")
            f.write(j)
            f.close()
        finally:
            self._lib.update({FileName.Setting: d})

    def _load_level(self):
        output_file = open('resources/levels/demo_level.json')
        d = json.loads(output_file.read())
        output_file.close()
        self._lib.update({FileName.Level_0: d})

    def _save_setting(self):
        d = self._lib[FileName.Setting]
        j = json.dumps(d)
        f = open("resources/settings.json", "w")
        f.write(j)
        f.close()

    def _save_level(self):
        d = self._lib[FileName.Level_0]
        j = json.dumps(d)
        f = open('resources/levels/demo_level.json', "w")
        f.write(j)
        f.close()

    def load(self):
        self._load_level()
        self._load_setting()

    def save(self):
        self._save_setting()
        self._save_level()

    def get(self, name_dict, name_value):
        return self._lib[name_dict][name_value]

    def set(self, name_dict, name_value, value):
        self._lib[name_dict][name_value] = value

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = FileManager()
        return cls._instance


class SoundName(Enum):
    Sound1 = 0
    Sound2 = 1
    Sound3 = 2
    Sound4 = 3
    Sound5 = 4
    Sound6 = 5


class AudioManager:
    _manager = None

    def __init__(self):
        _manager = self
        self._sounds = {}
        self._button_sounds()

    def _button_sounds(self):
        self._sounds = {SoundName.Sound1: pygame.mixer.Sound('resources/sounds/200.ogg'),
                        SoundName.Sound2: pygame.mixer.Sound('resources/sounds/210.ogg'),
                        SoundName.Sound3: pygame.mixer.Sound('resources/sounds/220.ogg'),
                        SoundName.Sound4: pygame.mixer.Sound('resources/sounds/click.ogg'),
                        SoundName.Sound5: pygame.mixer.Sound('resources/sounds/PlayerShoot.ogg'),
                        SoundName.Sound6: pygame.mixer.Sound('resources/sounds/EnemyShoot.ogg')}

    def play_sound(self, sound):
        self._sounds[sound].play(fade_ms=0)

    @classmethod
    def instance(cls):
        """
        :return: экземпляр менеджера
        """
        if cls._manager is None:
            cls._manager = AudioManager()
        return cls._manager
    def set_music(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(-1)