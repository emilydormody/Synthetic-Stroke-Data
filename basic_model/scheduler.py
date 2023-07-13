import random


class NeuroScheduler:
    def __init__(self, patient):
        self.times_lst = []
        self.next_time_name = None
        self.patent = patient

    def get_next_time(self, current):
        try:
            if len(self.times_lst) <= 0:
                return None
            # while self.times_lst[0][1] < current - 30:
            #     self.times_lst.pop(0)
            #     if len(self.times_lst) <= 0:
            #         return None
            self.next_time_name = self.times_lst[0][0]
            return self.times_lst[0][1]
        except IndexError:
            print(self.patent, current)

    def get_next_name(self):
        if self.next_time_name != self.times_lst[0][0]:
            self.next_time_name = None
        return self.next_time_name

    def add_value(self, value):
        if type(value) is tuple:
            self.times_lst.append(value)
            i = len(self.times_lst) - 2
            while self.times_lst[i][1] > value[1]:
                self.times_lst[i + 1] = self.times_lst[i]
                self.times_lst[i] = value
                i -= 1
                if i < 0:
                    return

    def filter_times(self):
        i = 0
        while i < len(self.times_lst) - 1:
            while self.times_lst[i][1] + 30 > self.times_lst[i + 1][1]:
                self.times_lst.remove(self.times_lst[i + 1])
                if i == len(self.times_lst) - 1:
                    break
            i += 1
        print(self.patent, self.times_lst)

    def drop_values(self, current):
        while self.times_lst[0][1] < current - 30:
            self.times_lst.pop(0)
            if len(self.times_lst) <= 0:
                return


s = NeuroScheduler(5)
s.add_value(('one', 10))
s.add_value(('six', 60))
s.add_value(('two', 20))
s.add_value(('eight', 30))
s.add_value(('three', 93))
s.add_value(('four', 97))
s.filter_times()
