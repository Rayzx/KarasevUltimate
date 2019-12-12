import abc


class Pool:
    """
        класс хранит в себе множество объектов для многократного использования
    """

    def __init__(self, new_object, n=10):
        self._free_object = []
        for i in range(n):
            self._free_object.append(new_object())
        self._new_object = new_object

    def obtain(self):
        """
        :return: возращаетт свободныйобъект
        """
        if len(self._free_object) == 0:
            self._free_object.append(self._new_object())
        a = self._free_object.pop()
        return a

    def free(self, obj):
        """
        :param obj: объект, который объявляеся свободным
        """
        if isinstance(obj, Poolable):
            obj.reset()
        self._free_object.append(obj)

    def clear(self):
        self._free_object.clear()

    def get_free(self):
        return len(self._free_object)


class Poolable:
    @abc.abstractmethod
    def reset(self):
        pass
