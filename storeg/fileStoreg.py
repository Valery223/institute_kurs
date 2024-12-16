import json

from entities.BusStop import BusStop
from entities.Passenger import Passenger


class BusStopSerializer:
    @staticmethod
    def save_bus_stops_to_file(bus_stops, filename: str):
        """
        Сохранение списка остановок в файл.
        - bus_stops: список объектов BusStop.
        - filename: имя файла для сохранения.
        """
        data = []
        for stop in bus_stops:
            stop_data = {
                "stop_id": stop.stop_id,
                "daily_queue": [
                    {"start_tick": p.start_tick, "end_stop": p.end_stop}
                    for p in stop.daily_queue
                ],
                "waiting_queue": [
                    {"start_tick": p.start_tick, "end_stop": p.end_stop}
                    for p in stop.waiting_queue
                ],
            }
            data.append(stop_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_bus_stops_from_file(filename: str):
        """
        Загрузка списка остановок из файла.
        - filename: имя файла с данными остановок.
        """
        with open(filename, "r") as file:
            data = json.load(file)

        bus_stops = []
        for stop_data in data:
            bus_stop = BusStop(stop_data["stop_id"])
            bus_stop.daily_queue = [
                Passenger(p["start_tick"], p["end_stop"])
                for p in stop_data["daily_queue"]
            ]
            bus_stop.waiting_queue = [
                Passenger(p["start_tick"], p["end_stop"])
                for p in stop_data["waiting_queue"]
            ]
            bus_stops.append(bus_stop)

        return bus_stops
