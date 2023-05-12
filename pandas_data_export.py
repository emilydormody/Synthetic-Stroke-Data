from basic_model import *
import pandas as pd


def main():
    h = Hospital()
    for i in range(2880):  # 48 hours of steps
        h.step()
    for patient in h.all_patients:
        if patient.name ==  0:
            print(patient.age, patient.icu_arrival_time, patient.neuro_time)

    d = {"Patient Id": patient_name(h), "Age": patient_age(h), "Gender": patient_gender(h), "Arrival Time": track_arrivals(h),
         "CT Scan Time": track_ctscans(h), "Thrombolysis Treatment Time": track_treatment(h),"ICU Arrival Time": track_icu_arrival(h),
         "Neurologist Visit Time": track_neurologist(h), "Delay": track_delay(h)}
    df = pd.DataFrame(data=d)
    df['CT Scan Time'] = pd.to_datetime(df['CT Scan Time'])
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
    df['Thrombolysis Treatment Time'] = pd.to_datetime(df['Thrombolysis Treatment Time'])
    df["ICU Arrival Time"] = pd.to_datetime(df["ICU Arrival Time"])
    df["Neurologist Visit Time"] = pd.to_datetime(df["Neurologist Visit Time"])
    print(df.info())
    print(df.head())

    df.to_csv('~/Documents/NSERC/stroke_model_data.csv')


main()