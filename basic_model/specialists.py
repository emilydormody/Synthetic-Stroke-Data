import numpy as np
from mesa import Agent


class CTScan(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.treatment_time = 30
        self.current_patient = None

    def step(self):
        if self.current_patient is None:
            if len(self.model.ct_patients) != 0:
                self.current_patient = self.model.ct_patients.pop(0)
                self.current_patient.ct_time = self.model.current_time
                self.current_patient.in_treatment = True
                print(self.current_patient.unique_id, ' ct start ', self.model.current_time, ' with ', self.name)
        elif self.current_patient.ct_time < self.model.current_time - self.treatment_time:
            print(self.current_patient.unique_id, ' ct end ', self.model.current_time, ' with ', self.name)
            self.current_patient.last_treatment = self.model.current_time
            self.current_patient.in_treatment = False
            self.current_patient = None


class TPA(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.treatment_time = 15
        self.current_patient = None

    def step(self):
        if self.current_patient is None:
            if len(self.model.t_patients) != 0:
                patient = self.model.t_patients.pop(0)
                if patient.check_permitted():
                    self.current_patient = patient
                    self.current_patient.t_time = self.model.current_time
                    self.current_patient.in_treatment = True
                    print(self.current_patient.unique_id, ' tpa start ', self.model.current_time, ' with ', self.name)
                else:
                    patient.tpa_permitted = False
        elif self.current_patient.t_time < self.model.current_time - self.treatment_time:
            print(self.current_patient.unique_id, ' tpa end ', self.model.current_time, ' with ', self.name)
            self.current_patient.last_treatment = self.model.current_time
            self.current_patient.in_treatment = False
            self.current_patient = None


class OccupationalTherapist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.treatment_time = 30
        self.current_patient = None

    def step(self):
        if self.current_patient is None:
            for i in np.random.permutation(len(self.model.neuro_patients)):
                patient = self.model.neuro_patients[i]
                if patient.occupational_visit == 0 and not patient.in_treatment:
                    self.current_patient = patient
                    patient.occupational_visit = self.model.current_time
                    self.current_patient.in_treatment = True
                    break
        elif self.current_patient.occupational_visit < self.model.current_time - self.treatment_time:
            self.current_patient.last_treatment = self.model.current_time
            self.current_patient.in_treatment = False
            self.current_patient = None


class PhysioTherapist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = unique_id
        self.model = model
        self.treatment_time = 30
        self.current_patient = None

    def step(self):
        if self.current_patient is None:
            for i in np.random.permutation(len(self.model.neuro_patients)):
                patient = self.model.neuro_patients[i]
                if patient.physio_visit == 0 and not patient.in_treatment:
                    self.current_patient = patient
                    patient.physio_visit = self.model.current_time
                    self.current_patient.in_treatment = True
                    break
        elif self.current_patient.physio_visit < self.model.current_time - self.treatment_time:
            self.current_patient.last_treatment = self.model.current_time
            self.current_patient.in_treatment = False
            self.current_patient = None