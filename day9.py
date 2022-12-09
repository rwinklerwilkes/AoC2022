from aocd import get_data
import numpy as np

data = get_data(day=9, year=2022)
test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

class Board:
    def __init__(self):
        self.head_pos = np.array([0,0])
        self.tail_pos = np.array([0,0])
        self.distinct_positions = set()

    def process_moves(self, data):
        for inst in data.split('\n'):
            self.move(inst)

    def move(self, instruction):
        direction, distance = instruction.split(' ')
        distance = int(distance)
        for i in range(distance):
            match direction:
                case 'U':
                    self.head_pos[0] -= 1
                case 'R':
                    self.head_pos[1] += 1
                case 'D':
                    self.head_pos[0] += 1
                case 'L':
                    self.head_pos[1] -= 1
            self.move_tail()

    def move_tail(self):
        difference = self.head_pos-self.tail_pos
        adjusted_diff = np.clip(difference, -1, 1)
        distance = np.max(np.abs(difference))
        #same position
        if np.all(self.head_pos == self.tail_pos) or distance <= 1:
            #do nothing
            pass
        else:
            self.tail_pos += adjusted_diff

        self.distinct_positions.add(tuple(self.tail_pos))

class Board_Part_Two:
    def __init__(self):
        self.head_pos = np.array([0,0])
        self.knots = [np.array([0,0]) for i in range(9)]
        self.distinct_positions = set()

    def process_moves(self, data):
        for inst in data.split('\n'):
            self.move(inst)

    def move(self, instruction):
        direction, distance = instruction.split(' ')
        distance = int(distance)
        for i in range(distance):
            match direction:
                case 'U':
                    self.head_pos[0] -= 1
                case 'R':
                    self.head_pos[1] += 1
                case 'D':
                    self.head_pos[0] += 1
                case 'L':
                    self.head_pos[1] -= 1
            for i in range(9):
                self.move_knot(i)

    def move_knot(self, knot_to_move):
        if knot_to_move == 0:
            next_knot = self.head_pos
        else:
            next_knot = self.knots[knot_to_move-1]
        knot = self.knots[knot_to_move]
        difference = next_knot-knot
        adjusted_diff = np.clip(difference, -1, 1)
        distance = np.max(np.abs(difference))
        #same position
        if np.all(next_knot == knot) or distance <= 1:
            #do nothing
            pass
        else:
            self.knots[knot_to_move] += adjusted_diff

        if knot_to_move == 8:
            self.distinct_positions.add(tuple(self.knots[knot_to_move]))

def part_one(data):
    b = Board()
    b.process_moves(data)
    answer = len(b.distinct_positions)
    return answer

def part_two(data):
    b = Board_Part_Two()
    b.process_moves(data)
    answer = len(b.distinct_positions)
    return answer

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 13
part_one_answer = part_one(data)

test_data_p2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
test_part_two_answer = part_two(test_data_p2)
assert test_part_two_answer == 36
part_two_answer = part_two(data)