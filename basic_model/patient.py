import random

from mesa import Agent
import numpy as np
from scipy import stats
from values import *


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
        self.treatment_counts = {'ct': True, 'tpa': True, 'icu': True, 'neuro_ward': True, 'physio': True, 'sw': True,
                                 'slp': True, 'cardio': True, 'ocu': True, 'neuro': True, 'dt': True}
        if self.admission_time != self.hospital_arrival:
            if random.random() <= 0.62:
                self.transport = "ambulance"
                self.time_of_stroke += 30
            else:
                self.transport = "walkin"
        else:
            self.transport = None
        self.discharge = NUM_TICKS + 1

        if random.random() <= 0.167:
            self.ct_time = self.hospital_arrival + self.ct_time_normal()
        else:
            self.ct_time = NUM_TICKS + 1
            self.treatment_counts['ct'] = False
        self.ct_treated = False
        self.tpa_treated = False
        self.tpa_permitted = True
        if random.random() >= 0.04:
            self.t_time = NUM_TICKS + 1
            self.treatment_counts['tpa'] = False
            self.tpa_permitted = False
        else:
            self.t_time = self.hospital_arrival + self.tpa_time_normal()

        if random.random() <= 0.45:
            self.need_icu = True
            self.icu_arrival_time = self.admission_time + self.icu_time_normal()
            self.icu_outtime = self.icu_arrival_time + self.icu_outtime_normal()
        else:
            self.need_icu = False
            self.icu_arrival_time = 0
            self.icu_outtime = 0
            self.treatment_counts['icu'] = False

        self.ed_arrived = False
        self.arrived = False
        self.icu_arrived = False
        self.last_treatment = -1
        self.in_treatment = False
        self.in_icu = False
        self.neuro_ward_arrived = False

        if self.icu_outtime == 0:
            if random.random() <= 0.506:
                self.neuro_time = self.neuro_time_normal()
                self.neuro_outtime = self.neuro_time + self.neuro_outtime_normal()
            else:
                self.neuro_time = NUM_TICKS + 1
                self.neuro_outtime = NUM_TICKS + 1
                self.treatment_counts['neuro_ward'] = False
        else:
            if random.random() <= 0.36:
                self.neuro_time = self.neuro_time_normal()
                self.neuro_outtime = self.neuro_time + self.neuro_outtime_normal()
            else:
                self.neuro_time = NUM_TICKS + 1
                self.neuro_outtime = NUM_TICKS + 1
                self.treatment_counts['neuro_ward'] = False

        if random.random() <= 0.52:
            self.occupational_visit = self.admission_time + self.occupational_time_normal()
        else:
            self.occupational_visit = NUM_TICKS + 1
            self.treatment_counts['ocu'] = False
        self.ocu_visited = False
        if random.random() <= 0.331:
            self.speech_visit = self.admission_time + self.speech_time_normal()
        else:
            self.speech_visit = NUM_TICKS + 1
            self.treatment_counts['slp'] = False
        self.speech_visited = False
        if random.random() <= 0.742:
            self.physio_visit = self.physio_time_normal()
        else:
            self.physio_visit = NUM_TICKS + 1
            self.treatment_counts['physio'] = False
        self.physio_visited = False
        if random.random() <= 0.179:
            self.diet_visit = self.admission_time + self.dietitian_time_normal()
        else:
            self.diet_visit = NUM_TICKS + 1
            self.treatment_counts['dt'] = False
        self.diet_visited = False
        if random.random() <= 0.203:
            self.social_worker_visit = self.admission_time + self.social_worker_normal()
        else:
            self.social_worker_visit = NUM_TICKS + 1
            self.treatment_counts['sw'] = False
        self.sw_visited = False
        if random.random() <= 0.023:
            self.neuro_visit = self.admission_time + self.neurologist_time_normal()
        else:
            self.neuro_visit = NUM_TICKS + 1
            self.treatment_counts['neuro'] = False
        self.neuro_visited = False
        if random.random() <= 0.022:
            self.need_cardiologist = True
            self.cardiologist_visit = self.admission_time + self.cardiology_time_normal()
        else:
            self.need_cardiologist = False
            self.cardiologist_visit = NUM_TICKS + 1
            self.treatment_counts['cardio'] = False
        self.cardio_visited = False

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
            elif self.arrived:
                if self.check_treatments():
                    if self.model.current_time - 20 >= self.admission_time:
                        self.discharge = self.model.current_time
                        self.model.schedule.remove(self)
                if self.model.current_time - 1 > self.icu_arrival_time and not self.icu_arrived and self.need_icu:
                    self.icu_arrival_time = self.model.current_time
                    self.icu_arrived = True
                    self.in_icu = True
                elif self.model.current_time >= self.icu_outtime and self.in_icu:
                    self.in_icu = False
                    self.treatment_counts['icu'] = False
                    if self.icu_outtime == self.neuro_time:
                        self.neuro_ward_admission()
                    if self.model.current_time - 1 > self.icu_outtime:
                        self.icu_outtime = self.model.current_time
                elif ((self.icu_arrived and not self.in_icu) or not self.need_icu) and not self.neuro_ward_arrived and \
                        self.model.current_time >= self.neuro_time:
                    self.neuro_ward_admission()
                elif self.model.current_time >= self.neuro_outtime and self in self.model.neuro_patients:
                    if self.model.current_time - 1 >= self.neuro_outtime:
                        self.neuro_outtime = self.model.current_time
                    self.model.neuro_patients.remove(self)
                    self.treatment_counts['neuro_ward'] = False  # for leaving neurology ward
            if self.model.current_time >= self.ct_time - 1 and not self.ct_treated:
                if self.model.ct_patients.count(self) == 0:
                    self.model.ct_patients.append(self)
            if self.model.current_time >= self.t_time - 1 and not self.tpa_treated:
                if self.model.t_patients.count(self) == 0 and self.check_permitted():
                    self.model.t_patients.append(self)
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
        if not self.tpa_permitted:
            return False
        else:
            if self.model.current_time - self.time_of_stroke <= 270:
                self.tpa_permitted = True
            else:
                self.tpa_permitted = False
                self.treatment_counts['tpa'] = False
            return self.tpa_permitted

    def neuro_ward_admission(self):
        if self.model.current_time - 1 > self.neuro_time:
            self.neuro_time = self.model.current_time
        self.neuro_ward_arrived = True
        self.last_treatment = self.model.current_time
        self.model.neuro_patients.append(self)

    def admission_time_normal(self):
        if random.random() < 0.956:
            return stats.skewnorm.rvs(4, 146.3, 269.8)
        else:
            return stats.gamma.rvs(1.21, 1002.4, 320.2)

    def neuro_time_normal(self):
        n = random.random()
        if self.icu_outtime == 0:
            time = self.admission_time
            if n < 0.136:
                time += stats.skewnorm.rvs(2.89, 0.762, 0.716)
            elif 0.136 <= n < 0.824:
                time += stats.skewnorm.rvs(2.38, 45.2, 49.6)
            elif 0.824 <= n < 0.991:
                time += stats.gamma.rvs(0.84, 201.1, 2428.7)
            else:
                time += stats.gamma.rvs(0.409, 10089.2, 10251.9)
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
        if n < 0.041 and not self.hospital_arrival == self.admission_time:  # <0 minutes (happens in ed)
            return self.hospital_arrival + stats.gamma.rvs(2.15, 42.2, 82.7)
        if n < 0.318:  # 0 to 300 mins
            return self.admission_time + stats.gamma.rvs(5.91, -45.7, 28)
        elif 0.277 <= n < 0.972:  # 300 to 30000 mins
            return self.admission_time + stats.gamma.rvs(0.973, 300.3, 5128.5)
        else:  # 30000 to 80000 mins
            return self.admission_time + stats.gamma.rvs(0.896, 30021.7, 12822.1)

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
        if random.random() >= 0.808:
            return stats.gamma.rvs(1.21, 16.03, 3320.7)
        else:
            return stats.gamma.rvs(0.735, 15177, 16620.2)

    def neurologist_time_normal(self):
        return stats.gamma.rvs(0.566, 5.92, 14428.2)

    def check_treatments(self):
        for key in self.treatment_counts.keys():
            if self.treatment_counts[key]:
                return False
        return True
