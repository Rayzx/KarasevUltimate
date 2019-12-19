import json
from enum import Enum

import pygame


class FileName(Enum):
    Setting = -1
    Player_Stats = 0

    Level_0 = 1
    Boss0 = 2
    Level_999 = 999

class FileManager:
    _instance = None

    def __init__(self):
        self._lib = {}
        self._level = None

    def _load_setting(self):
        d = None
        try:
            output_file = open('resources/settings.json', 'r')
            d = json.loads(output_file.read())
            output_file.close()
        except FileNotFoundError:
            d = {"width": 800, "height": 600, "fps": True, "debug": False, "wall_debug": False, "volume": 1,
                 'music_volume': 1}
            j = json.dumps(d)
            f = open("resources/settings.json", "w")
            f.write(j)
            f.close()
        finally:
            self._lib.update({FileName.Setting: d})

    def _load_player_stat(self):
        output_file = open('resources/playerStats.json')
        d = json.loads(output_file.read())
        output_file.close()
        self._lib.update({FileName.Player_Stats: d})

    def load_level(self, value):
        if value in self._lib:
            del self._lib[self._level]
        self._level = value
        output_file = open('resources/levels/' + str(self._level.name) + '.json')
        d = json.loads(output_file.read())
        output_file.close()
        self._lib.update({value: d})

    def _save_setting(self):
        d = self._lib[FileName.Setting]
        j = json.dumps(d)
        f = open("resources/settings.json", "w")
        f.write(j)
        f.close()

    def save_player_stats(self):
        d = self._lib[FileName.Player_Stats]
        j = json.dumps(d)
        f = open('resources/playerStats.json', "w")
        f.write(j)
        f.close()

    def save_level(self):
        d = self._lib[self._level]
        j = json.dumps(d)
        f = open('resources/levels/' + str(self._level.name) + '.json', "w")
        f.write(j)
        f.close()

    def load(self):
        self._load_player_stat()
        self._load_setting()

    def save(self):
        self.save_player_stats()
        self._save_setting()
        self.save_level()

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
        print(FileManager.instance().get(FileName.Setting, 'volume'))
        for key in self._sounds:
            self._sounds[key].set_volume(FileManager.instance().get(FileName.Setting, 'volume'))
        pygame.mixer.music.set_volume(FileManager.instance().get(FileName.Setting, 'music_volume'))

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

    def set_volume(self):
        for key in self._sounds:
            self._sounds[key].set_volume(FileManager.instance().get(FileName.Setting, 'volume'))
        pygame.mixer.music.set_volume(FileManager.instance().get(FileName.Setting, 'music_volume'))
