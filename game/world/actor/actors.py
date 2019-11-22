class Actor:
    """
        Hello! Greetings
    """

    def __init__(self):
        self._body = None
        self._shape = None
        self._Image_Name = None
        self._rect = None
        self._color = None
        self._isVisible = True

    def update(self, delta: float):
        """

        :param delta:
        """
        pass

    def _get_image(self):
        return self._Image_Name

    def _set_image(self, value):
        self._Image_Name = value

    def _get_rect(self):
        return self._rect

    def _set_rect(self, value):
        self._rect = value

    def _get_color(self):
        return self._color

    def _set_color(self, value):
        self._color = value

    def _get_body(self):
        return self._body

    def _set_body(self, value):
        self._body = value

    def _get_shape(self):
        return self._shape

    def _set_shape(self, value):
        self._shape = value

    def _set_isVisible(self,value):
        self._isVisible = value

    def _get_isVisible(self):
        return self._isVisible

    image = property(_get_image, _set_image, doc="")
    body = property(_get_body, _set_body, doc="")
    shape = property(_get_shape, _set_shape, doc="")
    rect = property(_get_rect, _set_rect, doc="")
    color = property(_get_color, _set_color, doc="")
    visible = property(_get_isVisible, _set_isVisible, doc="good thing!" )

class Static(Actor):
    pass


class Dynamic(Actor):
    pass


class Item(Actor):
    pass
