import random

from entities import Passenger


class Bus:
    def __init__(
        self,
        capacity: int,
        route: list[int],
        bus_id: int,
        boarding_fee: int = 50,
        departure_cost: int = 1000,
    ):
        """
        Инициализация автобуса.
        :param capacity: Общее количество мест в автобусе.
        :param route: Список позиций на карте, составляющих маршрут.
        """
        self.bus_id = bus_id
        self.capacity = capacity  # Общее количество мест
        self.free_seats = capacity  # Свободные места
        self.route = route  # Маршрут автобуса (позиции на карте)
        self.current_position_index = 0  # Индекс текущей позиции в маршруте
        self.passengers = []
        self.earnings = -departure_cost  # Учитываем стоимость запуска автобуса
        self.boarding_fee = boarding_fee

    def move(self):
        """
        Движение автобуса по маршруту.
        """
        self.current_position_index += 1
        if self.current_position_index >= len(self.route):
            self.current_position_index = (
                len(self.route) - 1
            )  # Автобус останавливается в конце маршрута

    @property
    def current_position(self) -> int:
        """
        Возвращает текущую позицию автобуса на карте.
        :return: Индекс текущей позиции.
        """
        return self.route[self.current_position_index]

    def pick_up_passengers(self, bus_stop):
        """
        Забирает пассажиров с остановки, если есть свободные места.
        :param bus_stop: Остановка (BusStop), на которой стоит автобус.
        """
        while self.free_seats > 0 and bus_stop.waiting_queue:
            passenger: Passenger = bus_stop.waiting_queue.pop(0)
            self.passengers.append(passenger)
            self.free_seats -= 1
            # print(f"Пассажир {passenger} сел в автобус")
            self.earnings += self.boarding_fee

    def drop_off_passengers(self, bus_stop, time_tick=-1):
        """
        Высаживает пассажиров, которые достигли своей конечной остановки.
        :param bus_stop: Остановка (BusStop), на которой стоит автобус.
        """
        remaining_passengers = []
        for passenger in self.passengers:
            if passenger.end_stop == bus_stop.stop_id:
                passenger.end_tick = time_tick  # Сохраняем время высадки
                # bus_stop.waiting_queue.append(passenger)  # Пассажир высаживается
                remaining_passengers.append(passenger)

        for to_remove in remaining_passengers:
            self.passengers.remove(to_remove)
            self.free_seats += 1
            # print(f"Пассажир {passenger} высажен на остановке {bus_stop.stop_id}")
