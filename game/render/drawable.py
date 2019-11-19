import abc


class Drawable:
    """
        класс для предоставления интерфейса рендеринга объектам
    """

    @abc.abstractmethod
    def get_type(self):
        """
        :return: имя текстуры / тип который надо отрисовать
        """
        pass

    @abc.abstractmethod
    def get_rect(self):
        """
        :return: прямоугольник где надо отрисовать текстуру
        """
        pass

    @abc.abstractmethod
    def get_color(self):
        pass