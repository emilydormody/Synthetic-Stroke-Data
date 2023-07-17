import datetime
import random

import numpy as np
from mesa import Agent
from datetime import time
from specialist import Specialist
from patient import Patient
from values import NUM_PATIENTS


class CTScan(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if len(self.model.ct_patients) != 0:
                    self.current_patient = self.model.ct_patients.pop(0)
                    if self.model.current_time - 1 > self.current_patient.ct_time:
                        self.current_patient.ct_time = self.model.current_time
                    self.current_patient.in_treatment = True
        if self.current_patient is not None:
            if self.current_patient.ct_time < self.model.current_time - self.treatment_time:
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
                        if self.model.current_time - 1 > self.current_patient.t_time:
                            self.current_patient.t_time = self.model.current_time
                        self.current_patient.in_treatment = True
        else:
            for patient in self.model.t_patients:
                if not patient.check_permitted():
                    self.model.t_patients.remove(patient)
        if self.current_patient is not None:
            if self.current_patient.t_time < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient.tpa_treated = True
                self.current_patient = None


class OccupationalTherapist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.occupational_visit = self.model.current_time
                else:
                    for i in range(len(self.model.ocu_patients)):
                        self.current_patient = self.model.ocu_patients.pop(0)
                        self.current_patient.ocu_visited = True
                        if self.model.current_time - 1 > self.current_patient.occupational_visit:
                            self.current_patient.occupational_visit = self.model.current_time
                        self.current_patient.in_treatment = True
                        self.daily_stroke_patients -= 1
                        break
        if self.current_patient is not None:
            if self.current_patient.occupational_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None



class PhysioTherapist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.physio_visit = self.model.current_time
                    self.busy = True
                else:
                    for i in range(len(self.model.physio_patients)):
                        self.current_patient = self.model.physio_patients.pop(0)
                        self.current_patient.physio_visited = True
                        if self.model.current_time - 1 > self.current_patient.physio_visit:
                            self.current_patient.physio_visit = self.model.current_time
                        self.current_patient.in_treatment = True
                        self.daily_stroke_patients -= 1
                        break
        if self.current_patient is not None:
            if self.current_patient.physio_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None


class SpeechPathologist(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.speech_visit = self.model.current_time
                else:
                    for i in range(len(self.model.speech_patients)):
                        self.current_patient = self.model.speech_patients.pop(0)
                        self.current_patient.speech_visited = True
                        if self.model.current_time - 1 > self.current_patient.speech_visit:
                            self.current_patient.speech_visit = self.model.current_time
                        self.current_patient.in_treatment = True
                        self.daily_stroke_patients -= 1
                        break
        if self.current_patient is not None:
            if self.current_patient.speech_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None


class Dietitian(Specialist):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.treatment_time = 30

    def step(self):
        if super().working_hours():
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.diet_visit = self.model.current_time
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.diet_visit == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.diet_visit = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.daily_stroke_patients -= 1
                                break
        if self.current_patient is not None:
            if self.current_patient.diet_visit < self.model.current_time - self.treatment_time:
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
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.social_worker_visit = self.model.current_time
                else:
                    for i in range(len(self.model.social_work_patients)):
                        self.current_patient = self.model.social_work_patients.pop(0)
                        self.current_patient.sw_visited = True
                        if self.model.current_time - 1 > self.current_patient.social_worker_visit:
                            self.current_patient.social_worker_visit = self.model.current_time
                        self.current_patient.in_treatment = True
                        self.daily_stroke_patients -= 1
                        break
        if self.current_patient is not None:
            if self.current_patient.social_worker_visit < self.model.current_time - self.treatment_time:
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
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.neuro_visit = self.model.current_time
                else:
                    for i in range(len(self.model.neurologist_patients)):
                        self.current_patient = self.model.neurologist_patients.pop(0)
                        self.current_patient.neuro_visited = True
                        if self.model.current_time - 1 > self.current_patient.neuro_visit:
                            self.current_patient.neuro_visit = self.model.current_time
                        self.current_patient.in_treatment = True
                        self.daily_stroke_patients -= 1
                        break
        if self.current_patient is not None:
            if self.current_patient.neuro_visit < self.model.current_time - self.treatment_time:
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
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.bloodwork = self.model.current_time
                else:
                    for i in np.random.permutation(len(self.model.neuro_patients)):
                        patient = self.model.neuro_patients[i]
                        if patient.last_treatment < self.model.current_time - 10:
                            if patient.bloodwork == 0 and not patient.in_treatment:
                                self.current_patient = patient
                                patient.bloodwork = self.model.current_time
                                self.current_patient.in_treatment = True
                                self.daily_stroke_patients -= 1
                                break
        if self.current_patient is not None:
            if self.current_patient.bloodwork < self.model.current_time - self.treatment_time:
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
            if self.current_patient is None:
                if random.randint(0, 1) == 0:
                    self.current_patient = Patient(NUM_PATIENTS+1, self.model)
                    self.current_patient.cardiologist_visit = self.model.current_time
                else:
                    for i in range(len(self.model.cardio_patients)):
                        self.current_patient = self.model.cardio_patients.pop(0)
                        self.current_patient.cardio_visited = True
                        if self.model.current_time - 1 > self.current_patient.cardiologist_visit:
                            self.current_patient.cardiologist_visit = self.model.current_time
                        self.current_patient.in_treatment = True
                        self.daily_stroke_patients -= 1
                        break
        if self.current_patient is not None:
            if self.current_patient.cardiologist_visit < self.model.current_time - self.treatment_time:
                self.current_patient.last_treatment = self.model.current_time
                self.current_patient.in_treatment = False
                self.current_patient = None


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
        if self.current_patient is not None:
            if self.current_patient.last_checkin < self.model.current_time - self.treatment_time:
                self.current_patient.in_treatment = False
                self.current_patient = None
