from generations_for_tests.BusStopGenerator import BusStopGenerator
from storeg.fileStoreg import BusStopSerializer


if __name__ == "__main__":
    num_stops = 5
    passengers_per_stop = 50
    total_ticks = 200

    # Генерация остановок
    bus_stops = [
        BusStopGenerator.generate_bus_stop(
            stop_id, passengers_per_stop, total_ticks, num_stops
        )
        for stop_id in range(num_stops)
    ]

    # Сохранение в файл
    filename = "bus_stops.json"
    BusStopSerializer.save_bus_stops_to_file(bus_stops, filename)
    print(f"Остановки сохранены в файл {filename}.")
