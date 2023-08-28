from dataclasses import dataclass
from datetime import date

import helper
import random


@dataclass
class Transport:
    source_city: str
    dest_city: str
    date: str
    capacity: int
    type: str

# to be checked
def gen_transport_src_dest(source, dest) -> Transport:
    transport_date = helper.gen_date().isoformat()
    transport_capacity = random.randint(30, 100)
    transport_types = ["own", "bus", "plane"]
    chosen_type = random.choice(transport_types)
    if chosen_type == "bus":
        transport_capacity = random.choice([30, 50])
    elif chosen_type == "plane":
        transport_capacity = random.choice([100, 150, 200])
    return Transport(source, dest, transport_date, transport_capacity, chosen_type)
