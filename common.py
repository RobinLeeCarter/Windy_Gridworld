import enum
from collections import namedtuple

XY = namedtuple('XY', ['x', 'y'])


class UserEvent(enum.IntEnum):
    NONE = 0
    QUIT = 1
    SPACE = 2
