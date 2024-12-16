from copy import deepcopy
import random
from typing import List
from tqdm import tqdm

from entities.Map import Map
from simuleted_text import simulate_text

import random
from typing import List

from storeg.fileStoreg import BusStopSerializer
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(
        self,
        simulation_map: Map,
        population_size: int,
        generations: int,
        day_length: int,
        route_length: int,
        num_buses: int,
    ):
        """
        Инициализация параметров генетического алгоритма.
        :param population_size: Размер популяции.
        :param generations: Количество поколений.
        :param day_length: Длина дня в тиках.
        :param route_length: Длина маршрута в тиках.
        :param num_buses: Количество автобусов.
        """
        self.map = simulation_map
        self.population_size = population_size
        self.generations = generations
        self.day_length = day_length
        self.route_length = route_length
        self.num_buses = num_buses
        self.population = []  # Популяция индивидов
        self.best_fitness_values = []  # Для графика

    def initialize_population(self):
        """Генерирует начальную популяцию."""
        population = [
            [[0] * self.day_length for _ in range(self.num_buses)]
            for _ in range(self.population_size)
        ]
        self.population = population

    def translate_gen_to_schedule(self, individual):
        """
        Трансляция гена в формат расписания, понятный симуляции.
        :param individual: Ген индивида (8 строк по 200 ячеек).
        :return: Расписание для симуляции в формате [[30, 120], [45], ...].
        """
        bus_schedules = []
        for bus_schedule in individual:
            schedule = []
            for i, value in enumerate(bus_schedule):
                if value == 1:  # Отправка автобуса
                    schedule.append(i)
            bus_schedules.append(schedule)
        return bus_schedules

    def apply_negative_zone(self, bus_schedule: List[int], position: int):
        """
        Изменяет на  -1 на участке от start до end в расписании автобуса(кроме самой position).
        :param bus_schedule: Расписание автобуса (список значений).
        """

        start = max(0, position - self.route_length)
        end = min(self.day_length, position + self.route_length + 1)

        for i in range(start, position):
            bus_schedule[i] -= 1
        for i in range(position + 1, end):
            bus_schedule[i] -= 1

    def delete_negative_zone(self, bus_schedule: List[int], position: int):
        start = max(0, position - self.route_length)
        end = min(self.day_length, position + self.route_length + 1)

        for i in range(start, position):
            bus_schedule[i] += 1
        for i in range(position + 1, end):
            bus_schedule[i] += 1

    def mutate(self, individual):
        """Вносит мутацию в индивида."""
        for bus_schedule in individual:
            # Мутация появления
            if random.random() < 0.01:  # Вероятность появления
                available_positions = [
                    i for i, value in enumerate(bus_schedule) if value == 0
                ]
                if available_positions:
                    new_position = random.choice(available_positions)
                    bus_schedule[new_position] = 1
                    self.apply_negative_zone(bus_schedule, new_position)

            # Мутация изменения
            if random.random() < 0.1:  # Вероятность изменения
                current_positions = [
                    i for i, value in enumerate(bus_schedule) if value == 1
                ]
                if current_positions:
                    current_position = random.choice(current_positions)
                    direction = random.choice([-1, 1])
                    new_position = current_position + direction
                    new_range = current_position + direction * self.route_length

                    # Проверка что не выходит за границы и что не пересекает с другими выездами
                    if (
                        0 <= new_position < self.day_length
                        and bus_schedule[new_position] == -1
                    ):
                        self.delete_negative_zone(bus_schedule, current_position)
                        bus_schedule[current_position] = 0
                        bus_schedule[new_position] = 1
                        self.apply_negative_zone(bus_schedule, new_position)

            # Мутация удаления
            if random.random() < 0.001:  # Вероятность удаления
                current_positions = [
                    i for i, value in enumerate(bus_schedule) if value == 1
                ]
                if current_positions:
                    position_to_remove = random.choice(current_positions)
                    bus_schedule[position_to_remove] = 0
                    self.delete_negative_zone(bus_schedule, position_to_remove)

    def evaluate_fitness(self, individual):
        """Оценивает приспособленность индивида."""

        shedule = self.translate_gen_to_schedule(individual)

        earnings = simulate_text(deepcopy(self.map), [], shedule, self.day_length)

        return sum(earnings)

    def select_parents(self):
        """Выбирает родителей для скрещивания."""
        selected = []
        for _ in range(2):  # Выбираем двух родителей
            tournament = random.sample(
                self.population, k=5
            )  # Турнир из 5 случайных индивидов
            best_parent = max(
                tournament, key=self.evaluate_fitness
            )  # Лучший по приспособленности
            selected.append(best_parent)
        return selected[0], selected[1]

    def crossover(self, parent1, parent2):
        """Выполняет скрещивание двух родителей."""
        child = [[0] * self.day_length for _ in range(self.num_buses)]
        for bus in range(self.num_buses):
            # Равномерный кроссовер: каждая строка с вероятностью 50% берётся от одного из родителей
            if random.random() < 0.5:
                child[bus] = parent1[bus][:]
            else:
                child[bus] = parent2[bus][:]
        return child

    def run(self):
        """Основной цикл генетического алгоритма."""
        # Инициализация начальной популяции
        self.initialize_population()

        with tqdm(total=self.generations, desc="Генерации", unit="gen") as progress_bar:
            for generation in range(self.generations):
                # Оценка приспособленности
                fitness = [self.evaluate_fitness(ind) for ind in self.population]

                # Логирование лучшего результата
                best_fitness = max(fitness)
                self.best_fitness_values.append(best_fitness)

                # Селекция
                new_population = []
                while len(new_population) < self.population_size:
                    parent1, parent2 = self.select_parents()
                    child = self.crossover(parent1, parent2)
                    self.mutate(child)
                    new_population.append(child)

                self.population = new_population

                # Обновляем прогресс-бар
                progress_bar.update(1)

        # Возвращает лучший результат
        best_fitness = max([self.evaluate_fitness(ind) for ind in self.population])
        self.plot_fitness()
        return self.population[
            [self.evaluate_fitness(ind) for ind in self.population].index(best_fitness)
        ]

    def plot_fitness(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.best_fitness_values, marker="o", linestyle="-", color="b")
        plt.title("Изменение лучшего значения прибыли по итерациям", fontsize=14)
        plt.xlabel("Итерация", fontsize=12)
        plt.ylabel("Лучшее значение прибыли", fontsize=12)
        plt.grid(True)
        plt.show()


# Пример использования
if __name__ == "__main__":
    filename = "primer.json"
    bus_stops = BusStopSerializer.load_bus_stops_from_file(filename)
    simulation_map = Map(stops=bus_stops, size=50)

    ga = GeneticAlgorithm(
        simulation_map,
        population_size=10,
        generations=10,
        day_length=200,
        route_length=50,
        num_buses=8,
    )
    best_schedule = ga.run()
    print("Best Schedule:", ga.translate_gen_to_schedule(best_schedule))
