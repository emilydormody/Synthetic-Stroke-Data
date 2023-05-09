import random

from mesa import Agent, Model
import mesa.time
from matplotlib import pyplot as plt

class Patient(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        if self.name % 2 == 0:
            self.gender = "M"
        else:
            self.gender = "F"
        self.age = random.randint(20, 91)
        self.admission_time = random.randint(1,1440)
        self.ct_time = 0
        self.t_time = 0
        self.neuro_time = 0
        self.icu_arrived = False
        self.icu_arrival_time = 0
        self.arrived = False

    def step(self):
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True
            print(self.unique_id, 'arrived at ', self.model.current_time)
        elif self.arrived:
            if self.ct_time == 0:
                self.model.ct_patients.append(self)
            elif self.t_time == 0:
                if self.ct_time > self.model.current_time - 2:
                    self.model.t_patients.append(self)
            elif not self.icu_arrived and self.t_time != self.model.current_time:
                self.icu_arrived = True
                print(self.unique_id, 'icu at ', self.model.current_time)
                self.icu_arrival_time = self.model.current_time
            elif self.neuro_time == 0 and self.icu_arrival_time > self.model.current_time - 24:
                self.model.neuro_patients.append(self)

class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 1
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = []
        self.all_patients = [] # modelled to have only one of each treatment happen at a time
        for i in range(20):
            patient = Patient(i, self)
            self.schedule.add(patient)
            self.all_patients.append(patient)

    def step(self):
        self.treat_patients()
        self.schedule.step()
        self.current_time += 1

    def treat_patients(self):
        if len(self.ct_patients) != 0:
            patient = self.ct_patients.pop(0)
            patient.ct_time = self.current_time
            print(patient.unique_id, 'ct scan at ', self.current_time)

        if len(self.t_patients) != 0:
            patient = self.t_patients.pop(0)
            patient.t_time = self.current_time
            print(patient.unique_id, 'thrombo at ', self.current_time)

        if len(self.neuro_patients) != 0:
            patient = self.neuro_patients.pop(0)
            patient.neuro_time = self.current_time
            print(patient.unique_id, 'saw neuro at ', self.current_time)


def graph_arrivals(model):
    lst = []
    for patient in model.all_patients:
        arrival = patient.admission_time
        lst.append(arrival//60)
    print(lst)
    plt.hist(lst)
    plt.show()


h = Hospital()
for i in range(2880):
    h.step()
graph_arrivals(h)