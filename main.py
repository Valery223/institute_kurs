from copy import deepcopy
from matplotlib import pyplot as plt
from collections import Counter

from entities.BusStop import BusStop
from entities.Map import Map
from gen_end import GeneticAlgorithm
from generations_for_tests.BusStopGenerator import BusStopGenerator
from grafig_visualizate import simulate_pygame
from optimal_bus_schedule import optimal_bus_schedule
from simuleted_text import simulate_text
from storeg.fileStoreg import BusStopSerializer


def get_positive_int(prompt, min_value=1, max_value=None):
    """Запрашивает у пользователя положительное целое число в заданном диапазоне."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value or (max_value is not None and value > max_value):
                raise ValueError
            return value
        except ValueError:
            if max_value:
                print(f"Ошибка: введите целое число от {min_value} до {max_value}.")
            else:
                print(f"Ошибка: введите целое число больше или равно {min_value}.")


def generate_bus_stops(num_stops, passengers_per_stop, total_ticks):
    """Генерация остановок и сохранение в файл."""
    filename = (
        input("Введите название файла для СОХРАНЕНИЯ остановок (без .json): ") + ".json"
    )

    bus_stops = [
        BusStopGenerator.generate_bus_stop(
            stop_id, passengers_per_stop, total_ticks, num_stops
        )
        for stop_id in range(num_stops)
    ]

    BusStopSerializer.save_bus_stops_to_file(bus_stops, filename)
    print(f"Остановки сохранены в файл {filename}.")


def load_bus_stops():
    """Загрузка остановок из файла."""
    filename = (
        input("Введите название файла для ЗАГРУЗКИ остановок (без .json): ") + ".json"
    )
    bus_stops = BusStopSerializer.load_bus_stops_from_file(filename)
    print(f"Загружено {len(bus_stops)} остановок.")
    return bus_stops


def visualize_passenger_distribution(bus_stops):
    """Построение графика распределения пассажиров по тикам."""
    tick_counts = Counter()

    for stop in bus_stops:
        for passenger in stop.daily_queue:
            tick_counts[passenger.start_tick] += 1

    ticks = sorted(tick_counts.keys())
    counts = [tick_counts[t] for t in ticks]

    plt.figure(figsize=(10, 6))
    plt.plot(ticks, counts, marker="o", label="Количество пассажиров")
    plt.title("Распределение пассажиров по тикам")
    plt.xlabel("Тики")
    plt.ylabel("Количество пассажиров")
    plt.grid(True)
    plt.legend()
    plt.show()


def generate_map(bus_stops, map_size):
    """Создание карты с остановками."""
    return Map(stops=bus_stops, size=map_size)


def main():
    bus_stops = []
    game_map = None
    bus_schedules = []
    total_ticks = 200
    map_size = 50

    while True:
        print("\nВыберите действие:")
        print("1. Генерация остановок")
        print("2. Загрузка остановок")
        print("3. Графическое распределение пассажиров")
        print("4. Создание карты")
        print("5. Показать карту")
        print("6. Графическая визуализация")
        print("7. Текстовая симуляция")
        print("8. Генетический алгоритм для расписания")
        print("9. Прямой алгоритм(простой)")
        print("0. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            total_ticks = get_positive_int(
                "Введите общее количество тиков (100–10000): ", 100, 10000
            )
            num_stops = get_positive_int(
                "Введите количество остановок (2–100): ", 2, 100
            )
            passengers_per_stop = get_positive_int(
                "Введите количество пассажиров на остановку (10–1000): ", 10, 1000
            )
            generate_bus_stops(num_stops, passengers_per_stop, total_ticks)

        elif choice == "2":
            bus_stops = load_bus_stops()

        elif choice == "3":
            if bus_stops:
                visualize_passenger_distribution(bus_stops)
            else:
                print("Ошибка: сначала загрузите или сгенерируйте остановки.")

        elif choice == "4":
            if bus_stops:
                map_size = get_positive_int(
                    f"Введите размер карты ({len(bus_stops)*3} - {total_ticks/4}): ",
                    len(bus_stops) * 3,
                    total_ticks / 4,
                )
                game_map = generate_map(bus_stops, map_size)
                print("Карта успешно создана.")
            else:
                print("Ошибка: сначала загрузите или сгенерируйте остановки.")

        elif choice == "5":
            if game_map:
                print(game_map)
            else:
                print("Ошибка: карта еще не создана.")

        elif choice == "6":
            if game_map:
                simulate_pygame(deepcopy(game_map), bus_schedules, total_ticks, fps=10)
            else:
                print("Ошибка: карта еще не создана.")

        elif choice == "7":
            if game_map:
                print(
                    f"Заработано денег: {simulate_text(deepcopy(game_map), [], bus_schedules, total_ticks)}"
                )
            else:
                print("Ошибка: карта еще не создана.")

        elif choice == "8":
            if game_map:
                population_size = get_positive_int(
                    "Введите размер популяции (желательно 10–100): ", 10, 1000
                )
                generations = get_positive_int(
                    "Введите количество поколений (желательно 1–50): ", 1, 2000
                )
                ga = GeneticAlgorithm(
                    game_map,
                    population_size,
                    generations,
                    total_ticks,
                    map_size,
                    num_buses=8,
                )
                best_schedule = ga.run()
                bus_schedules = ga.translate_gen_to_schedule(best_schedule)
                print("Лучшее расписание:", bus_schedules)
            else:
                print("Ошибка: карта еще не создана.")

        elif choice == "9":
            if game_map:
                bus_schedules = optimal_bus_schedule(game_map, map_size, total_ticks, 8)

        elif choice == "0":
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
