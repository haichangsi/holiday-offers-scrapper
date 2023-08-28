from dataclasses import dataclass
from RoomGenerator import Room
from FoodGenerator import FoodType

from typing import List


@dataclass
class Hotel:
    name: str
    rooms: List[Room]
    food_types: List[str]
