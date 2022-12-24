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
        while moving:
            shape_to_use = self.push(shape_to_use)
            shape_to_use = self.move_down(shape_to_use)
            if self.all_shapes.intersection(shape_to_use):
                shape_to_use = self.move_up(shape_to_use)
                self.all_shapes = self.all_shapes.union(shape_to_use)
                moving = False
        self.top = max([y for x,y in self.all_shapes]) + 4
        return shape_to_use

    def part_one(self):
        for i in range(2022):
            shape_to_use = self.drop_rock()
        return self.top - 4

test = Cavern(test_data)
test_part_one_answer = test.part_one()
actual = Cavern(data)
part_one_answer = actual.part_one()