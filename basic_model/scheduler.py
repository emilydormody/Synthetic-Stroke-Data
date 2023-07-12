import random


class NeuroScheduler:
    def __init__(self):
        self.times_lst = []
        self.next_time_name = None

    def get_next_time(self, current):
        while self.times_lst[0] < current:
            self.times_lst.pop(0)
        self.next_time_name = self.times_lst[0][0]
        return self.times_lst[0][1]

    def get_next_name(self):
        if self.next_time_name != self.times_lst[0][0]:
            self.next_time_name = None
        return self.next_time_name

    def add_value(self, value):
        if type(value) is tuple:
            self.times_lst.append(value)
            i = len(self.times_lst)-2
            while self.times_lst[i][1] > value[1]:
                self.times_lst[i+1] = self.times_lst[i]
                self.times_lst[i] = value
                i -= 1
                if i < 0:
                    return

    def filter_times(self):
        i = 0
        while i < len(self.times_lst)-1:
            while self.times_lst[i][1] + 30 > self.times_lst[i+1][1]:
                self.times_lst.remove(self.times_lst[i+1])
            i += 1
        print(self.times_lst)




s = Scheduler()
s.add_value(('one',1))
s.add_value(('six', 6))
s.add_value(('two', 2))
s.add_value(('eight', 8))
s.add_value(('three', 3))
s.add_value(('four', 4))
