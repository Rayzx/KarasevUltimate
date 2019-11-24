class Manager:
    _w = None

    @classmethod
    def remove_actor(cls, actor):
        cls._w.remove_actor(actor)

    @classmethod
    def add_actor(cls, actor):
        cls._w.instance().add_actor(actor)

    @classmethod
    def explosion(cls, pos, force):
        pass

    @classmethod
    def shot(cls, pos, direction, force):
        pass

    @classmethod
    def set_world(cls, world):
        cls._w = world