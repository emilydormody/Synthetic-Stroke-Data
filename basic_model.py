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
        self.ct_time = 0
        self.t_time = 0
        self.neuro_time = 0
        self.icu_arrival = 0
        self.arrived = False

    def step(self):
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True
        elif self.arrived:
            if self.ct_time == 0:
                self.ct_patients



class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 0
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = [] # modelled to have only one of each treatment happen at a time
        for i in range(100):
            patient = Patient(i, self)
            self.schedule.add(patient)

    def step(self):
        self.treat_patients()
        self.schedule.step()
        self.current_time += 1

    def treat_patients(self):
        if len(self.ct_patients) != 0:
            patient = self.ct_patients.pop(0)
            patient.ct_time = self.current_time

        if len(self.t_patients) != 0:
            patient = self.t_patients.pop(0)
            patient.t_time = self.current_time

        if len(self.neuro_patients) != 0:
            patient = self.neuro_patients.pop(0)
            patient.neuro_time = self.current_time

