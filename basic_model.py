import random

from mesa import Agent, Model
import mesa.time

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
        self.ct_scanned = False
        self.t_time = 0
        self.treated = False
        self.neuro_time = 0
        self.neuro_visit = False
        self.icu_arrived = False
        self.icu_arrival_time = 0
        self.arrived = False

    def step(self):
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True
            print(self.unique_id, 'arrived at ', self.model.current_time)
        elif self.arrived:
            if not self.ct_scanned:
                if self.admission_time < self.model.current_time - 15:
                    self.model.ct_patients.append(self)
            elif self.ct_scanned and not self.treated: # self.ct_time < self.model.current_time:
                if self.ct_time < self.model.current_time - 15:
                    self.model.t_patients.append(self)
            elif self.treated and not self.icu_arrived:
                if self.t_time < self.model.current_time - 5:
                    self.icu_arrived = True
                    print(self.unique_id, 'icu at ', self.model.current_time)
                    self.icu_arrival_time = self.model.current_time
            elif self.icu_arrived and not self.neuro_visit:
                if self.icu_arrival_time < self.model.current_time - 120:
                    self.model.neuro_patients.append(self)

class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 1
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = []
        self.all_patients = [] # modelled to have only one of each treatment happen at a time
        for i in range(100):
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
            patient.ct_scanned = True
            patient.ct_time = self.current_time
            print(patient.unique_id, 'ct scan at ', self.current_time)

        if len(self.t_patients) != 0:
            patient = self.t_patients.pop(0)
            patient.treated = True
            patient.t_time = self.current_time
            print(patient.unique_id, 'thrombo at ', self.current_time)

        if len(self.neuro_patients) != 0:
            patient = self.neuro_patients.pop(0)
            patient.neuro_visit = True
            patient.neuro_time = self.current_time
            print(patient.unique_id, 'saw neuro at ', self.current_time)


def convert_time(time):
    date = "2023-05-07 "
    if time >= 1440:
        date = "2023-05-08 "
        time -= 1440
    hour = time//60
    minute = time-hour*60
    if minute < 10:
        minute = "0"+str(minute)
    return date+str(hour)+":"+str(minute)

def track_arrivals(model):
    lst = []
    for patient in model.all_patients:
        arrival = convert_time(patient.admission_time)
        lst.append(arrival)
    return lst

def track_icu_arrival(model):
    lst = []
    for patient in model.all_patients:
        arrival = convert_time(patient.icu_arrival_time)
        lst.append(arrival)
    return lst

def track_ctscans(model):
    lst = []
    for patient in model.all_patients:
        scan = convert_time(patient.ct_time)
        lst.append(scan)
    return lst

def track_treatment(model):
    lst = []
    for patient in model.all_patients:
        treatment = convert_time(patient.t_time)
        lst.append(treatment)
    return lst

def track_neurologist(model):
    lst = []
    for patient in model.all_patients:
        visit = convert_time(patient.neuro_time)
        lst.append(visit)
    return lst

def patient_name(model):
    lst = []
    for patient in model.all_patients:
        name = patient.name
        lst.append(name)
    return lst

def patient_age(model):
    lst = []
    for patient in model.all_patients:
        age = patient.age
        lst.append(age)
    return lst

def patient_gender(model):
    lst = []
    for patient in model.all_patients:
        gender = patient.gender
        lst.append(gender)
    return lst


def main():
    h = Hospital()
    for i in range(2880):
        h.step()


if __name__ == "__main__":
    main()

