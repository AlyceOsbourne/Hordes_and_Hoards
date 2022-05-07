# goal oriented action planning for game AI
from enum import Enum, auto

class States(Enum):
    Advance = auto()
    Attack = auto()
    Flee = auto()