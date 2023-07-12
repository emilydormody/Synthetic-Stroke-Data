import random


class Scheduler:
    def __init__(self):
        self.times_lst = []
        self.add_values()
        self.times_lst = insert_sort(self.times_lst)
        self.filter_times()
        self.next_time_name = None
        print(self.times_lst)

    def get_next_time(self, current):
        while self.times_lst[0] < current:
            self.times_lst.pop(0)
        self.next_time_name = self.times_lst[0][0]
        return self.times_lst[0][1]

    def get_next_name(self):
        if self.next_time_name != self.times_lst[0][0]:
            self.next_time_name = None
        return self.next_time_name

    def add_values(self):
        pass

    def filter_times(self):
        i = 0
        while i < len(self.times_lst)-1:
            while self.times_lst[i][1] + 30 > self.times_lst[i+1][1]:
                self.times_lst.remove(self.times_lst[i+1])
            i += 1


def insert_sort(lst):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j][1] > key[1]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst


s = Scheduler()
#s.add_values()
