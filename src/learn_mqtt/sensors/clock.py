import pandas as pd


class GenericClock:

    def __init__(self):

        self.time_start = pd.Timestamp.now()

    @property
    def zone(self):
        return self._zone


if __name__ == "__main__":
    clock = GenericClock()
    print(clock.time)
