from aocd import get_data

data = get_data(day=17, year=2022)
test_data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

def parse_data(data):
    return data.split('')

class Cavern:
    SHAPES = "####",".#.\n###\n.#.","..#\n..#\n###","#\n#\n#\n#","##\n##"
    def __init__(self, jet_shape):
        self.jet_shape = jet_shape
        self.jet_pos = 0

