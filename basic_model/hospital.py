from mesa import Agent, Model
import mesa.time
import datetime
from patient import Patient
from different_specialists import*


class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 1
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = []
        self.all_patients = []
        self.date = datetime.datetime.now()
        self.add_specialists()


    def step(self):
        self.schedule.step()
        self.current_time += 1


    def convert_time(self, time):
        if time == 0:
            return None
        date = self.date+datetime.timedelta(minutes=time)
        return str(date)[0:19]


    def patient_info(self):
        dict = {"Patient Id": [], "Age": [], "Gender": [], "Time of Stroke": [], "Arrival Time": [], "CT Scan Time": [],
                "TPA Treatment Time": [],
                "Reason for Rejecting TPA": [], "ICU Arrival Time": [], "Neurology Ward Arrival Time": [],
                "Occupational Therapist Visit": [],
                "Speech Pathologist Visit": [], "Physiotherapist Visit": [], "Dietitian Visit": [],
                "Social Worker Visit": [],
                "Cardiologist Visit": [], "Neurologist Visit": [], "Blood Work Time": [], "Last Check": []}
        for patient in self.all_patients:
            dict["Patient Id"].append(patient.name)
            dict["Age"].append(patient.age)
            dict["Gender"].append(patient.gender)
            dict["Time of Stroke"].append(self.convert_time(patient.time_of_stroke))
            dict["Arrival Time"].append(self.convert_time(patient.admission_time))
            dict["CT Scan Time"].append(self.convert_time(patient.ct_time))
            dict["TPA Treatment Time"].append(self.convert_time(patient.t_time))
            if patient.tpa_denied:
                reason = "Patient/family refusal"
            elif patient.t_time == 0:
                reason = "Arrived later then 4.5 Hours"
            else:
                reason = None
            dict["Reason for Rejecting TPA"].append(reason)
            dict["ICU Arrival Time"].append(self.convert_time(patient.icu_arrival_time))
            dict["Neurology Ward Arrival Time"].append(self.convert_time(patient.neuro_time))
            dict["Occupational Therapist Visit"].append(self.convert_time(patient.occupational_visit))
            dict["Speech Pathologist Visit"].append(self.convert_time(patient.speech_visit))
            dict["Physiotherapist Visit"].append(self.convert_time(patient.physio_visit))
            dict["Dietitian Visit"].append(self.convert_time(patient.diet_visit))
            dict["Social Worker Visit"].append(self.convert_time(patient.social_worker_visit))
            if patient.cardiologist_visit == 0:
                dict["Cardiologist Visit"].append(None)
            else:
                dict["Cardiologist Visit"].append(self.convert_time(patient.cardiologist_visit))
            dict["Neurologist Visit"].append(self.convert_time(patient.neuro_visit))
            dict["Blood Work Time"].append(self.convert_time(patient.bloodwork))
            dict["Last Check"].append(self.convert_time(patient.last_checkin))
        return dict

    def add_specialists(self):
        for i in range(100):
            patient = Patient(i, self)
            self.schedule.add(patient)
            self.all_patients.append(patient)
        for i in range(4):
            ct = CTScan(600 + i, self)
            ct.set_schedule(8, 16)
            self.schedule.add(ct)
        ct = CTScan(604, self)
        ct.set_schedule(16, 6)
        self.schedule.add(ct)
        tpa = TPA(610, self)
        tpa.set_schedule(8, 20)
        ocu = OccupationalTherapist(620, self)
        ocu.set_schedule(8, 16)
        phys1 = PhysioTherapist(630, self)
        phys1.set_schedule(8, 16)
        phys2 = PhysioTherapist(631, self)
        phys2.set_schedule(8, 16)
        sp = SpeechPathologist(640, self)
        sp.set_schedule(8, 16)
        diet = Dietitian(650, self)
        diet.set_schedule(8, 16)
        sw1 = SocialWorker(660, self)
        sw1.set_schedule(8, 16)
        sw2 = SocialWorker(661, self)
        sw2.set_schedule(8, 16)
        neuro = Neurologist(670, self)
        neuro1 = Neurologist(671, self)
        neuro.set_schedule(8, 20)
        neuro1.set_schedule(20,8)
        cd = Cardiologist(680, self)
        cd.set_schedule(8, 16)
        for i in range(5):
            bw = BloodWork(690 + i, self)
            self.schedule.add(bw)
            bw.set_schedule(8, 16)
        for i in range(4):
            nurse = Nurse(6100 + i, self)
            self.schedule.add(nurse)
            nurse.set_schedule(8, 20)
        for i in range(4):
            nurse = Nurse(6104 +i, self)
            self.schedule.add(nurse)
            nurse.set_schedule(20, 8)
        self.schedule.add(tpa)
        self.schedule.add(ocu)
        self.schedule.add(phys1)
        self.schedule.add(phys2)
        self.schedule.add(sp)
        self.schedule.add(diet)
        self.schedule.add(sw1)
        self.schedule.add(sw2)
        self.schedule.add(neuro)
        self.schedule.add(cd)
