from mesa import Agent, Model
import mesa.time
import numpy as np
from patient_and_patientdata import Patient

class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 1
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = []
        self.occupational_patient = None
        self.speech_patient = None
        self.physio_patient = None
        self.diet_patient = None
        self.social_worker_patient = None
        self.neuro_patient = None
        self.cardiologist_patient = None
        self.neuro_lst = [0 for x in range(7)]
        self.all_patients = []  # modelled to have only one of each treatment happen at a time
        for i in range(100):
            patient = Patient(i, self)
            self.schedule.add(patient)
            self.all_patients.append(patient)

    def step(self):
        self.treat_patients()
        self.neuro_ward_unordered()
        self.schedule.step()
        self.current_time += 1

    def treat_patients(self):
        if len(self.ct_patients) != 0:
            patient = self.ct_patients.pop(0)
            patient.ct_scanned = True
            patient.ct_time = self.current_time
            patient.last_treatment = self.current_time
            print(patient.unique_id, ' scanned at ', self.current_time)

        if len(self.t_patients) != 0:
            patient = self.t_patients.pop(0)
            patient.treated = True
            patient.t_time = self.current_time
            patient.last_treatment = self.current_time
            print(patient.unique_id, ' tpa at ', self.current_time)

        # if len(self.neuro_patients) != 0:
        #     patient = self.neuro_patients.pop(0)
        #     patient.neuro_ward = True
        #     patient.neuro_time = self.current_time
        #     patient.last_treatment = self.current_time
        #     print(patient.unique_id, ' neuro ward at ', self.current_time)

    def neuro_ward_ordered_treatment(self):
        self.neuro_reset()
        for i in np.random.permutation(len(self.neuro_patients)):
            patient = self.neuro_patients[i]
            if patient.fully_treated():
                self.neuro_patients.remove(patient)
            if patient.last_treatment <= self.current_time - 30:
                if patient.occupational_visit == 0 and self.occupational_patient is None:
                    patient.last_treatment = self.current_time
                    patient.occupational_visit = self.current_time
                    self.occupational_patient = patient
                    print(patient.unique_id, ' occupe at ', self.current_time)
                elif patient.speech_visit == 0 and self.speech_patient is None:
                    patient.last_treatment = self.current_time
                    patient.speech_visit = self.current_time
                    self.speech_patient = patient
                    print(patient.unique_id, ' speech at ', self.current_time)
                elif patient.physio_visit == 0 and self.physio_patient is None:
                    patient.last_treatment = self.current_time
                    patient.physio_visit = self.current_time
                    self.physio_patient = patient
                    print(patient.unique_id, ' physio at ', self.current_time)
                elif patient.diet_visit == 0 and self.diet_patient is None:
                    patient.last_treatment = self.current_time
                    patient.diet_visit = self.current_time
                    self.diet_patient = patient
                    print(patient.unique_id, ' diet at ', self.current_time)
                elif patient.social_worker_visit == 0 and self.social_worker_patient is None:
                    patient.last_treatment = self.current_time
                    patient.social_worker_visit = self.current_time
                    self.social_worker_patient = patient
                    print(patient.unique_id, ' sw at ', self.current_time)
                elif patient.neuro_visit == 0 and self.neuro_patient is None:
                    patient.last_treatment = self.current_time
                    patient.neuro_visit = self.current_time
                    self.neuro_patient = patient
                    print(patient.unique_id, ' neuro at ', self.current_time)
                elif patient.cardiologist_visit == 0 and patient.need_cardiologist and self.cardiologist_patient is None:
                    patient.last_treatment = self.current_time
                    patient.cardiologist_visit = self.current_time
                    self.cardiologist_patient = patient
                    print(patient.unique_id, ' cardio at ', self.current_time)

    def neuro_reset(self):
        self.occupational_patient = None
        self.speech_patient = None
        self.physio_patient = None
        self.diet_patient = None
        self.social_worker_patient = None
        self.neuro_patient = None
        self.cardiologist_patient = None

    def neuro_ward_unordered(self):
        self.neuro_lst = [0 for x in range(7)]
        for i in np.random.permutation(len(self.neuro_patients)):
            patient = self.neuro_patients[i]
            if patient.last_treatment <= self.current_time - 30:
                self.find_next_space(patient)

    def find_next_space(self, patient):
        if self.neuro_lst.count(0) == 0:
            return
        for space in range(len(self.neuro_lst)):
            if self.neuro_lst[space] == 0:
                if space == 0 and patient.occupational_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.occupational_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' occupe at ', self.current_time)
                elif space == 1 and patient.speech_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.speech_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' speech at ', self.current_time)
                elif space == 2 and patient.physio_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.physio_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' physio at ', self.current_time)
                elif space == 3 and patient.diet_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.diet_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' diet at ', self.current_time)
                elif space == 4 and patient.social_worker_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.social_worker_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' sw at ', self.current_time)
                elif space == 5 and patient.neuro_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.neuro_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' neuro at ', self.current_time)
                elif space == 6 and patient.cardiologist_visit == 0 and patient.need_cardiologist:
                    patient.last_treatment = self.current_time
                    patient.cardiologist_visit = self.current_time
                    self.neuro_lst[space] = patient
                    print(patient.unique_id, ' cardio at ', self.current_time)
                return

