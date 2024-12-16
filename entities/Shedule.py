class BusSchedule:
    def __init__(self, departure_times: list[int]):
        """
        Инициализация расписания автобусов.
        :param departure_times: Список тиков, на которых автобусы выходят.
        """
        self.departure_times = sorted(departure_times)

    def get_departures(self, current_tick: int) -> int:
        """
        Возвращает количество автобусов, которые должны выйти на текущем тике.
        :param current_tick: Текущий тик симуляции.
        :return: Количество автобусов, выходящих на текущем тике.
        """
        return self.departure_times.count(current_tick)
