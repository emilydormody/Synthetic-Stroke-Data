from hospital import Hospital
from export_to_df import *


def main():
    h = Hospital()
    for i in range(10000):
        h.step()

    export_to_pandas(h)


if __name__ == "__main__":
    main()
