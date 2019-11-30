import pygame
import pymunk
import resources.resource_manager as rm


class Actor:
    """
        Hello! Greetings
    """

    # имена коллизия для pymunk
    collision_type = {
        'NoCollision': 0,
        'Bullet': 1,
        'Player': 2,
        'Ghost': 3,
        'Environment': 4
    }

    def __init__(self, t=None, color=None):
        self._body = None
        self._shape = None
        self._rect = None
        self._image_Name = t
        self._color = color
        self._isVisible = True
        self._life = 1

    def update(self, delta: float):
        """

        :param delta:
        """
        pass

    def collision(self, actor=None):
        pass

    def _create_body(self, position, body_type, image_type, vertices, mass=0):
        if body_type == pymunk.Body.STATIC:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        elif body_type == pymunk.Body.DYNAMIC:
            if image_type == rm.Image_Name.Polygon:
                self.body = pymunk.Body(mass, pymunk.moment_for_poly(mass, vertices, (0, 0)),
                                        body_type=pymunk.Body.DYNAMIC)
            elif image_type == rm.Image_Name.Circle:
                self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, vertices, 0, (0, 0)),
                                        body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(position)
        self.body.data = self
        if image_type == rm.Image_Name.Polygon:
            self.shape = pymunk.Poly(self.body, vertices)
        elif image_type == rm.Image_Name.Circle:
            self.shape = pymunk.Circle(self.body, vertices)

    def _get_image(self):
        return self._image_Name

    def _set_image(self, value):
        self._image_Name = value

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

    def _get_isVisible(self):
        return self._isVisible

    def _set_isVisible(self, value):
        self._isVisible = value

    def _get_pos(self):
        return self.body.position

    def _get_life(self):
        return self._life

    def _set_life(self, value):
        self._life = value

    image = property(_get_image, _set_image, doc="возращает тип изображения, которое надо отрисовать")
    body = property(_get_body, _set_body, doc="возращает pymunk тело актера")
    shape = property(_get_shape, _set_shape, doc="возращает pymunk форму актера")
    rect = property(_get_rect, _set_rect, doc="возращает какую-то хйню")
    color = property(_get_color, _set_color, doc="возращает цвет")
    visible = property(_get_isVisible, _set_isVisible, doc="good thing!")
    pos = property(_get_pos)
    life = property(_get_life, _set_life)


class Static(Actor):
    def __init__(self, x, y, t, vertices, color):
        """
        :param x:
        :param y:
        :param t: тип формы
        :param vertices: масив вершин/радиус
        :param color:
        """
        super().__init__(t, color)
        self._create_body((x, y), pymunk.Body.STATIC, t, vertices)


class Dynamic(Actor):

    def __init__(self, x, y, t, vertices, color, mass=10):
        super().__init__(t, color)
        self.rect = pygame.Rect(500, 450.0, 50, 50)
        self._create_body((x, y), pymunk.Body.DYNAMIC, t, vertices, mass)


class Item(Actor):
    pass
