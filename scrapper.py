import re
import requests
import csv
import json
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from urllib.request import urlopen
from typing import Type
from datetime import date

from Hotel import Hotel
from RoomGenerator import RoomGenerator
from FoodGenerator import FoodGenerator


@dataclass
class TripData:
    source_city: str
    dest_country: str
    dest_city: str
    dest_hotel: Hotel


class Scrapper:
    def __init__(self, cities_max=200) -> None:
        self.page = None
        self.csv_filename = "scrapper/scrapped_data/destinations.csv"
        self.json_filename = "scrapper/scrapped_data/destinations.json"
        self.trips = []
        self.cities_max = cities_max
        self.cities = []
        self.i = 2
        self.room_gen = RoomGenerator()
        self.food_gen = FoodGenerator()

    def read_page(self, page_counter=2) -> None:
        self.curr_url = "https://www.wakacje.pl/wczasy/?str-" + str(page_counter)
        self.page = requests.get(self.curr_url).content
        self.soup = BeautifulSoup(self.page, "html.parser")

    def print_page(self) -> None:
        if self.page:
            print(self.page)

    def __get_source(self) -> list:
        source = []
        for x in self.page:
            if (
                x["data-testid"] == "offer-listing-transport-plane"
                or x["data-testid"] == "offer-listing-transport-bus"
            ):
                text = x.get_text().replace(" ", "")
                source.append(text.split(","))
        return source

    def __process_source(self, sources):
        result_source = []
        for source in sources:
            for city in source:
                if re.search(r"\((.*?)\)", city):
                    tmp_city = re.sub(r"\((.*?)\)", " ", city)
                    tmp_city = tmp_city.split(" ")
                    source.remove(city)
                    source.append(tmp_city[0])
                    source.append(tmp_city[1])

            result_source.append(source)
        return result_source

    def __get_destination_countries(self) -> list:
        countries = []
        for x in self.page:
            if "offer-listing-geo" in x["data-testid"]:
                countries.append(x.get_text().split(" ")[0])
        return countries

    def __get_destination_cities(self) -> list:
        cities = []
        for x in self.page:
            if "offer-listing-geo" in x["data-testid"]:
                text = x.get_text().replace(" ", "")
                try:
                    city = text.split("/")[2]
                    cities.append(city)
                # there is no region info, just a country and a city
                except IndexError:
                    city = text.split("/")[1]
                    cities.append(city)
        return cities

    def __get_destination_hotels(self) -> list:
        hotels = []
        prev_x = None
        for x in self.page:
            # print(x.get_text())
            if "offer-listing-name" in x["data-testid"] and x.get_text() != prev_x:
                hotels.append(x.get_text())
            prev_x = x.get_text()
        return hotels

    def __parse_html(self) -> None:
        test = self.soup.find_all("span", {"data-testid": True})
        self.page = test
        # source - cities in Poland
        sources = self.__get_source()

        # destination
        countries = self.__get_destination_countries()
        cities = self.__get_destination_cities()
        hotels = self.__get_destination_hotels()
        sources = self.__process_source(sources)

        for city in cities:
            if city not in self.cities:
                self.cities.append(city)

        for i in range(len(sources)):
            for j in range(len(sources[i])):
                # generate rooms and food types for the hotel
                hotel_name = hotels[i]
                hotel_rooms = self.room_gen.gen_rooms_with_dates_for_hotel(hotel_name)
                hotel_board = self.food_gen.gen_food_type()
                hotel = Hotel(hotel_name, hotel_rooms, hotel_board)
                trip = TripData(sources[i][j], countries[i], cities[i], hotel)
                self.trips.append(trip)

    # FROM available cities (from Poland only)
    # TO country, city, hotel
    def dict_to_csv(self) -> None:
        try:
            with open(self.csv_filename, "w") as csv_file:
                fieldnames = TripData.__annotations__.keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for data in self.trips:
                    writer.writerow(asdict(data))
        except IOError:
            print("IO Error")

    def csv_to_dict(self) -> None:
        try:
            with open(self.csv_filename, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.trips.append(row)
        except IOError:
            print("IO Error")

    def dict_to_json(self) -> None:
        dict_trips = [asdict(trip) for trip in self.trips]
        try:
            with open(self.json_filename, "w", encoding="utf-8") as json_file:
                json.dump(dict_trips, json_file, ensure_ascii=False, indent=4)
        except IOError:
            print("IO Error")

    def json_to_dict(self) -> None:
        try:
            with open(self.json_filename, "r", encoding="utf-8") as json_file:
                trips = json.load(json_file)
                self.trips = [TripData(**trip) for trip in trips]
        except IOError:
            print("IO Error")

    def run(self) -> None:
        i = 2
        while len(self.cities) < self.cities_max:
            self.read_page(self.i)
            self.__parse_html()
            self.i += 1

    def print_trips(self) -> None:
        print(self.trips)


scrapper = Scrapper()
scrapper.run()
scrapper.dict_to_csv()
scrapper.dict_to_json()
