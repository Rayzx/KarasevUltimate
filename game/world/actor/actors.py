import pymunk

from game.world.actor.data_actor import Structure, Stats


class MyBody(pymunk.Body):
    def __init__(self, mass=0, moment=0, body_type=pymunk.Body.DYNAMIC):
        super().__init__(mass, moment, body_type)
        self._data = None

    def _set_data(self, data):
        self._data = data

    def _get_data(self):
        return self._data

    def _del_data(self):
        self._data = None

    data = property(_get_data, _set_data, _del_data)


class Actor:
    """
        Hello! Greetings
    """

    def __init__(self, t=None, color=None):
        self._body = None
        self._shape = None
        self._structure = t
        self._isVisible = True
        self._live = 1
        self._effect = None
        self._stats = {
            Stats.Health: 1,
            Stats.Color: color,
            Stats.Pos: 1  # self.pos
        }
        self.stats_update = False

    def update(self, delta: float):
        pass

    def collision(self, actor=None):
        return True

    def get_stat(self, name):
        return self._stats[name]

    def set_stat(self, name, value):
        self.stats_update = True
        self._stats[name] = value

    def _create_body(self, position, body_type, image_type, vertices, mass=0):
        if body_type == pymunk.Body.STATIC:
            self.body = MyBody(body_type=pymunk.Body.STATIC)
        elif body_type == pymunk.Body.DYNAMIC:
            if image_type == Structure.Polygon:
                self.body = MyBody(mass, pymunk.moment_for_poly(mass, vertices, (0, 0)),
                                   body_type=pymunk.Body.DYNAMIC)
            elif image_type == Structure.Circle:
                self.body = MyBody(mass, pymunk.moment_for_circle(mass, vertices, 0, (0, 0)),
                                   body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(position)
        self.body.data = self

        if image_type == Structure.Polygon:
            self.shape = pymunk.Poly(self.body, vertices)
        elif image_type == Structure.Circle:
            self.shape = pymunk.Circle(self.body, vertices)

    def _get_effect(self):
        return self._effect

    def _set_effect(self, value):
        self._effect = value

    def _del_effect(self):
        self.effect = None

    def _get_structure(self):
        return self._structure

    def _set_structure(self, value):
        self._structure = value

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

    effect = property(_get_effect, _set_effect, _del_effect, doc="эффект который несет в себе актер")
    structure = property(_get_structure, _set_structure, doc="возращает тип изображения, которое надо отрисовать")
    body = property(_get_body, _set_body, doc="возращает pymunk тело актера")
    shape = property(_get_shape, _set_shape, doc="возращает pymunk форму актера")
    visible = property(_get_isVisible, _set_isVisible, doc="good thing!")
    pos = property(_get_pos)

    @staticmethod
    def center(vertices):
        if isinstance(vertices, int):
            return vertices
        x, y = 0.0, 0.0
        for v in vertices:
            x += v[0]
            y += v[1]
        x /= len(vertices)
        y /= len(vertices)
        for v in vertices:
            v[0] -= x
            v[1] -= y
        return vertices


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
    max_velocity = 2000
    min_velocity = 1
    coefficient_of_friction = 3

    def __init__(self, x, y, t, vertices, color, mass=100):
        super().__init__(t, color)
        self._create_body((x, y), pymunk.Body.DYNAMIC, t, vertices, mass)

    @staticmethod
    def speed_update_body(body, gravity, damping, dt):
        if isinstance(body, pymunk.Body) and isinstance(body.velocity, pymunk.Vec2d):
            ll = body.velocity.length
            if ll == 0:
                return
            v = -body.velocity / ll
            v *= body.mass * body.shapes.pop().friction * Dynamic.coefficient_of_friction
            v += gravity
            pymunk.Body.update_velocity(body, v, damping, dt)

            if ll > Dynamic.max_velocity:
                scale = Dynamic.max_velocity / ll
                body.velocity = body.velocity * scale
            if ll < 1:
                body.velocity = body.velocity * 0


class Item(Actor):
    pass
