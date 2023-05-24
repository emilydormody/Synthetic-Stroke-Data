from mesa import Agent, Model
import mesa.time
import numpy as np
from patient_and_patientdata import Patient, PatientData
from specialists import*


class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 1
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = []  # modelled to have only one of each treatment happen at a time
        self.occupational_patient = None
        self.speech_patient = None
        self.physio_patient = None
        self.diet_patient = None
        self.social_worker_patient = None
        self.neuro_patient = None
        self.cardiologist_patient = None
        self.neuro_lst = [0 for x in range(7)]
        self.all_patients = []
        for i in range(100):
            patient = Patient(i, self)
            self.schedule.add(patient)
            self.all_patients.append(patient)
        ct1 = CTScan(600, self)
        ct2 = CTScan(601, self)
        tpa = TPA(602, self)
        ocu = OccupationalTherapist(603, self)
        phys1 = PhysioTherapist(604, self)
        phys2 = PhysioTherapist(605, self)
        sp = SpeechPathologist(606, self)
        diet = Dietitian(607, self)
        self.schedule.add(ct1)
        self.schedule.add(ct2)
        self.schedule.add(tpa)
        self.schedule.add(ocu)
        self.schedule.add(phys1)
        self.schedule.add(phys2)
        self.schedule.add(sp)
        self.schedule.add(diet)
        self.patient_data = PatientData(self)

    def step(self):
        self.neuro_ward_ordered_treatment()
        self.schedule.step()
        self.current_time += 1


    def neuro_ward_ordered_treatment(self):
        self.neuro_reset()
        for i in np.random.permutation(len(self.neuro_patients)):
            patient = self.neuro_patients[i]
            if patient.last_treatment <= self.current_time - 30 and not patient.in_treatment:
                if patient.bloodwork == 0:
                    patient.last_treatment = self.current_time
                    patient.bloodwork = self.current_time
                # elif patient.occupational_visit == 0 and self.occupational_patient is None:
                #     patient.last_treatment = self.current_time
                #     patient.occupational_visit = self.current_time
                #     self.occupational_patient = patient
                # elif patient.speech_visit == 0 and self.speech_patient is None:
                #     patient.last_treatment = self.current_time
                #     patient.speech_visit = self.current_time
                #     self.speech_patient = patient
                # elif patient.physio_visit == 0 and self.physio_patient is None:
                #     patient.last_treatment = self.current_time
                #     patient.physio_visit = self.current_time
                #     self.physio_patient = patient
                # elif patient.diet_visit == 0 and self.diet_patient is None:
                #     patient.last_treatment = self.current_time
                #     patient.diet_visit = self.current_time
                #     self.diet_patient = patient
                elif patient.social_worker_visit == 0 and self.social_worker_patient is None:
                    patient.last_treatment = self.current_time
                    patient.social_worker_visit = self.current_time
                    self.social_worker_patient = patient
                elif patient.neuro_visit == 0 and self.neuro_patient is None:
                    patient.last_treatment = self.current_time
                    patient.neuro_visit = self.current_time
                    self.neuro_patient = patient
                elif patient.cardiologist_visit == 0 and patient.need_cardiologist and self.cardiologist_patient is None:
                    patient.last_treatment = self.current_time
                    patient.cardiologist_visit = self.current_time
                    self.cardiologist_patient = patient

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
                if patient.bloodwork == 0:
                    patient.last_treatment = self.current_time
                    patient.bloodwork = self.current_time
                else:
                    self.find_next_space(patient)
        for patient in self.neuro_patients:
            if patient.fully_treated():
                self.neuro_patients.remove(patient)

    def find_next_space(self, patient):
        if self.neuro_lst.count(0) == 0:
            return
        for space in range(len(self.neuro_lst)):
            if self.neuro_lst[space] == 0:
                if space == 0 and patient.occupational_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.occupational_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
                elif space == 1 and patient.speech_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.speech_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
                elif space == 2 and patient.physio_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.physio_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
                elif space == 3 and patient.diet_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.diet_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
                elif space == 4 and patient.social_worker_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.social_worker_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
                elif space == 5 and patient.neuro_visit == 0:
                    patient.last_treatment = self.current_time
                    patient.neuro_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
                elif space == 6 and patient.cardiologist_visit == 0 and patient.need_cardiologist:
                    patient.last_treatment = self.current_time
                    patient.cardiologist_visit = self.current_time
                    self.neuro_lst[space] = patient
                    return
