import pygame

from entities.BusStop import BusStop
from entities.Map import Map
from entities.Shedule import BusSchedule
from entities.bus import Bus
from storeg.fileStoreg import BusStopSerializer


def simulate_pygame(simulation_map, bus_schedules, total_ticks=1000, fps=30):
    """
    Запускает визуальную симуляцию с заданными данными.
    :param simulation_map: Объект карты (Map).
    :param bus_schedules: Список расписаний для каждого автобуса (список списков).
    :param total_ticks: Общее количество тиков симуляции.
    :param fps: Частота кадров для визуализации.
    """
    # Инициализация Pygame
    pygame.init()
    screen_size = 800  # Размер окна
    screen = pygame.display.set_mode((screen_size, 200))
    clock = pygame.time.Clock()
    cell_size = screen_size // simulation_map.size  # Размер одной клетки карты
    current_tick = 0

    # Активные автобусы
    active_buses = []

    # Основной цикл симуляции
    while current_tick < total_ticks or active_buses:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 1. Обновить очереди пассажиров на остановках
        for stop in simulation_map.stops.values():
            stop.update_waiting_queue(current_tick)
            stop.remove_passengers(current_tick)

        # 2. Выпустить автобусы по расписанию
        for i, schedule in enumerate(bus_schedules):
            if (
                current_tick in schedule and len(active_buses) < 8
            ):  # Проверка лимита автобусов
                new_bus = Bus(
                    bus_id=i, capacity=20, route=list(range(simulation_map.size))
                )
                active_buses.append(new_bus)
                print(f"Bus {i+1} departed at tick {current_tick}.")

        # 3. Двигать автобусы и проверять остановки
        buses_to_remove = []
        for bus in active_buses:
            bus.move()

            # Если автобус достигает конца маршрута, он удаляется
            if simulation_map.is_terminal(bus.current_position):
                buses_to_remove.append(bus)
                continue

            # Проверить, находится ли автобус на остановке
            stop = simulation_map.is_bus_at_stop(bus.current_position)
            if stop:
                bus.drop_off_passengers(stop)
                bus.pick_up_passengers(stop)

        # Удалить автобусы, которые завершили маршрут
        for bus in buses_to_remove:
            active_buses.remove(bus)

        # 4. Отрисовка карты и объектов
        screen.fill((255, 255, 255))  # Очистить экран
        draw_map(screen, simulation_map, active_buses, cell_size)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(fps)

        # Следующий тик
        current_tick += 1
    pygame.quit()


# Функция для отрисовки карты и автобусов
def draw_map(screen, simulation_map, buses, cell_size):
    """
    Отрисовывает карту, остановки и автобусы.
    :param screen: Экран pygame.
    :param simulation_map: Объект карты.
    :param buses: Список автобусов.
    :param cell_size: Размер одной клетки.
    """
    # Отрисовка клеток карты
    for i in range(simulation_map.size):
        rect = pygame.Rect(i * cell_size, 50, cell_size, cell_size)
        pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    # Отрисовка остановок
    for position, stop in simulation_map.stops.items():
        x = position * cell_size + cell_size // 2
        pygame.draw.circle(screen, (0, 0, 255), (x, 100), 10)
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(len(stop.waiting_queue)), True, (0, 0, 0))
        screen.blit(text, (x - 10, 120))

    # Отрисовка автобусов
    for bus in buses:
        x = bus.current_position * cell_size + cell_size // 2
        pygame.draw.rect(screen, (255, 0, 0), (x - 15, 70, 30, 20))
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(len(bus.passengers)), True, (0, 0, 0))
        screen.blit(text, (x - 10, 50))


if __name__ == "__main__":
    # Загрузка из файла
    filename = "bus_stops.json"
    bus_stops: list[BusStop] = BusStopSerializer.load_bus_stops_from_file(filename)

    simulation_map = Map(stops=bus_stops, size=50)

    # Расписание для 8 автобусов
    bus_schedules = [
        [102, 12],
        [45, 59],
        [25, 8],
        [99, 109],
        [12, 22, 144],
        [44, 134],
        [112, 21],
        [19, 91],
    ]

    simulate_pygame(simulation_map, bus_schedules, total_ticks=200, fps=10)
