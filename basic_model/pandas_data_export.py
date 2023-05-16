from hospital import Hospital
from patient_and_patientdata import Patient
import pandas as pd


def main():
    h = Hospital()
    for i in range(2880):  # 48 hours of steps
        h.step()

    df = pd.DataFrame(data=h.patient_data.patient_info())
    df['CT Scan Time'] = pd.to_datetime(df['CT Scan Time'])
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
    df['Thrombolysis Treatment Time'] = pd.to_datetime(df['Thrombolysis Treatment Time'])
    df["ICU Arrival Time"] = pd.to_datetime(df["ICU Arrival Time"])
    df["Neurologist Visit Time"] = pd.to_datetime(df["Neurologist Visit Time"])
    print(df.info())
    print(df.head())

    # df.sort_values(by='Arrival Time').to_csv('~/Documents/NSERC/stroke_model_data.csv')


main()