from dataclasses import dataclass
from typing import List

import random
import itertools


@dataclass
class FoodType:
    type: List[str]


class FoodGenerator:
    def __init__(self) -> None:
        # food types with prices
        self.food_types_basic = {
            "room only": 0,
            "board and breakfast": 20,
            "half board": 40,
            "full board": 60,
            "all inclusive": 80,
        }
        self.food_types_extended = []

    # meal options per room
    def gen_food_type(self):
        offert_range = random.randint(1, 5)
        chosen_types = dict(itertools.islice(self.food_types_basic.items(), offert_range))
        return chosen_types
