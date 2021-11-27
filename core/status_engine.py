from enum import Enum


class StatusEnum(Enum):

    def __new__(cls, *args):
        index = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._index = index
        return obj

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self._index >= other._index
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self._index > other._index
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self._index <= other._index
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._index < other._index
        return NotImplemented

    @classmethod
    def get_as_list(cls):
        return [(state.name, state.value) for state in cls]

    @classmethod
    def get_state_names_greater_than_or_equal_to(cls, border_state):
        return [state.name for state in cls if state >= border_state]
