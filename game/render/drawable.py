import abc

import pygame

from resources.resource_manager import Resource_Type


class Drawable:
    """
        класс для предоставления интерфейса рендеринга объектам
    """

    @abc.abstractmethod
    def get_type(self) -> Resource_Type:
        """
        :return: имя текстуры / тип который надо отрисовать
        """
        pass

    @abc.abstractmethod
    def get_rect(self) -> pygame.Rect:
        """
        :return: прямоугольник где надо отрисовать текстуру
        """
        pass
