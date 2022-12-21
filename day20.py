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
        pd = self.parse_data(data)
        self.data = pd

    def parse_data(self, data):
        return [(i,int(val)) for i, val in enumerate(data.split('\n'))]

    def move_val(self, i):
        orig_idx, val = self.data.pop(i)
        new_pos = i + val
        self.data.insert(new_pos%len(self.data), (orig_idx,val))
        return self.data

    def move_orig_idx(self, i):
        pass

    def part_one(self):
        pass

m = Mixer(test_data)

m.move_val(0)