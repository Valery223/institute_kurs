from copy import deepcopy
from entities.BusStop import BusStop
from entities.Map import Map
from entities.Shedule import BusSchedule
from entities.bus import Bus
from storeg.fileStoreg import BusStopSerializer


def simulate_text(simulation_map, buses, bus_schedules, total_ticks):

    simulation_map = deepcopy(simulation_map)
    """
    Запускает текстовую симуляцию.
    :param simulation_map: Карта (Map).
    :param buses: Список автобусов (Bus).
    :param bus_schedules: Список расписаний для каждого автобуса (список списков времени отправления).
    :param total_ticks: Общее количество тиков.
    :return: Массив заработков для каждого автобуса.
    """
    current_tick = 0
    total_earnings = [0] * len(bus_schedules)  # Массив заработков для каждого автобуса

    while current_tick < total_ticks or buses:
        # Обновить очереди пассажиров на остановках
        for stop in simulation_map.stops.values():
            stop.update_waiting_queue(current_tick)
            stop.remove_passengers(current_tick)

        # Выпуск автобусов по их индивидуальным расписаниям
        for i, schedule in enumerate(bus_schedules):
            if current_tick in schedule and len(buses) < len(bus_schedules):
                new_bus = Bus(
                    capacity=20, route=list(range(simulation_map.size)), bus_id=i
                )
                buses.append(new_bus)

        # Движение автобусов
        buses_to_remove: list[Bus] = []
        for bus in buses:
            bus.move()

            # Проверить, достиг ли автобус конца маршрута
            if simulation_map.is_terminal(bus.current_position):
                buses_to_remove.append(bus)
                continue

            # Проверить, находится ли автобус на остановке
            stop = simulation_map.is_bus_at_stop(bus.current_position)
            if stop:
                bus.drop_off_passengers(stop)
                bus.pick_up_passengers(stop)

        # Удалить автобусы, завершившие маршрут
        for bus in buses_to_remove:
            # print(f"Bus {bus.bus_id} earnings: {bus.earnings}")
            total_earnings[bus.bus_id] += bus.earnings
            buses.remove(bus)

        # Следующий тик
        current_tick += 1

    # print(f"=== Total Earnings by Bus: {total_earnings} ===")
    return total_earnings


if __name__ == "__main__":
    # Загрузка из файла
    filename = "bus_stops.json"
    bus_stops: list[BusStop] = BusStopSerializer.load_bus_stops_from_file(filename)

    simulation_map = Map(stops=bus_stops, size=50)

    # Расписания для каждого автобуса
    bus_schedules = [[50, 100], [65, 121], [], [], [], [], [], []]

    earnings = simulate_text(simulation_map, [], bus_schedules, total_ticks=200)
    print(f"Final Earnings: {earnings}")
    print(f"sum = {sum(earnings)}")
