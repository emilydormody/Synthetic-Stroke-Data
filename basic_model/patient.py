
import random

from mesa import Agent, Model
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
        self.admission_time = random.randint(300, 8000)
        self.time_of_stroke = self.admission_time - random.randint(60, 150) - np.random.normal(60, 15)
        self.ct_time = 0
        self.t_time = 0
        self.tpa_permitted = False
        if random.randint(0,9) == 0:
            self.tpa_denied = True
        else:
            self.tpa_denied = False
        self.icu_arrival_time = 0
        if random.randint(0, 1) == 0:
            self.need_icu = True
        else:
            self.need_icu = False
        self.delay = random.uniform(0, 3)
        self.arrived = False
        self.last_treatment = -1
        self.in_treatment = False
        self.neuro_time = 0
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
        if self.model.current_time >= self.admission_time and not self.arrived:
            self.arrived = True
            self.last_treatment = self.model.current_time
        elif self.arrived and not self.in_treatment:
            if self.ct_time == 0 and not self.in_treatment:
                if self.last_treatment < self.model.current_time - self.ct_delay():
                    if self.model.ct_patients.count(self) == 0:
                        self.model.ct_patients.append(self)
            elif self.check_permitted() and self.t_time == 0:
                if self.last_treatment < self.model.current_time - self.t_delay():
                    if self.model.t_patients.count(self) == 0:
                        self.model.t_patients.append(self)
            elif (self.t_time > 0 or not self.tpa_permitted) and (self.icu_arrival_time == 0 and self.need_icu):
                if self.last_treatment < self.model.current_time - self.icu_delay():
                    if self.need_icu:
                        self.icu_arrival_time = self.model.current_time
                        self.last_treatment = self.model.current_time
            elif (self.icu_arrival_time > 0 or not self.need_icu) and self.neuro_time == 0:
                if self.last_treatment < self.model.current_time - 120:
                    self.neuro_time = self.model.current_time
                    self.last_treatment = self.model.current_time
                    self.model.neuro_patients.append(self)

    def fully_treated(self):
        return self.neuro_time != 0 and self.occupational_visit != 0 and self.speech_visit != 0 and self.physio_visit != 0 and \
               self.diet_visit != 0 and self.social_worker_visit != 0 and self.neuro_visit != 0 and \
               (self.cardiologist_visit != 0 or not self.need_cardiologist)

    def check_permitted(self):
        if self.tpa_denied:
            return False
        elif self.model.current_time - self.time_of_stroke <= 270:
            self.tpa_permitted = True
            return True
        else:
            self.tpa_permitted = False
            return False
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








