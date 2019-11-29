import pygame


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
        self.button = (pygame.mixer.Sound('resources/sounds/200.ogg'),pygame.mixer.Sound('resources/sounds/210.ogg'),pygame.mixer.Sound('resources/sounds/220.ogg'),pygame.mixer.Sound('resources/sounds/click.ogg'))

    def play_sound(self, sound):
        sound.play(fade_ms=0)
