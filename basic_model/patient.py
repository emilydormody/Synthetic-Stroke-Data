import math
import random

from mesa import Agent, Model
import numpy as np
from scipy import stats


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
        self.hospital_arrival = random.randint(300, 8000)
        if random.random() >= 0.75:
            self.admission_time = self.hospital_arrival
        else:
            self.admission_time = self.hospital_arrival + self.admission_time_normal()
        self.time_of_stroke = self.hospital_arrival - random.randint(60, 150) - np.random.normal(60, 15)
        self.ct_time = self.hospital_arrival + self.ct_time_normal()
        self.ct_treated = False
        self.t_time = self.hospital_arrival + self.tpa_time_normal()
        self.tpa_treated = False
        self.tpa_permitted = False
        if random.random() >= 0.9:
            self.tpa_denied = True
        else:
            self.tpa_denied = False
        if random.random() >= 0.5:
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
        self.neuro_time = self.admission_time + self.neuro_time_normal()
        self.neuro_outtime = self.admission_time + self.neuro_outtime_normal()
        self.neuro_ward_arrived = False
        self.occupational_visit = 0
        self.speech_visit = 0
        self.physio_visit = 0
        self.diet_visit = 0
        self.social_worker_visit = 0
        self.neuro_visit = 0
        if random.randint(0, 3) == 0:
            self.need_cardiologist = True
        else:
            self.need_cardiologist = False
        self.cardiologist_visit = 0
        self.bloodwork = 0
        self.last_checkin = 0
        self.patient_info = self.get_patient_info()

    def step(self):
        if self.model.current_time >= self.hospital_arrival and not (
                self.ed_arrived or self.hospital_arrival == self.admission_time):
            self.ed_arrived = True
            self.model.ed_patients.append(self)
            self.last_treatment = self.model.current_time
            print(self.unique_id, 'ed')
        elif self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True
            if self in self.model.ed_patients:
                self.model.ed_patients.remove(self)
            self.last_treatment = self.model.current_time
            print(self.unique_id, 'arrived')
        elif self.model.current_time >= self.ct_time and not self.ct_treated:
            if self.model.ct_patients.count(self) == 0:
                self.model.ct_patients.append(self)
                print(self.unique_id, 'ct list')
        elif self.check_permitted() and not self.tpa_treated:
            if self.model.current_time >= self.t_time and self.ct_treated:
                if self.model.t_patients.count(self) == 0:
                    self.model.t_patients.append(self)
                    print(self.unique_id, 'tpa list')
        elif self.arrived and not self.in_treatment:
            if (self.tpa_treated or not self.tpa_permitted) and not self.icu_arrived and self.need_icu:
                if self.model.current_time >= self.icu_arrival_time:
                    print(self.unique_id, 'icu')
                    self.icu_arrival_time = self.model.current_time
                    self.icu_arrived = True
                    self.in_icu = True
            elif self.in_icu:
                if self.model.current_time >= self.icu_outtime:
                    self.in_icu = False
            elif ((self.icu_arrived and not self.in_icu) or not self.need_icu) and not self.neuro_ward_arrived:
                if self.model.current_time >= self.neuro_time:
                    self.neuro_ward_arrived = True
                    self.neuro_time = self.model.current_time
                    self.last_treatment = self.model.current_time
                    self.model.neuro_patients.append(self)
                    print(self.unique_id, 'neuro')

    def check_permitted(self):
        if self.tpa_denied:
            return False
        else:
            if self.model.current_time - self.time_of_stroke <= 270:
                self.tpa_permitted = True
            else:
                self.tpa_permitted = False
            return self.tpa_permitted

    def get_patient_info(self):
        dict = {}
        dict["Blood Glucose"] = 0
        dict["Temperature"] = 0
        dict["Heart Rate"] = 0
        dict["Respiratory Rate"] = 0
        dict["Blood Pressure"] = 0
        dict["Pulse Oximetry"] = 0
        dict["Swallowing Ability"] = 0
        dict["Swallowing Screen Result"] = None
        dict["Diet Type"] = None
        dict["Texture of Food"] = None
        dict["Home/Family Situation"] = 0
        dict["Mental State"] = 0
        dict["Emotional State"] = 0
        dict["Action Plan"] = 0
        dict["Environment"] = 0
        dict["Bath/Shower Ability"] = 0
        dict["Dressing"] = 0
        dict["Grooming"] = 0
        dict["Toileting"] = 0
        dict["Eating"] = 0
        dict["Bed Mobility"] = 0
        dict["Walking"] = 0
        dict["Wheelchair Mobility"] = 0
        dict["Cognition"] = 0
        dict["Perception"] = 0
        dict["Range of Motion"] = 0
        dict["Balance"] = 0
        dict["Sensation"] = 0
        dict["Proprioception"] = 0
        dict["Strength"] = 0
        dict["Manual Dexterity"] = 0
        dict["Coordination"] = 0
        dict["Ashworth Scale Result"] = 0
        dict["Accomodation"] = 0
        dict["Hand Dominance"] = 0
        dict["Pain"] = 0
        dict["Communication"] = 0
        dict["Vision"] = 0
        dict["Hearing"] = 0
        dict["Bowel/Bladder Functioning"] = 0
        dict["Cardiopulmonary Functioning"] = 0
        dict["Respiratory Functioning"] = 0
        dict["Muscle Tone"] = 0
        dict["Reflexes/Coordination"] = 0
        dict["Speech Intelligibility"] = 0
        dict["Oral Peripheral Exam Result"] = 0
        return dict

    def admission_time_normal(self):
        if random.random() < 0.956:
            return stats.skewnorm.rvs(4, 146.3, 269.8)
        else:
            return stats.gamma.rvs(1.2, 1002.4, 320.2)

    def neuro_time_normal(self):
        n = random.random()
        if n < 0.1:
            return stats.skewnorm.rvs(2.81, 0.762, 0.7)
        elif 0.1 <= n < 0.54:
            return stats.skewnorm.rvs(2.35, 45.6, 49)
        elif 0.54 <= n < 87.8:
            return stats.gamma.rvs(1.74, 95.5, 1692.1)
        else:
            return stats.gamma.rvs(0.908, 10090.3, 7966.6)

    def icu_time_normal(self):
        n = random.random()
        if n < 0.157:
            return stats.gamma.rvs(3.23, 0.237, 0.343)
        elif 0.157 <= n < 0.615:
            return stats.skewnorm.rvs(2.84, 35.6, 59.7)
        else:
            return stats.gamma.rvs(0.547,201,15138.3)

    def ct_time_normal(self):
        return 15

    def tpa_time_normal(self):
        return 45

    def neuro_outtime_normal(self):
        if random.random() < 0.941:
            return stats.gamma.rvs(2.16, -410.2, 2262.7)
        else:
            return stats.gamma.rvs(1.026, 15065.1, 6889.6)

    def icu_outtime_normal(self):
        n = random.random()
        if n < 0.285:
            return stats.skewnorm.rvs(-2.82,2085.4,805.6)
        elif 0.285 <= n < 0.941:
            return stats.gamma.rvs(0.891, 2404.5, 5009.6)
        else:
            return stats.gamma.rvs(1.05, 20001, 11464)
