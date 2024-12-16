from entities.BusStop import BusStop


class Map:
    def __init__(self, stops: list[BusStop], size: int):
        """
        Инициализация карты.
        :param stops: список остановок (BusStop).
        :param size: размер карты (количество клеток на прямой).
        """
        self.size = size  # Общее количество клеток на карте
        self.grid = [None] * size  # Пустая карта (список из клеток)
        self.stops = {}  # Словарь для хранения остановок с их позициями

        # Автоматическое размещение остановок на карте
        interval = size // (len(stops) + 1)  # Интервалы между остановками
        for i, stop in enumerate(stops):
            position = (i + 1) * interval
            self.grid[position] = stop
            self.stops[position] = stop
            stop.position = position  # Установка позиции для остановки

    def is_bus_at_stop(self, bus_position: int):
        """
        Проверка, находится ли автобус на остановке.
        :param bus_position: текущая позиция автобуса на карте.
        :return: BusStop объект, если позиция является остановкой, иначе None.
        """
        return self.stops.get(bus_position, None)

    def is_terminal(self, bus_position: int):
        """
        Проверка, находится ли автобус на конечной позиции (начало или конец карты).
        :param bus_position: текущая позиция автобуса на карте.
        :return: True, если позиция является конечной, иначе False.
        """
        return bus_position == 0 or bus_position == self.size - 1

    def __repr__(self):
        """
        Текстовое представление карты для визуализации.
        """
        map_str = ""
        for i in range(self.size):
            if i in self.stops:
                map_str += f"[S{self.stops[i].stop_id}]"  # Отображение остановки
            else:
                map_str += "[ ]"  # Пустая клетка
        return map_str

    def add_bus(self, bus_id, start_position=0):
        """
        Добавляет автобус на карту.
        """
        self.bus_positions[bus_id] = start_position

    def move_bus(self, bus_id):
        """
        Продвигает автобус на 1 тик вперед по карте.
        """
        if bus_id in self.bus_positions:
            self.bus_positions[bus_id] += 1

    def get_buses_at_stops(self):
        """
        Проверяет, какие автобусы находятся на остановках.
        Возвращает словарь {stop_id: [bus_id, ...]}.
        """
        buses_at_stops = {stop.stop_id: [] for stop in self.stops}
        for bus_id, position in self.bus_positions.items():
            for stop in self.stops:
                if (
                    position == stop.stop_id * self.interval
                ):  # Используем interval вместо фиксированного значения
                    buses_at_stops[stop.stop_id].append(bus_id)
        return buses_at_stops

    # def __str__(self):
    #     map_info = "\n".join([str(stop) for stop in self.stops])
    #     return f"Map with stops:\n{map_info}\nBus positions: {self.bus_positions}"
