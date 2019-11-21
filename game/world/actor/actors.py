class Actor:
    """
        Hello!
    """

    def __init__(self):
        self._angle = 0
        self._texture_name = None
        self._rect = None
        self._color = None

    def update(self, delta: float):
        """

        :param delta:
        """
        pass

    def _get_texture(self):
        return self._texture_name

    def _set_texture(self, value):
        self._texture_name = value

    def _get_rect(self):
        return self._rect

    def _set_rect(self, value):
        self._rect = value

    def _get_color(self):
        return self._color

    def _set_color(self, value):
        self._color = value

    def _get_angle(self):
        return self._angle

    def _set_angle(self, value):
        self._angle = value

    texture = property(_get_texture, _set_texture, doc="")
    angle = property(_get_angle, _set_angle, doc="")
    rect = property(_get_rect, _set_rect, doc="")
    color = property(_get_color, _set_color, doc="")


class Static(Actor):
    pass


class Dynamic(Actor):
    pass


class Item(Actor):
    pass
