
import pandas as pd


def export_to_pandas(model):

    df = pd.DataFrame(data=model.patient_data.patient_info())
    df['CT Scan Time'] = pd.to_datetime(df['CT Scan Time'])
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
    df['TPA Treatment Time'] = pd.to_datetime(df['TPA Treatment Time'])
    df["ICU Arrival Time"] = pd.to_datetime(df["ICU Arrival Time"])
    df["Neurology Ward Arrival Time"] = pd.to_datetime(df["Neurology Ward Arrival Time"])
    df["Time of Stroke"] = pd.to_datetime(df["Time of Stroke"])
    df["Occupational Therapist Visit"] = pd.to_datetime(df["Occupational Therapist Visit"])
    df["Speech Pathologist Visit"] = pd.to_datetime(df["Speech Pathologist Visit"])
    df["Physiotherapist Visit"] = pd.to_datetime(df["Physiotherapist Visit"])
    df["Dietitian Visit"] = pd.to_datetime(df["Dietitian Visit"])
    df["Social Worker Visit"] = pd.to_datetime(df["Social Worker Visit"])
    df["Cardiologist Visit"] = pd.to_datetime(df["Cardiologist Visit"])
    df["Neurologist Visit"] = pd.to_datetime(df["Neurologist Visit"])
    df["Blood Work Time"] = pd.to_datetime(df["Blood Work Time"])
    print(df.info())
    print(df)

    df.sort_values(by='Arrival Time').to_csv('~/Downloads/stroke_model_data.csv')
