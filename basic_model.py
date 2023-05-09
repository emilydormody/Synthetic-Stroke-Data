import random

from mesa import Agent, Model
import mesa.time

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
        self.icu_arrival = 0
        self.arrived = False
        self.treatment_count = 0

    def step(self):
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True

class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 0
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patient = [] # modelled to have two of each treatment happen at once
        for i in range(100):
            patient = Patient(i, self)
            self.schedule.add(patient)

    def steps(self):
        self.schedule.step()
        self.current_time += 1
