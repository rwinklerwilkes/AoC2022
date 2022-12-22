from aocd import get_data
import re

data = get_data(day=21, year=2022)
test_data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

class Monkey:
    def __init__(self, left, op=None, right=None):
        if left and not right:
            self.value = complex(left)
            self.left = None
            self.right = None
            self.op = None
        else:
            self.value = None
            self.left = left
            self.op = op
            self.right = right

    def get_value(self):
        if self.value:
            return self.value
        else:
            left = self.left.get_value()
            right = self.right.get_value()
            self.value = eval(f'{left} {self.op} {right}')
            return self.value

def parse_line(line):
    monkey, rest = line.split(': ')
    reg = r'([a-z]+) ([\+\/\-\*]) ([a-z]+)'
    m = re.match(reg, rest)
    if m:
        left, symbol, right = m.groups()
    else:
        left = rest
        symbol = None
        right = None
    return monkey, left, symbol, right

def parse_monkeys(data, part_one=True):
    all_monkeys = {}
    for line in data.split('\n'):
        monkey, left, symbol, right = parse_line(line)
        if monkey == 'root' and not part_one:
            symbol = '=='
        if monkey == 'humn' and not part_one:
            left = 1j
        m = Monkey(left, symbol, right)
        all_monkeys[monkey] = m

    for name, monkey_obj in all_monkeys.items():
        if monkey_obj.left in all_monkeys:
            monkey_obj.left = all_monkeys[monkey_obj.left]
        if monkey_obj.right in all_monkeys:
            monkey_obj.right = all_monkeys[monkey_obj.right]
    return all_monkeys


def part_one(data):
    am = parse_monkeys(data)
    answer = am['root'].get_value()
    return answer

def part_two(data):
    am = parse_monkeys(data, part_one=False)
    l = am['root'].left.get_value()
    r = am['root'].right.get_value()
    if r.imag:
        l, r = r, l
    answer = round(((r-l.real)/l.imag).real)
    return answer

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 152
part_one_answer = part_one(data)

test_part_two_answer = part_two(test_data)
assert test_part_two_answer == 301
part_two_answer = part_two(data)