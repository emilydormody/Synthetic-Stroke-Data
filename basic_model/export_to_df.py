
import pandas as pd


def export_to_pandas(model):

    df = pd.DataFrame(data=model.patient_info())
    df['CT Scan Time'] = pd.to_datetime(df['CT Scan Time'])
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
    df['Discharge Time'] = pd.to_datetime(df['Discharge Time'])
    df['TPA Treatment Time'] = pd.to_datetime(df['TPA Treatment Time'])
    df["ICU Arrival Time"] = pd.to_datetime(df["ICU Arrival Time"])
    df["ICU Checkout Time"] = pd.to_datetime(df["ICU Checkout Time"])
    df["Neurology Ward Arrival Time"] = pd.to_datetime(df["Neurology Ward Arrival Time"])
    df["Time of Stroke"] = pd.to_datetime(df["Time of Stroke"])
    df["ED Arrival Time"] = pd.to_datetime(df["ED Arrival Time"])
    df["Occupational Therapist Visit"] = pd.to_datetime(df["Occupational Therapist Visit"])
    df["Speech Pathologist Visit"] = pd.to_datetime(df["Speech Pathologist Visit"])
    df["Physiotherapist Visit"] = pd.to_datetime(df["Physiotherapist Visit"])
    df["Dietitian Visit"] = pd.to_datetime(df["Dietitian Visit"])
    df["Social Worker Visit"] = pd.to_datetime(df["Social Worker Visit"])
    df["Cardiologist Visit"] = pd.to_datetime(df["Cardiologist Visit"])
    df["Neurologist Visit"] = pd.to_datetime(df["Neurologist Visit"])
    print(df.info())
    print(df.head())
    print(df["Physiotherapist Visit"])

    #df.sort_values(by='Arrival Time').to_csv('~/Documents/NSERC/files/stroke_model_data.csv')
    #pd.DataFrame(data=model.ticks()).to_csv('~/Documents/NSERC/files/data_minutes.csv')
    pd.DataFrame(data=model.ticks()).to_csv('~/Downloads/data_minutes.csv')
    df.sort_values(by='Arrival Time').to_csv('~/Downloads/stroke_model_data.csv')