class Passenger:
    def __init__(self, start_tick: int, end_stop: int = -1):
        self.start_tick = start_tick
        self.end_tick = None
        self.end_stop = end_stop

    def __repr__(self):
        return f"Passenger(start_tick={self.start_tick}, end_stop={self.end_stop})"
