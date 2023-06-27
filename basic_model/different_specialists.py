import datetime
import random

import numpy as np
from mesa import Agent
from datetime import time
from specialist import Specialist
from patient import Patient


class CTScan(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if len(self.model.ct_patients) != 0:
                    self.current_patient = self.model.ct_patients.pop(0)
                    self.current_patient.ct_time = self.model.current_time
                    self.current_patient.in_treatment = True
            elif self.current_patient.ct_time < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient.ct_treated = True
                self.current_patient = None


class TPA(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 15

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if len(self.model.t_patients) != 0:
                    patient = self.model.t_patients.pop(0)
                    if patient.check_permitted():
                        self.current_patient = patient
                        self.current_patient.t_time = self.model.current_time
                        self.current_patient.in_treatment = True
                    else:
                        patient.tpa_permitted = False
            elif self.current_patient.t_time < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient.tpa_treated = True
                self.current_patient = None
        else:
            for patient in self.model.t_patients:
                if not patient.check_permitted():
                    self.model.t_patients.remove(patient)


class OccupationalTherapist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.occupational_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.occupational_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.occupational_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.occupational_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False



class PhysioTherapist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.physio_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.physio_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.physio_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.physio_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class SpeechPathologist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.speech_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.speech_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.speech_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.speech_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class Dietitian(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.diet_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.diet_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.diet_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.diet_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class SocialWorker(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.social_worker_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.social_worker_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.social_worker_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.social_worker_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class Neurologist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.neuro_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.neuro_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.neuro_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.neuro_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class BloodWork(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 20

    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.bloodwork = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.bloodwork == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.bloodwork = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.bloodwork < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class Cardiologist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30


    def step(self):
        if super().working_hours():
            if not self.busy:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(10000, self.model)
                    self.current_patient.cardiologist_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.need_cardiologist and patient.last_treatment < self.model.current_time - 10:
                            if patient.cardiologist_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.cardiologist_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.busy = True
                                self.daily_stroke_patients -= 1
                                break
            elif self.current_patient.cardiologist_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None
                self.busy = False


class Nurse(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 5

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                for i in np.random.permutation(len(self.model.neuro_patients)):
                    patient = self.model.neuro_patients[i]
                    if not patient.in_treatment:
                        self.current_patient = patient
                        patient.last_checkin = self.model.current_time
                        self.current_patient.in_treatment = True
                        break
            elif self.current_patient.last_checkin < self.model.current_time - self.treatment_time:
                self.current_patient.in_treatment = False
                self.current_patient = None
