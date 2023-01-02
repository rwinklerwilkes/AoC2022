from aocd import get_data
import numpy as np

data = get_data(day=17, year=2022)
test_data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


def parse_data(data):
    return data.split('')


class Cavern:
    def __init__(self, jet_shape):
        self.jet_shape = jet_shape
        self.jet_pos = 0
        self.cur_shape = 0
        self.set_shapes()
        self.top = 4
        self.all_shapes = {(x,0) for x in range(7)}
        #NOTE - this needs to be longer than the length of the cycle so you may need to update when rerunning
        self.RECENT_SHAPES_TO_KEEP = 1700
        self.recent_shapes = []
        self.recent_heights = []
        self.states = {}

    def draw(self):
        x_shape = 7
        y_shape = max([y for x,y in self.all_shapes]) + 1
        board = [['_' for x in range(x_shape)] for y in range(y_shape)]
        for yr in range(len(board)):
            for xr in range(len(board[yr])):
                if yr == 0:
                    board[yr][xr] = '-'
                elif (xr, yr) in self.all_shapes:
                    board[yr][xr] = '+'
        board_draw = '\n'.join([''.join(row) for row in reversed(board)])
        print(board_draw)
        return board_draw


    def set_shapes(self):
        shapes = [[(2, 0), (3, 0), (4, 0), (5, 0)],
                  [(3, 2), (2, 1), (3, 1), (4, 1), (3, 0)],
                  [(4, 2), (4, 1), (2, 0), (3, 0), (4, 0)],
                  [(2, 3), (2, 2), (2, 1), (2, 0)],
                  [(2, 1), (3, 1), (2, 0), (3, 0)]]
        self.shapes = [set(s) for s in shapes]

    def get_shape(self, y):
        self.recent_shapes.append(self.cur_shape)
        self.recent_shapes = self.recent_shapes[-self.RECENT_SHAPES_TO_KEEP:]
        shape_to_use = self.shapes[self.cur_shape]
        self.cur_shape += 1
        self.cur_shape %= len(self.shapes)
        return {(x, ys + y) for x, ys in shape_to_use}

    def move_left(self, shape):
        if any([x==0 for x,_ in shape]):
            return shape
        else:
            return {(x - 1, y) for x, y in shape}

    def move_right(self, shape):
        if any([x == 6 for x, _ in shape]):
            return shape
        else:
            return {(x + 1, y) for x, y in shape}

    def move_down(self, shape):
        return {(x, y-1) for x, y in shape}

    def move_up(self, shape):
        return {(x, y + 1) for x, y in shape}

    def push(self, shape):
        dir = self.jet_shape[self.jet_pos]
        if dir == '<':
            moved_shape = self.move_left(shape)
            if moved_shape.intersection(self.all_shapes):
                moved_shape = shape
        elif dir == '>':
            moved_shape = self.move_right(shape)
            if moved_shape.intersection(self.all_shapes):
                moved_shape = shape
        else:
            assert False
        self.jet_pos += 1
        self.jet_pos %= len(self.jet_shape)
        return moved_shape

    def drop_rock(self):
        shape_to_use = self.get_shape(self.top)
        moving = True
        last_top = self.top - 4
        while moving:
            shape_to_use = self.push(shape_to_use)
            shape_to_use = self.move_down(shape_to_use)
            if self.all_shapes.intersection(shape_to_use):
                shape_to_use = self.move_up(shape_to_use)
                self.all_shapes = self.all_shapes.union(shape_to_use)
                moving = False
        this_top = max([y for x,y in self.all_shapes])
        self.recent_heights.append(this_top - last_top)
        self.recent_heights = self.recent_heights[-self.RECENT_SHAPES_TO_KEEP:]
        self.top = this_top + 4
        return shape_to_use

    def find_cycle(self):
        for i in range(4000):
            shape_to_use = self.drop_rock()
            state = (self.jet_pos, self.cur_shape, tuple(self.recent_shapes), tuple(self.recent_heights))
            if state in self.states:
                #cycle found
                last_height = self.states[state][0]
                last_i = self.states[state][1]
                height_diff = self.top - 4 - last_height
                i_diff = i - last_i
                return state, last_i, last_height, height_diff, i_diff
            else:
                self.states[state] = (self.top - 4, i)
        return None, None, None

    def run_from_cycle(self, cycle_start, cycle_diff, cycle_end, height_start, height_diff):
        number_of_cycles = (cycle_end - cycle_start) // cycle_diff
        i_before_end = cycle_start + cycle_diff * number_of_cycles
        height_before_end = height_start + height_diff * number_of_cycles
        return i_before_end, height_before_end

    def find_end_height(self, i_before_end, height_before_end, desired_i, state_to_run):
        pass

    def part_one(self):
        for i in range(2022):
            shape_to_use = self.drop_rock()
        return self.top - 4

    def part_two(self):
        desired_height = 1000000000000
        state, last_i, last_height, height_diff, i_diff = self.find_cycle()
        i_before_end, height_before_end = self.run_from_cycle(last_i, i_diff, desired_height, last_height, height_diff)
        height_diffs = state[3][-i_diff:]
        remaining_height = sum(height_diffs[:desired_height - i_before_end - 1])
        total_height = height_before_end + remaining_height
        return total_height

test = Cavern(test_data)
test_part_one_answer = test.part_one()
actual = Cavern(data)
part_one_answer = actual.part_one()

test = Cavern(test_data)
test_part_two_answer = test.part_two()

actual = Cavern(data)
part_two_answer = actual.part_two()