import random

from mesa import Agent
from datetime import time, timedelta


class Specialist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.shift_end = time(16)
        self.shift_start = time(8)
        self.daily_stroke_patients = random.randint(2,8)
        self.current_patient = None

    def set_schedule(self, start, end):
        self.shift_start = time(start)
        self.shift_end = time(end)

    def working_hours(self):
        current = (self.model.start_date + timedelta(minutes=self.model.current_time)).time()
        if self.same_time(current, self.shift_start):
            self.daily_stroke_patients = random.randint(2, 8)
        if self.daily_stroke_patients == 0:
            return False
        if self.shift_start < self.shift_end:
            return self.shift_start <= current <= self.shift_end
        elif self.shift_end < self.shift_start:
            return self.shift_start <= current or current <= self.shift_end

    def same_time(self, one, two):
        return one.strftime('%H:%M') == two.strftime('%H:%M')
