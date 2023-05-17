from hospital import Hospital
from pandas_data_export import *


def main():
    h = Hospital()
    for i in range(3180):  # 24 hours from last possible admission time
        h.step()

    export_to_pandas(h)


if __name__ == "__main__":
    main()
