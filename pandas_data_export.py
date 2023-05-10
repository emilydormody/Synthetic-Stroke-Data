from basic_model import *
import pandas as pd


def main():
    h = Hospital()
    for i in range(2880):  # 48 hours of steps
        h.step()

    d = {"Patient Id": patient_name(h), "Age": patient_age(h), "Gender": patient_gender(h), "Arrival Time": track_arrivals(h),
         "CT Scan Time": track_ctscans(h), "Thrombolysis Treatment Time": track_treatment(h),"ICU Arrival Time": track_icu_arrival(h),
         "Neurologist Visit Time": track_neurologist(h)}
    df = pd.DataFrame(data=d)
    print(df.head())


main()