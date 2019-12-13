class AbstractEffect:
    _instance = None

    @classmethod
    def instance(cls):
        pass


class AbstractPositive(AbstractEffect):
    pass


class AbstractNegative(AbstractEffect):
    pass
