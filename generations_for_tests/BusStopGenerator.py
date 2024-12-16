import random
from entities.BusStop import BusStop
from generations_for_tests.PassengerGenerator import PassengerGenerator


class BusStopGenerator:
    @staticmethod
    def generate_bus_stop(stop_id: int, n: int, total_ticks: int, num_stops: int):
        """
        Генерация остановки с очередью пассажиров на день.
        - stop_id: ID остановки.
        - n: количество пассажиров на день.
        - total_ticks: общее количество тиков в симуляции.
        - num_stops: общее количество остановок.
        """
        if stop_id == num_stops - 1:
            # Если это конечная остановка, здесь пассажиров не должно быть
            return BusStop(stop_id)

        passengers = PassengerGenerator.generate_passengers(n, total_ticks)
        for passenger in passengers:
            # Назначаем конечную остановку, которая выше текущей
            passenger.end_stop = random.randint(stop_id + 1, num_stops - 1)

        passengers.sort(key=lambda p: p.start_tick)  # Сортируем по времени
        bus_stop = BusStop(stop_id)
        bus_stop.daily_queue = passengers
        return bus_stop
