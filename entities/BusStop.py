from entities.Passenger import Passenger


class BusStop:
    def __init__(self, stop_id: int, position: int = -1):
        self.stop_id = stop_id
        self.position = position
        self.daily_queue = []  # Очередь на день (генерируется и сортируется)
        self.waiting_queue: list[Passenger] = []  # Очередь пассажиров, которые уже ждут

    def update_waiting_queue(self, current_tick: int):
        """Переместить пассажиров с текущим тиком из daily_queue в waiting_queue."""
        while self.daily_queue and self.daily_queue[0].start_tick <= current_tick:
            self.waiting_queue.append(self.daily_queue.pop(0))

    def remove_passengers(self, current_tick: int):
        to_remove = []
        for passenger in self.waiting_queue:
            if current_tick - passenger.start_tick >= 20:
                to_remove.append(passenger)

        for passenger in to_remove:
            self.waiting_queue.remove(passenger)

    def __repr__(self):
        return f"BusStop(stop_id={self.stop_id}, position={self.position}, waiting={len(self.waiting_queue)})"
