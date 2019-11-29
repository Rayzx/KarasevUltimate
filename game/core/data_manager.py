import pygame


class AudioManager:
    _manager = None
    def __init__(self):
        _manager = self
        self.button = []
    
    @classmethod
    def instance(cls):
        """
        :return: экземпляр менеджера
        """
        if cls._manager is None:
            cls._manager = AudioManager()
        return cls._manager

    def button_sounds(self):
        self.button = [pygame.mixer.Sound('resources/sounds/200.wav'),pygame.mixer.Sound('resources/sounds/210.wav'),pygame.mixer.Sound('resources/sounds/220.wav')]

    def play_sound(self, sound):
        sound.play()
