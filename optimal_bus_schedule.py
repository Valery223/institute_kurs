from entities.BusStop import BusStop
from entities.Map import Map
from simuleted_text import simulate_text
from storeg.fileStoreg import BusStopSerializer
from tqdm import tqdm


def optimal_bus_schedule(game_map, map_size, total_ticks, num_buses=8):
    """
    Генерация расписания для автобусов с максимизацией прибыли.
    """
    # Инициализация расписания
    schedule = [[] for _ in range(num_buses)]

    # Формирование интервалов
    intervals = list(range(0, total_ticks, map_size))
    intervals.append(total_ticks)

    for i in tqdm(range(len(intervals) - 1), desc="Processing intervals"):
        for num_bus in tqdm(range(num_buses), desc="Processing buses", leave=False):
            max_profit = sum(simulate_text(game_map, [], schedule, total_ticks))
            best_time = -1

            # Перебор всех возможных выездов в текущем интервале
            for time in range(intervals[i], intervals[i + 1] + 1):
                # Проверяем допустимость времени для текущего автобуса
                if is_time_valid(schedule[num_bus], time, map_size):
                    schedule[num_bus].append(time)
                    current_profit = sum(
                        simulate_text(game_map, [], schedule, total_ticks)
                    )
                    if current_profit > max_profit:
                        max_profit = current_profit
                        best_time = time
                    schedule[num_bus].pop()  # Откатываем изменение

            # Добавляем лучшее найденное время в расписание
            if best_time != -1:
                schedule[num_bus].append(best_time)

    return schedule


def is_time_valid(bus_schedule, time, map_size):
    """
    Проверяет, можно ли добавить выезд в заданное время для автобуса.
    """
    return not bus_schedule or time - bus_schedule[-1] >= map_size


if __name__ == "__main__":
    filename = "bus_stops.json"
    bus_stops: list[BusStop] = BusStopSerializer.load_bus_stops_from_file(filename)

    simulation_map = Map(stops=bus_stops, size=50)
    print(optimal_bus_schedule(simulation_map, 50, 200, 8))
