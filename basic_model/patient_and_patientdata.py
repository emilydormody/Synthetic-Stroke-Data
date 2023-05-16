import random

from mesa import Agent, Model
import mesa.time
import numpy as np


class Patient(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        if self.name % 2 == 0:
            self.gender = "M"
        else:
            self.gender = "F"
        self.age = random.randint(20, 91)
        self.admission_time = random.randint(300, 1740)
        self.time_of_stroke = self.admission_time - random.randint(120, 210) - np.random.normal(60, 15)
        self.ct_time = 0
        self.ct_scanned = False
        self.t_time = 0
        self.tpa_permitted = False
        self.treated = False
        self.icu_arrived = False
        self.icu_arrival_time = 0
        self.delay = random.uniform(0, 3)
        self.arrived = False
        self.last_treatment = -1

        self.neuro_time = 0
        self.neuro_ward = False
        self.occupational_visit = 0
        self.speech_visit = 0
        self.physio_visit = 0
        self.diet_visit = 0
        self.social_worker_visit = 0
        self.neuro_visit = 0
        if random.randint(0, 4) == 0:
            self.need_cardiologist = True
        else:
            self.need_cardiologist = False
        self.cardiologist_visit = 0

    def step(self):
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True
            if self.admission_time - self.time_of_stroke <= 270:
                self.tpa_permitted = True
            print(self.unique_id, ' stroke at ', self.time_of_stroke, ' arrived at ', self.admission_time,
                  ' difference is ', self.admission_time - self.time_of_stroke, ' need cardio ', self.need_cardiologist)
        elif self.arrived:
            if not self.ct_scanned:
                if self.last_treatment < self.model.current_time - self.ct_delay():
                    if self.model.ct_patients.count(self) == 0:
                        self.model.ct_patients.append(self)
            elif self.tpa_permitted and not self.treated:
                if self.ct_scanned:  # self.ct_time < self.model.current_time:
                    if self.last_treatment < self.model.current_time - self.t_delay():
                        if self.model.t_patients.count(self) == 0:
                            self.model.t_patients.append(self)
            elif (self.treated or not self.tpa_permitted) and not self.icu_arrived:
                if self.last_treatment < self.model.current_time - self.icu_delay():
                    self.icu_arrived = True
                    self.icu_arrival_time = self.model.current_time
                    self.last_treatment = self.model.current_time
                    print(self.unique_id, ' icu at ', self.model.current_time)
            elif self.icu_arrived and not self.neuro_ward:
                if self.last_treatment < self.model.current_time - 120:
                    self.neuro_ward = True
                    self.neuro_time = self.model.current_time
                    self.last_treatment = self.model.current_time
                    self.model.neuro_patients.append(self)
                    print(self.unique_id, ' neuro ward at ', self.model.current_time)

    def fully_treated(self):
        return self.neuro_time != 0 and self.occupational_visit != 0 and self.speech_visit != 0 and self.physio_visit != 0 and \
                self.diet_visit != 0 and self.social_worker_visit != 0 and self.neuro_visit != 0 and \
                (self.cardiologist_visit != 0 or not self.need_cardiologist)

    def ct_delay(self):
        delay = 15
        if 0.5 < self.delay < 1:
            delay += int(self.delay * 10)
        return delay

    def t_delay(self):
        delay = 15
        if 1 < self.delay < 2:
            delay += int((self.delay - 1) * 10)
        return delay

    def icu_delay(self):
        delay = 5
        if 2 < self.delay < 3:
            delay += int((self.delay - 2) * 10)
        return delay


class PatientData():
    def __init__(self, hospital):
        self.all_patients = hospital.all_patients

    def convert_time(self,time):
        date = "2023-05-07 "
        if time >= 1440:
            date = "2023-05-08 "
            time -= 1440
        hour = time // 60
        minute = time - hour * 60
        if minute < 10:
            minute = "0" + str(minute)
        return date + str(hour) + ":" + str(minute)
    def patient_info(self):
        dict = {"Patient Id":[], "Age":[], "Gender":[]}
        for patient in self.all_patients:
            dict["Patient Id"].append(patient.name)
            dict["Age"].append(patient.age)
            dict["Gender"].append(patient.gender)
        return dict








