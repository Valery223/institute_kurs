import random

from entities.Passenger import Passenger


class PassengerGenerator:
    @staticmethod
    def generate_passengers(n, total_ticks=200):
        """
        Генерация пассажиров с пиковыми интервалами.
        :param n: общее количество пассажиров
        :param total_ticks: общее количество тиков
        :return: список пассажиров
        """
        passengers = []

        # Динамическое определение пиковых и низких интервалов на основе total_ticks
        peak_start_1 = int(total_ticks * 0.3)
        peak_end_1 = int(total_ticks * 0.4)
        peak_start_2 = int(total_ticks * 0.6)
        peak_end_2 = int(total_ticks * 0.7)

        peak_intervals = [(peak_start_1, peak_end_1), (peak_start_2, peak_end_2)]
        low_intervals = [
            (0, peak_start_1 - 1),
            (peak_end_1 + 1, peak_start_2 - 1),
            (peak_end_2 + 1, total_ticks - 1),
        ]

        for _ in range(n):
            # Определяем, в какой интервал генерировать пассажира
            interval_type = random.choices(["peak", "low"], weights=[0.6, 0.4])[0]
            if interval_type == "peak":
                interval = random.choice(peak_intervals)
            else:
                interval = random.choice(low_intervals)

            # Генерация случайного тика в выбранном интервале
            start_tick = random.randint(interval[0], interval[1])
            passengers.append(Passenger(start_tick))

        return passengers
