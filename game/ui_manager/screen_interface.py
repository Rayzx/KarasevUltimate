import abc


class Screen:
    """
        общий интерфейс(декоратар) с которым работает ui_manager
    """

    @abc.abstractmethod
    def show(self):
        """
            вызывается при приклеплении экрана к менеджеру
        """
        pass

    @abc.abstractmethod
    def update(self, delta: float):
        """
            вызывается каждый раз, когда надо обновить экран
        :param delta: шаг по времени
        """
        pass

    @abc.abstractmethod
    def render(self):
        """
            вызывается каждый раз, когда надо отрисовать экран
        """
        pass

    @abc.abstractmethod
    def destroy(self):
        """
            вызывается при уничтожении экрана
        """
        pass

    @abc.abstractmethod
    def call(self, event):
        """
            вызывается ядром при обработке действий
        :param event:
        """
        pass
