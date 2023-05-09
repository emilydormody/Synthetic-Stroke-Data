import random

from mesa import Agent, Model

class Patient(Agent):
    def __init__(self, unique_id, model):
        super().__init__(self, unique_id, model)
        self.name = unique_id
        if self.name % 2 == 0:
            self.gender = "M"
        else:
            self.gender = "F"
        self.age = random.randint(20, 91)
        self.admission_time = random.randint(1440)+1
        self.arrived = False
        self.treatment_count = 0

    def step(self):
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True



