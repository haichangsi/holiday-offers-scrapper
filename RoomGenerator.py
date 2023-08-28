from dataclasses import dataclass
import random
from datetime import date, timedelta

import helper


@dataclass
class Room:
    name: str
    capacity: int
    available: list


class RoomGenerator:
    def __init__(self) -> None:
        self._current_hotel = None
        # enum maybe?
        self.possible_room_names = {
            "small": 1,
            "medium": 2,
            "large": 4,
            "apartment": 6,
            "studio": 3,
        }

    @property
    def current_hotel(self):
        return self._current_hotel

    @current_hotel.setter
    def current_hotel(self, hotel):
        if hotel is not None and hotel is str:
            self._current_hotel = hotel
        else:
            self._current_hotel = None

    # def date_range(self, start, end):
    #     for n in range(int((end - start).days)+1):
    #         yield start + timedelta(n)

    # available dates per room
    def gen_av_dates_per_room(self, start, end):
        free_seq_num = random.randint(1, 5)
        # have many consequent free days, maybe only 7-10?
        free_seq_len = random.randint(1, 10)
        while free_seq_num * free_seq_len > (end - start).days:
            free_seq_num -= 1
        all_dates = list(helper.date_range(start, end))

        for _ in range(free_seq_num):
            free_seq_start = random.choice(all_dates)
            free_seq_end = free_seq_start + timedelta(free_seq_len)
            for date in helper.date_range(free_seq_start, free_seq_end):
                if date in all_dates:
                    all_dates.remove(date)

        all_dates = self.group_consecutive_dates(sorted(all_dates))
        conv_dates = self.convert_dates(all_dates)

        return conv_dates

    def group_consecutive_dates(self, dates_list):
        continuous_date_sequences = []
        current_sequence = [dates_list[0]]

        for i in range(1, len(dates_list)):
            if dates_list[i] == current_sequence[-1] + timedelta(days=1):
                current_sequence.append(dates_list[i])
            else:
                continuous_date_sequences.append(
                    (current_sequence[0], current_sequence[-1])
                )
                current_sequence = [dates_list[i]]

        continuous_date_sequences.append((current_sequence[0], current_sequence[-1]))
        return continuous_date_sequences

    def convert_dates(self, dates):
        conv_dates = []
        for date in dates:
            conv_dates.append((date[0].isoformat(), date[1].isoformat()))
        return conv_dates

    # maybe just pass the chosen hotel here?
    def gen_rooms_with_dates_for_hotel(self, hotel):
        rooms = []
        rooms_num = random.randint(5, 20)
        for _ in range(rooms_num):
            room_type = random.choice(list(self.possible_room_names.keys()))
            room_size = self.possible_room_names[room_type]
            av_dates = self.gen_av_dates_per_room(
                helper.gen_period_start, helper.gen_period_end
            )
            room = Room(room_type, room_size, av_dates)
            rooms.append(room)
        return rooms
