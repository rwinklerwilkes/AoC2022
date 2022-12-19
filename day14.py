import numpy as np
from aocd import get_data

data = get_data(day=14,year=2022)
test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

class Map:
    def __init__(self, part_one = True):
        self.filled_spots = set()
        self.SAND_START = (0,500)
        self.sand_spots = set()
        self.at_max = False
        self.part_one = part_one
        self.min_row = None
        self.row_range = None
        self.min_col = None
        self.col_range = None

    def determine_ranges(self):
        if not self.min_row:
            all_row = [i[0] for i in self.filled_spots]
            self.min_row = min(all_row)
            max_row = max(all_row)
            all_col = [i[1] for i in self.filled_spots]
            self.min_col = min(all_col)
            max_col = max(all_col)
            self.row_range = max_row - self.min_row
            self.col_range = max_col - self.min_col
        return self.min_row, self.row_range, self.min_col, self.col_range

    def draw_map(self):
        min_row, row_range, min_col, col_range = self.determine_ranges()
        #Add some extra to be safe
        board = np.zeros((row_range+10, col_range+10))
        spots = [[(i[0]-min_row, i[1]-min_col),i] for i in self.filled_spots]
        for s, os in spots:
            if os in self.sand_spots:
                board[s] = 9
            else:
                board[s] = 1
        return board

    def parse_line(self, line):
        pointstr = line.split(' -> ')
        points = [[int(i) for i in point.split(',')] for point in pointstr]
        for i in range(len(points)-1):
            start,end = points[i:i+2]
            self.map_pair(start, end)

    def map_pair(self, start, end):
        sc, sr = start
        ec, er = end
        if sc != ec:
            step = int((ec-sc)/abs((ec-sc)))
            for i in range(sc, ec+step, step):
                self.filled_spots.add((sr,i))
        elif sr != er:
            step = int((er-sr)/abs((er-sr)))
            for i in range(sr, er+step, step):
                self.filled_spots.add((i, sc))

    def parse_data(self, data):
        lines = data.split('\n')
        for line in lines:
            self.parse_line(line)

        _,_,_,_ = self.determine_ranges()

    def fall_sand(self):
        sand_pos = self.SAND_START
        at_rest = False

        min_row, row_range, min_col, col_range = self.determine_ranges()
        max_row = min_row + row_range
        while not at_rest and not self.at_max:
            next_row = sand_pos[0]+1
            left = (next_row, sand_pos[1] - 1)
            right = (next_row, sand_pos[1] + 1)
            down = (next_row, sand_pos[1])
            check_left = left in self.filled_spots or (not self.part_one and next_row >= max_row + 2)
            check_right = right in self.filled_spots or (not self.part_one and next_row >= max_row + 2)
            check_down = down in self.filled_spots or (not self.part_one and next_row >= max_row + 2)
            if not check_down:
                sand_pos = down
            elif not check_left:
                #Move left
                sand_pos = left
            elif not check_right:
                sand_pos = right
            else:
                self.filled_spots.add(sand_pos)
                self.sand_spots.add(sand_pos)
                at_rest = True
            if self.part_one:
                void_check = sand_pos[0] > max_row
            else:
                void_check = self.SAND_START in self.sand_spots
            if void_check:
                self.at_max = True

def part_one(data):
    m = Map()
    m.parse_data(data)

    while not m.at_max:
        m.fall_sand()

    answer = len(m.sand_spots)
    return answer

def part_two(data):
    m = Map(part_one=False)
    m.parse_data(data)

    while not m.at_max:
        m.fall_sand()

    answer = len(m.sand_spots)
    return m, answer

# test_part_one_answer = part_one(test_data)
# assert test_part_one_answer == 24
# part_one_answer = part_one(data)

_, test_part_two_answer = part_two(test_data)
assert test_part_two_answer == 93
_, part_two_answer = part_two(data)
