import pymunk

from game.world.actor.data_actor import Structure, CollisionType, collision_type


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
        self._color = color
        self._isVisible = True
        self._live = 1
        self._own_effect = None

    def update(self, delta: float):
        pass

    def collision(self, actor=None):
        return True

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

    def _get_structure(self):
        return self._structure

    def _set_structure(self, value):
        self._structure = value

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
        return self._live

    def _set_life(self, value):
        self._live = value

    def _get_own_effect(self):
        return self._own_effect

    def _set_own_effect(self, value):
        self._own_effect = value

    def del_own_effect(self):
        self._own_effect = None

    structure = property(_get_structure, _set_structure, doc="возращает тип изображения, которое надо отрисовать")
    body = property(_get_body, _set_body, doc="возращает pymunk тело актера")
    shape = property(_get_shape, _set_shape, doc="возращает pymunk форму актера")
    color = property(_get_color, _set_color, doc="возращает цвет")
    visible = property(_get_isVisible, _set_isVisible, doc="good thing!")
    pos = property(_get_pos)
    life = property(_get_life, _set_life)
    own_effect = property(_get_own_effect, _set_own_effect, del_own_effect, doc='эффект, который носит в себе актер')

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
        self.shape.collision_type = collision_type[CollisionType.Environment]


class Dynamic(Actor):

    def __init__(self, x, y, t, vertices, color, mass=10):
        super().__init__(t, color)
        self._effects = []
        self._speed = 200
        self._create_body((x, y), pymunk.Body.DYNAMIC, t, vertices, mass)
        self.life = 1
        self.maxLife = 1

    def add_effect(self, value):
        self._effects.append(value)

    def del_effect(self, value):
        self._effects.remove(value)

    def get_effects(self):
        return self._effects

    def update_effects(self, delta):
        for effect in self._effects:
            effect.update(delta)

    def _get_speed(self):
        return self._speed

    def _set_speed(self, value):
        self._speed = value

    speed = property(_get_speed, _set_speed)

    def dealDamage(self, damage):
        """
        :param damage: урон
        """
        if self.life - damage > 0:
            self.life = self.life - damage
        else:
            self.life = 0

    def heal(self, heal):
        """
        :param heal: restored health
        """
        if self.life + heal < self.maxLife:
            self.life = self.life + heal
            return True
        else:
            if self.life == self.maxLife:
                return True
            else:
                self.life = self.maxLife
                return False

    @staticmethod
    def speed_update_body(body, gravity, damping, dt):
        max_velocity = 2000
        min_velocity = 3
        # coefficient_of_friction = 1

        if isinstance(body, pymunk.Body) and isinstance(body.velocity, pymunk.Vec2d):
            ll = body.velocity.length
            if ll == 0:
                return

            k = 100 / ll
            v = [-body.velocity[0] * k, -body.velocity[1] * k]
            v += gravity
            pymunk.Body.update_velocity(body, v, damping, dt)

            if ll > max_velocity:
                scale = max_velocity / ll
                body.velocity = body.velocity * scale
            if ll < min_velocity:
                body.velocity = [0, 0]


class Item(Actor):

    def __init__(self, x, y, t, vertices, color):
        super().__init__(t, color)
        self._create_body((x, y), pymunk.Body.STATIC, t, vertices, 1)
        self.shape.sensor = True
        self.shape.collision_type = collision_type[CollisionType.Environment]
