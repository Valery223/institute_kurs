from entities.BusStop import BusStop
from entities.Map import Map


class MapGenerator:
    def __init__(self, num_stops: int, interval: int):
        """
        Генератор карты с остановками.
        :param num_stops: Количество остановок
        :param interval: Интервал между остановками (в тиках)
        """
        self.num_stops = num_stops
        self.interval = interval

    def generate_map(self):
        """
        Генерирует карту с остановками.
        """
        stops = [BusStop(stop_id=i) for i in range(self.num_stops)]
        return Map(stops, self.interval)
