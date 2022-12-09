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


def part_one(data):
    b = Board()
    b.process_moves(data)
    answer = len(b.distinct_positions)
    return answer

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 13
part_one_answer = part_one(data)