from hospital import Hospital
from export_to_df import *
from values import NUM_TICKS
def main():
    h = Hospital()
    for i in range(NUM_TICKS):
        h.step()

    export_to_pandas(h)


if __name__ == "__main__":
    main()


