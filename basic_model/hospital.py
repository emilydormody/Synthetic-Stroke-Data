from mesa import Agent, Model
import mesa.time
import datetime
from patient import Patient
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
        for i in range(5):
            ct = CTScan(600+i, self)
            self.schedule.add(ct)
        tpa = TPA(610, self)
        ocu = OccupationalTherapist(620, self)
        phys1 = PhysioTherapist(630, self)
        phys2 = PhysioTherapist(631, self)
        sp = SpeechPathologist(640, self)
        diet = Dietitian(650, self)
        sw1 = SocialWorker(660, self)
        sw2 = SocialWorker(661, self)
        neuro = Neurologist(670, self)
        cd = Cardiologist(680, self)
        for i in range(5):
            bw = BloodWork(690+i, self)
            self.schedule.add(bw)
        for i in range(8):
            nurse = Nurse(6100+i, self)
            self.schedule.add(nurse)
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

    def step(self):
        self.schedule.step()
        self.current_time += 1


    def convert_time(self, time):
        if time == 0:
            return None
        date = datetime.datetime.now()
        date += datetime.timedelta(minutes=time)
        return str(date)[0:19]

    def patient_info(self):
        dict = {"Patient Id": [], "Age": [], "Gender": [], "Time of Stroke": [], "Arrival Time": [], "CT Scan Time": [],
                "TPA Treatment Time": [], "ICU Arrival Time": [], "Neurology Ward Arrival Time": [],
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
