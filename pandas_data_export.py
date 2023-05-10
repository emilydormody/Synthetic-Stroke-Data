from basic_model import *
import pandas as pd


def main():
    h = Hospital()
    for i in range(2880):  # 48 hours of steps
        h.step()

    d = {"Arrival Time": track_arrivals(h), "ICU Arrival Time": track_icu_arrival(h)}
    df = pd.DataFrame(data=d)
    print(df.head())


main()