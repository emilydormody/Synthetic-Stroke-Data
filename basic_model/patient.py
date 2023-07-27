import math
import random

import pandas as pd
from mesa import Agent, Model
import numpy as np
from scipy import stats
from values import *

# lst codes
OCU = 0
SLP = 1
PT = 2
DT = 3
SW = 4
NR = 5
CD = 6



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

        self.hospital_arrival = random.randint(300, NUM_TICKS // 4) + random.random()
        if random.random() >= 0.75:
            self.admission_time = self.hospital_arrival
        else:
            self.admission_time = self.hospital_arrival + self.admission_time_normal()
        self.time_of_stroke = self.hospital_arrival - random.randint(120, 150) - np.random.normal(90, 15)
        if self.admission_time != self.hospital_arrival:
            if random.random() <= 0.62:
                self.transport = "ambulance"
                self.time_of_stroke += 30
            else:
                self.transport = "walkin"
        else:
            self.transport = None
        self.discharge = None

        self.ct_time = self.hospital_arrival + self.ct_time_normal()
        self.ct_treated = False
        self.t_time = self.hospital_arrival + self.tpa_time_normal()
        self.tpa_treated = False
        self.tpa_permitted = False
        if random.random() >= 0.9:
            self.tpa_denied = True
        else:
            self.tpa_denied = False

        if random.random() <= 0.45:
            self.need_icu = True
            self.icu_arrival_time = self.admission_time + self.icu_time_normal()
            self.icu_outtime = self.icu_arrival_time + self.icu_outtime_normal()
        else:
            self.need_icu = False
            self.icu_arrival_time = 0
            self.icu_outtime = 0

        self.ed_arrived = False
        self.arrived = False
        self.icu_arrived = False
        self.last_treatment = -1
        self.in_treatment = False
        self.in_icu = False
        self.neuro_ward_arrived = False

        # self.neuro_times_lst = [self.admission_time + self.occupational_time_normal(),
        #                         self.admission_time + self.speech_time_normal(),
        #                         self.admission_time + self.physio_time_normal(),
        #                         0,
        #                         self.admission_time + self.social_worker_normal(),
        #                         0,
        #                         self.admission_time + self.cardiology_time_normal()]
        self.neuro_time = self.neuro_time_normal()
        self.neuro_outtime = self.neuro_time + self.neuro_outtime_normal()
        self.specialist_count = 0
        if random.random() <= 0.52:
            self.occupational_visit = self.admission_time + self.occupational_time_normal()
        else:
            self.occupational_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.ocu_visited = False
        if random.random() <= 0.331:
            self.speech_visit = self.admission_time + self.speech_time_normal()
        else:
            self.speech_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.speech_visited = False
        if random.random() <= 0.742:
            self.physio_visit = self.admission_time + self.physio_time_normal()
        else:
            self.physio_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.physio_visited = False
        if random.random() <= 0.179:
            self.diet_visit = self.admission_time + self.dietitian_time_normal()
        else:
            self.diet_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.diet_visited = False
        if random.random() <= 0.203:
            self.social_worker_visit = self.admission_time + self.social_worker_normal()
        else:
            self.social_worker_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.sw_visited = False
        if random.random() <= 0.023:
            self.neuro_visit = self.admission_time + self.neurologist_time_normal()
        else:
            self.neuro_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.neuro_visited = False
        if random.random() <= 0.022:
            self.need_cardiologist = True
            self.cardiologist_visit = self.admission_time + self.cardiology_time_normal()
        else:
            self.need_cardiologist = False
            self.cardiologist_visit = NUM_TICKS + 1
            self.specialist_count += 1
        self.cardio_visited = False
        self.bloodwork = 0
        self.last_checkin = 0
        # if self.unique_id == NUM_PATIENTS-1:
        #     pd.DataFrame(data=self.model.before_ticks()).to_csv('~/Documents/NSERC/files/before.csv')
        # print(self.unique_id, 'ed', self.hospital_arrival, 'admit', self.admission_time, 'ct', self.ct_time, 'tpa',
        # self.t_time, 'icu', self.icu_arrival_time, 'out', self.icu_outtime, 'neuro', self.neuro_time)
        # print(self.unique_id)

    def step(self):
        if not self.in_treatment:
            if self.model.current_time >= self.hospital_arrival and not (
                    self.ed_arrived or self.hospital_arrival == self.admission_time):
                self.ed_arrived = True
                self.model.ed_patients.append(self)
            elif self.model.current_time >= self.admission_time and not self.arrived:
                self.arrived = True
                if self in self.model.ed_patients:
                    self.model.ed_patients.remove(self)
                if self.model.current_time - 1 > self.admission_time:
                    self.admission_time = self.model.current_time
            elif not self.ct_treated:
                if self.model.current_time >= self.ct_time - 1:
                    if self.model.ct_patients.count(self) == 0:
                        self.model.ct_patients.append(self)
            elif self.check_permitted() and not self.tpa_treated and self.ct_treated:
                if self.model.current_time >= self.t_time - 1:
                    if self.model.t_patients.count(self) == 0:
                        self.model.t_patients.append(self)
            elif self.arrived:
                if (self.tpa_treated or not self.tpa_permitted) and not self.icu_arrived and self.need_icu and \
                        self.model.current_time >= self.icu_arrival_time:
                    if self.model.current_time - 1 > self.icu_arrival_time:
                        # print('icu', self.icu_arrival_time, 'current', self.model.current_time, self.unique_id)
                        self.icu_arrival_time = self.model.current_time
                    self.icu_arrived = True
                    self.in_icu = True
                elif self.model.current_time >= self.icu_outtime and self.in_icu:
                    self.in_icu = False
                    if self.icu_outtime == self.neuro_time:
                        self.neuro_ward_admission()
                    if self.model.current_time - 1 > self.icu_outtime:
                        self.icu_outtime = self.model.current_time
                elif ((self.icu_arrived and not self.in_icu) or not self.need_icu) and not self.neuro_ward_arrived and \
                        self.model.current_time >= self.neuro_time:
                    self.neuro_ward_admission()
                elif self.model.current_time >= self.neuro_outtime and self.specialist_count == 7:
                    self.discharge = self.model.current_time
                    self.model.schedule.remove(self)
                else:
                    if self.model.current_time >= self.occupational_visit - 1 and not self.ocu_visited:
                        if self.model.ocu_patients.count(self) == 0:
                            self.model.ocu_patients.append(self)
                    if self.model.current_time >= self.physio_visit - 1 and not self.physio_visited:
                        if self.model.physio_patients.count(self) == 0:
                            self.model.physio_patients.append(self)
                    if self.model.current_time >= self.speech_visit - 1 and not self.speech_visited:
                        if self.model.speech_patients.count(self) == 0:
                            self.model.speech_patients.append(self)
                    if self.model.current_time >= self.diet_visit - 1 and not self.diet_visited:
                        if self.model.dietitian_patients.count(self) == 0:
                            self.model.dietitian_patients.append(self)
                    if self.model.current_time >= self.social_worker_visit - 1 and not self.sw_visited:
                        if self.model.social_work_patients.count(self) == 0:
                            self.model.social_work_patients.append(self)
                    if self.model.current_time >= self.cardiologist_visit - 1 and not self.cardio_visited and self.need_cardiologist:
                        if self.model.cardio_patients.count(self) == 0:
                            self.model.cardio_patients.append(self)
                    if self.model.current_time >= self.neuro_visit - 1 and not self.neuro_visited:
                        if self.model.neurologist_patients.count(self) == 0:
                            self.model.neurologist_patients.append(self)

    def check_permitted(self):
        if self.tpa_denied:
            return False
        else:
            if self.model.current_time - self.time_of_stroke <= 270:
                self.tpa_permitted = True
            else:
                self.tpa_permitted = False
            return self.tpa_permitted

    def neuro_ward_admission(self):
        if self.model.current_time - 1 > self.neuro_time:
            self.neuro_time = self.model.current_time
        self.neuro_ward_arrived = True
        self.last_treatment = self.model.current_time
        self.model.neuro_patients.append(self)

    def get_patient_info(self):
        dict = {"Blood Glucose": 0, "Temperature": 0, "Heart Rate": 0, "Respiratory Rate": 0, "Blood Pressure": 0,
                "Pulse Oximetry": 0, "Swallowing Ability": 0, "Swallowing Screen Result": None, "Diet Type": None,
                "Texture of Food": None, "Home/Family Situation": 0, "Mental State": 0, "Emotional State": 0,
                "Action Plan": 0, "Environment": 0, "Bath/Shower Ability": 0, "Dressing": 0, "Grooming": 0,
                "Toileting": 0, "Eating": 0, "Bed Mobility": 0, "Walking": 0, "Wheelchair Mobility": 0, "Cognition": 0,
                "Perception": 0, "Range of Motion": 0, "Balance": 0, "Sensation": 0, "Proprioception": 0, "Strength": 0,
                "Manual Dexterity": 0, "Coordination": 0, "Ashworth Scale Result": 0, "Accomodation": 0,
                "Hand Dominance": 0, "Pain": 0, "Communication": 0, "Vision": 0, "Hearing": 0,
                "Bowel/Bladder Functioning": 0, "Cardiopulmonary Functioning": 0, "Respiratory Functioning": 0,
                "Muscle Tone": 0, "Reflexes/Coordination": 0, "Speech Intelligibility": 0,
                "Oral Peripheral Exam Result": 0}
        return dict

    def admission_time_normal(self):
        if random.random() < 0.956:
            return stats.skewnorm.rvs(4, 146.3, 269.8)
        else:
            return stats.gamma.rvs(1.21, 1002.4, 320.2)

    def neuro_time_normal(self):
        n = random.random()
        if self.icu_outtime == 0:
            time = self.admission_time
            if n < 0.1:
                time += abs(stats.skewnorm.rvs(2.81, 0.762, 0.703))
            elif 0.1 <= n < 0.556:
                time += abs(stats.skewnorm.rvs(2.3, 45.1, 49.4))
            elif 0.556 <= n < 0.931:
                time += abs(stats.gamma.rvs(1.72, 1002.2, 1821.30))
            else:
                time += abs(stats.gamma.rvs(0.749, 10089.2, 8856.7))
        else:
            time = self.icu_outtime
            if n < 0.0388:
                time += self.icu_outtime + stats.gamma.rvs(0.832, 1.42, 2309.4)
        return time

    def icu_time_normal(self):
        n = random.random()
        if n < 0.157:
            return stats.gamma.rvs(3.23, 0.237, 0.343)
        elif 0.157 <= n < 0.615:
            return stats.skewnorm.rvs(2.84, 35.6, 59.7)
        else:
            return stats.gamma.rvs(0.547, 201, 15138.3)

    def ct_time_normal(self):
        return stats.norm.rvs(15, 5)

    def tpa_time_normal(self):
        return stats.norm.rvs(45, 5)

    def neuro_outtime_normal(self):
        if random.random() < 0.941:
            return stats.gamma.rvs(2.16, -410.2, 2262.7)
        else:
            return stats.gamma.rvs(1.026, 15065.1, 6889.8)

    def icu_outtime_normal(self):
        n = random.random()
        if n < 0.285:
            return stats.skewnorm.rvs(-2.82, 2085, 805.6)
        elif 0.285 <= n < 0.923:
            return stats.gamma.rvs(0.891, 2404.5, 5009.6)
        else:
            return stats.gamma.rvs(1.05, 20001, 11464)

    def physio_time_normal(self):
        n = random.random()
        if n < 0.027 and not self.hospital_arrival == self.admission_time:  # <0 minutes (happens in ed)
            return stats.gamma.rvs(2.15, 42.2, 82.7)
        if n < 0.277:  # 0 to 300 mins
            return stats.gamma.rvs(5.91, -45.7, 28)
        elif 0.277 <= n < 0.931:  # 300 to 30000 mins
            return stats.gamma.rvs(0.973, 300.3, 5128.5)
        else:  # 30000 to 80000 mins
            return stats.gamma.rvs(0.896, 30021.7, 12822.1)

    def dietitian_time_normal(self):
        if random.random() <= 0.026:  # 50000 to 1750000 mins
            return stats.gamma.rvs(0.91, 50820.9, 28701.1)
        else:  # 0 to 50000 mins
            return stats.gamma.rvs(0.865, 0.15, 11974.5)

    def speech_time_normal(self):
        n = random.random()
        if n < 0.2:  # 0 to 250 mins
            return stats.skewnorm.rvs(2.45, 44.7, 87)
        elif 0.2 <= n < 0.864:  # 250 to 20000 mins
            return stats.gamma.rvs(0.847, 250.3, 5876.3)
        else:  # 20000 to 90000 mins
            return stats.gamma.rvs(0.915, 20011.6, 18547.4)

    def social_worker_normal(self):
        if random.random() < 0.071:  # 20000 to 60000 mins
            return stats.gamma.rvs(0.988, 20165.5, 9808.2)
        else:  # 0 to 20000 mins
            return stats.gamma.rvs(0.812, 0.117, 4461.4)

    def occupational_time_normal(self):
        n = random.random()
        if n < 0.251:  # 0 to 200
            return stats.skewnorm.rvs(-0.664, 120.3, 51)
        elif 0.251 <= n < 0.896:  # 200 to 20000
            return stats.gamma.rvs(0.918, 200.4, 4280.7)
        else:  # 20000 to 100000
            return stats.gamma.rvs(0.872, 20001.8, 16391.2)

    def cardiology_time_normal(self):
        return stats.gamma.rvs(0.772, 22.6, 113337.4)

    def neurologist_time_normal(self):
        return stats.gamma.rvs(0.566, 5.92, 14428.2)



