from mesa import Agent, Model
import mesa.time
from .different_specialists import *
from .values import *


class Hospital(Model):
    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.current_time = 1
        self.ed_patients = []
        self.ct_patients = []
        self.t_patients = []
        self.neuro_patients = []
        self.all_patients = []
        self.ocu_patients = []
        self.physio_patients = []
        self.speech_patients = []
        self.social_work_patients = []
        self.cardio_patients = []
        self.neurologist_patients = []
        self.dietitian_patients = []
        self.start_date = datetime.datetime.now()
        self.add_agents()

    def step(self):
        self.schedule.step()
        self.current_time += 1


    def convert_time(self, time):
        if time <= 0 or time > NUM_TICKS:
            return None
        date = self.start_date + datetime.timedelta(minutes=time)
        return str(date)[0:19]

    def patient_info(self):
        dict = {"Patient Id": [], "Age": [], "Gender": [], "Time of Stroke": [], "ED Arrival Time": [],
                "Arrival Time": [], "Arrival Transport": [], "CT Scan Time": [],
                "TPA Treatment Time": [], "ICU Arrival Time": [],
                "ICU Checkout Time": [], "Neurology Ward Arrival Time": [],
                "Occupational Therapist Visit": [],
                "Speech Pathologist Visit": [], "Physiotherapist Visit": [], "Dietitian Visit": [],
                "Social Worker Visit": [],
                "Cardiologist Visit": [], "Neurologist Visit": [], "Blood Work Time": [], "Last Check": []}
        for patient in self.all_patients:
            dict["Patient Id"].append(patient.name)
            dict["Age"].append(patient.age)
            dict["Gender"].append(patient.gender)
            dict["Time of Stroke"].append(self.convert_time(patient.time_of_stroke))
            if patient.ed_arrived:
                dict["ED Arrival Time"].append(self.convert_time(patient.hospital_arrival))
            else:
                dict["ED Arrival Time"].append(None)
            dict["Arrival Time"].append(self.convert_time(patient.admission_time))
            dict["Arrival Transport"].append(patient.transport)
            dict["CT Scan Time"].append(self.convert_time(patient.ct_time))
            if patient.tpa_treated:
                dict["TPA Treatment Time"].append(self.convert_time(patient.t_time))
            else:
                dict["TPA Treatment Time"].append(None)
            dict["ICU Arrival Time"].append(self.convert_time(patient.icu_arrival_time))
            dict["ICU Checkout Time"].append(self.convert_time(patient.icu_outtime))
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

    def ticks(self):
        dict = {'patient_id': [], 'time_of_stroke': [], 'ed_intime': [], 'admittime': [], 'discharge': [], 'ct_scan': [], 'tpa_time': [],
                'icu_intime': [], 'icu_outtime': [], 'icu_arrived': [], 'neuro_intime': [],'neuro_outtime': [], 'ocu': [],'physio': [],
                'social_work': [],'dietitian': [], 'cardiologist': [], 'speech_lang': [],'neurologist': [] }
        for patient in self.all_patients:
            dict['patient_id'].append(patient.unique_id)
            dict['time_of_stroke'].append(patient.time_of_stroke)
            if patient.ed_arrived:
                dict['ed_intime'].append(patient.hospital_arrival)
            else:
                dict['ed_intime'].append(None)
            dict['admittime'].append(patient.admission_time)
            dict['discharge'].append(patient.discharge)
            if patient.ct_treated:
                dict['ct_scan'].append(patient.ct_time)
            else:
                dict['ct_scan'].append(None)
            if patient.tpa_treated:
                dict['tpa_time'].append(patient.t_time)
            else:
                dict['tpa_time'].append(None)
            if patient.icu_arrived:
                dict['icu_arrived'].append(True)
                dict['icu_intime'].append(patient.icu_arrival_time)
                dict['icu_outtime'].append(patient.icu_outtime)
            else:
                dict['icu_arrived'].append(False)
                dict['icu_intime'].append(None)
                dict['icu_outtime'].append(None)
            if patient.neuro_time <= NUM_TICKS:
                dict['neuro_intime'].append(patient.neuro_time)
                dict['neuro_outtime'].append(patient.neuro_outtime)
            else:
                dict['neuro_intime'].append(None)
                dict['neuro_outtime'].append(None)
            if patient.occupational_visit <= NUM_TICKS:
                dict['ocu'].append(patient.occupational_visit)
            else:
                dict['ocu'].append(None)
            if patient.physio_visit <= NUM_TICKS:
                dict['physio'].append(patient.physio_visit)
            else:
                dict['physio'].append(None)
            if patient.speech_visit <= NUM_TICKS:
                dict['speech_lang'].append(patient.speech_visit)
            else:
                dict['speech_lang'].append(None)
            if patient.cardiologist_visit <= NUM_TICKS:
                dict['cardiologist'].append(patient.cardiologist_visit)
            else:
                dict['cardiologist'].append(None)
            if patient.social_worker_visit <= NUM_TICKS:
                dict['social_work'].append(patient.social_worker_visit)
            else:
                dict['social_work'].append(None)
            if patient.diet_visited:
                dict['dietitian'].append(patient.diet_visit)
            else:
                dict['dietitian'].append(None)
            if patient.neuro_visit <= NUM_TICKS:
                dict['neurologist'].append(patient.neuro_visit)
            else:
                dict['neurologist'].append(None)
        return dict

    def before_ticks(self):
        dict = {'patient_id': [], 'time_of_stroke': [], 'ed_intime': [], 'admittime': [], 'ct_scan': [], 'tpa_time': [],
                'icu_intime': [], 'icu_outtime': [],'neuro_intime': [], 'neuro_outtime': [], 'ocu': [],
                'physio': [], 'social_work': [], 'cardiologist': [], 'speech_lang': [], 'neurologist': []}
        for patient in self.all_patients:
            dict['patient_id'].append(patient.unique_id)
            dict['time_of_stroke'].append(patient.time_of_stroke)
            dict['ed_intime'].append(patient.hospital_arrival)
            dict['admittime'].append(patient.admission_time)
            dict['ct_scan'].append(patient.ct_time)
            if patient.hospital_arrival - patient.t_time <= 270:
                dict['tpa_time'].append(patient.t_time)
            else:
                dict['tpa_time'].append(None)
            if patient.need_icu:
                dict['icu_intime'].append(patient.icu_arrival_time)
                dict['icu_outtime'].append(patient.icu_outtime)
            else:
                dict['icu_intime'].append(None)
                dict['icu_outtime'].append(None)
            dict['neuro_intime'].append(patient.neuro_time)
            dict['neuro_outtime'].append(patient.neuro_outtime)
            dict['ocu'].append(patient.occupational_visit)
            dict['physio'].append(patient.physio_visit)
            dict['speech_lang'].append(patient.speech_visit)
            dict['cardiologist'].append(patient.cardiologist_visit)
            dict['social_work'].append(patient.social_worker_visit)
            dict['neurologist'].append(patient.neuro_visit)
        return dict

    def add_agents(self):
        for i in range(NUM_PATIENTS):
            patient = Patient(i, self)
            self.schedule.add(patient)
            self.all_patients.append(patient)

        shift_num = 0
        for i in range(NUM_PER_SPECIALISTS):
            ct = CTScan(6000 + i, self)
            tpa = TPA(6100 + i, self)
            ocu = OccupationalTherapist(6200 + i, self)
            phys1 = PhysioTherapist(6300 + i, self)
            sp = SpeechPathologist(6400 + i, self)
            dt = Dietitian(6500 + i, self)
            sw1 = SocialWorker(6600 + i, self)
            neuro = Neurologist(6700 + i, self)
            cd = Cardiologist(6800 + i, self)
            self.schedule.add(ct)
            self.schedule.add(tpa)
            self.schedule.add(ocu)
            self.schedule.add(phys1)
            self.schedule.add(sp)
            self.schedule.add(dt)
            self.schedule.add(sw1)
            self.schedule.add(neuro)
            self.schedule.add(cd)
            if shift_num > 0:
                ct.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                tpa.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                ocu.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                phys1.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                sp.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                dt.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                sw1.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                neuro.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
                cd.set_schedule(SHIFT_LST[shift_num][0], SHIFT_LST[shift_num][1])
            shift_num += 1
            print(shift_num)
            if shift_num >= len(SHIFT_LST):
                shift_num = 0


        # for i in range(4):
        #     ct = CTScan(6000 + i, self)
        #     self.schedule.add(ct)
        # for i in range(2):
        #     ct = CTScan(6004+i, self)
        #     ct.set_schedule(16, 6)
        #     self.schedule.add(ct)
        # for i in range(2):
        #     ct = CTScan(6006 + i, self)
        #     ct.set_schedule(4,12)
        #     self.schedule.add(ct)
        # tpa = TPA(6010, self)
        # tpa.set_schedule(8, 22)
        # tpa2 = TPA(6011, self)
        # tpa2.set_schedule(22, 8)
        # self.schedule.add(tpa)
        # self.schedule.add(tpa2)
        #
        # for i in range(4):
        #     ocu = OccupationalTherapist(6020+i, self)
        #     self.schedule.add(ocu)
        # for j in range(2):
        #     ocu = OccupationalTherapist(6024+j, self)
        #     ocu.set_schedule(14,20)
        #     self.schedule.add(ocu)
        # for k in range(2):
        #     ocu = OccupationalTherapist(6026+k, self)
        #     ocu.set_schedule(20,5)
        #     self.schedule.add(ocu)
        # ocu = OccupationalTherapist(6028, self)
        # ocu.set_schedule(4,11)
        # self.schedule.add(ocu)
        #
        # for i in range(5):
        #     phys1 = PhysioTherapist(6030+i, self)
        #     self.schedule.add(phys1)
        # for i in range(2):
        #     phys2 = PhysioTherapist(6035+i, self)
        #     phys2.set_schedule(16,0)
        #     self.schedule.add(phys2)
        # phys3 = PhysioTherapist(6037, self)
        # phys3.set_schedule(0, 7)
        # self.schedule.add(phys3)
        # phys4 = PhysioTherapist(6038, self)
        # phys4.set_schedule(1,8)
        # self.schedule.add(phys4)
        #
        # for i in range(3):
        #     sp = SpeechPathologist(6040+i, self)
        #     self.schedule.add(sp)
        # for j in range(2):
        #     sp = SpeechPathologist(6043+j, self)
        #     sp.set_schedule(13,22)
        #     self.schedule.add(sp)
        # for k in range(2):
        #     sp = SpeechPathologist(6045+k, self)
        #     sp.set_schedule(20,4)
        #     self.schedule.add(sp)
        # sp = SpeechPathologist(6047, self)
        # sp.set_schedule(0,8)
        # self.schedule.add(sp)
        #
        # for i in range(4):
        #     dt = Dietitian(6050 + i, self)
        #     self.schedule.add(dt)
        # for j in range(2):
        #     dt = Dietitian(6054 + j, self)
        #     dt.set_schedule(14, 20)
        #     self.schedule.add(dt)
        # for k in range(2):
        #     dt = Dietitian(6056 + k, self)
        #     dt.set_schedule(20, 5)
        #     self.schedule.add(dt)
        # dt = Dietitian(6058, self)
        # dt.set_schedule(4, 11)
        # self.schedule.add(dt)
        #
        # for i in range(4):
        #     sw1 = SocialWorker(6060+i, self)
        #     self.schedule.add(sw1)
        # for j in range(2):
        #     sw = SocialWorker(6064 + j, self)
        #     sw.set_schedule(14, 20)
        #     self.schedule.add(sw)
        # for k in range(2):
        #     sw = SocialWorker(6066 + k, self)
        #     sw.set_schedule(20, 5)
        #     self.schedule.add(sw)
        # sw = SocialWorker(6068, self)
        # sw.set_schedule(4, 11)
        # self.schedule.add(sw)
        #
        # for i in range(3):
        #     neuro = Neurologist(6070+i, self)
        #     neuro.set_schedule(8, 20)
        #     self.schedule.add(neuro)
        #     neuro1 = Neurologist(6073+i, self)
        #     neuro1.set_schedule(20, 8)
        #     self.schedule.add(neuro1)
        #
        #
        # for i in range(3):
        #     cd = Cardiologist(6080+i, self)
        #     self.schedule.add(cd)
        # for j in range(2):
        #     cd = Cardiologist(6083+j, self)
        #     cd.set_schedule(14,23)
        #     self.schedule.add(cd)
        # cd = Cardiologist(6085, self)
        # cd.set_schedule(22,8)
        # self.schedule.add(cd)

        # for i in range(5):
        #     bw = BloodWork(690 + i, self)
        #     self.schedule.add(bw)
        #     bw.set_schedule(8, 16)
        # for i in range(4):
        #     nurse = Nurse(6100 + i, self)
        #     self.schedule.add(nurse)
        #     nurse.set_schedule(8, 20)
        # for i in range(4):
        #     nurse = Nurse(6104 + i, self)
        #     self.schedule.add(nurse)
        #     nurse.set_schedule(20, 8)

