from aocd import get_data

data = get_data(day=20, year=2022)
test_data = """1
2
-3
3
-2
0
4"""

class Mixer:
    def __init__(self, data):
        pd, idxs = self.parse_data(data)
        self.data = pd
        self.idxs = idxs
        self.idx_to_use = 0

    def parse_data(self, data):
        vals = [int(val) for i, val in enumerate(data.split('\n'))]
        idxs = [i for i, val in enumerate(data.split('\n'))]
        return vals, idxs

    def move_val(self, i):
        val = self.data.pop(i)
        idx = self.idxs.pop(i)
        new_pos = i + val
        #Shifted off to the left
        if new_pos == 0:
            self.data.append(val)
            self.idxs.append(idx)
        else:
            self.data.insert(new_pos % len(self.data), val)
            self.idxs.insert(new_pos % len(self.idxs), idx)
        return self.data

    def move_orig_idx(self, i):
        cur_index = self.idxs.index(i)
        self.move_val(cur_index)

    def part_one(self):
        answer = 0
        for i in range(len(self.data)):
            self.move_orig_idx(i)
        zidx = self.data.index(0)
        for i in range(1000,4000,1000):
            answer += self.data[(zidx+i)%len(self.data)]
        return answer

    def part_two(self):
        self.data = [i*811589153 for i in self.data]
        answer = 0
        for j in range(10):
            for i in range(len(self.data)):
                self.move_orig_idx(i)

        zidx = self.data.index(0)
        for i in range(1000,4000,1000):
            answer += self.data[(zidx+i)%len(self.data)]
        return answer

m = Mixer(test_data)
test_part_one_answer = m.part_one()

m = Mixer(data)
part_one_answer = m.part_one()

m = Mixer(test_data)
test_part_two_answer = m.part_two()

m = Mixer(data)
part_two_answer = m.part_two()