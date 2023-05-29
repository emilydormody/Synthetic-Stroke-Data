
from mesa import Agent
from datetime import time, timedelta


class Specialist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.shift_end = None
        self.shift_start = None

    def set_schedule(self, start, end):
        self.shift_start = time(start)
        self.shift_end = time(end)
        print(self.shift_start, self.shift_end)

    def working_hours(self):
        current = (self.model.date + timedelta(minutes=self.model.current_time)).time()
        if self.shift_start < self.shift_end:
            return self.shift_start <= current <= self.shift_end
        elif self.shift_end < self.shift_start:
            return self.shift_start <= current or current <= self.shift_end
