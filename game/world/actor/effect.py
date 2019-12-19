class Effect:
    """
        общий суперкласс для всех эффектов
    """

    def __init__(self):
        self._life_time = 0
        self._current_time = 0
        self._actor = None

    def update(self, delta):
        """
        :param delta: временной шаг
        """
        pass

    def is_alive(self):
        """
            проверяет применяется ли еще эффект
        """
        return self.current_time <= self.life_time

    def _get_actor(self):
        return self._actor

    def _set_actor(self, value):
        self._actor = value

    def _del_actor(self):
        self._actor = None

    def _get_life_time(self):
        return self._life_time

    def _set_life_time(self, value):
        self._life_time = value

    def _del_life_time(self):
        self._life_time = 0

    def _get_current_time(self):
        return self._current_time

    def _set_current_time(self, value):
        self._current_time = value

    def _del_current_time(self):
        self._current_time = 0

    actor = property(_get_actor, _set_actor, _del_actor, doc="актер к которому привязал эффект")
    life_time = property(_get_life_time, _set_life_time, _del_life_time, doc="время применения эффекта")
    current_time = property(_get_current_time, _set_current_time, _del_current_time,
                            doc="время которое эффект применяется")


class BoostEffect(Effect):

    def __init__(self, actor):
        super().__init__()
        self.life_time = 5
        self.actor = actor
        actor.speed = 800

    def update(self, delta):
        self.current_time += delta
        self.actor.speed = 800
        if not self.is_alive():
            self.actor.speed = 200
            self.actor.del_effect(self)
