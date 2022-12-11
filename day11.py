from typing import Callable
import re
from aocd import get_data

data = get_data(day=11, year=2022)
test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

class Monkey:
    def __init__(self, starting_items: list, operation: Callable[[int], int], test: int):
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.true_monkey = None
        self.false_monkey = None
        self.inspect_count = 0

    def set_test_targets(self, true_false, tf_monkey):
        if true_false:
            self.true_monkey = tf_monkey
        else:
            self.false_monkey = tf_monkey

    def inspect(self, item):
        worry = self.operation(item)
        bored = round(worry/3, 0)
        pass_test = (bored % self.test) == 0
        if pass_test:
            self.true_monkey.append(item)
        else:
            self.false_monkey.append(item)
        self.inspect_count += 1

    def round(self):
        for i in range(len(self.items)):
            item = self.items.pop(0)
            self.inspect(item)

def parse_monkeys(data):
    monkeys = [monkey.split('\n') for monkey in data.split('\n\n')]
    parsed_monkeys = {}
    ops = []
    for m in monkeys:
        mn = int(re.match(r'Monkey ([0-9]+):', m[0]).group(1))
        msi = [int(i) for i in re.match(r'Starting items: ([0-9,\s]+)', m[1].strip()).group(1).split(',')]
        op = lambda old: eval(re.match('Operation: new = (old [0-9+\-*/\s])', m[2].strip()).group(1)) #Operation: new = old + 6
        test = int(re.match(r'Test: divisible by ([0-9]+)', m[3].strip()).group(1))
        tm = int(re.match(r'If true: throw to monkey ([0-9]+)', m[4].strip()).group(1))
        fm = int(re.match(r'If false: throw to monkey ([0-9]+)', m[5].strip()).group(1))
        pm = Monkey(msi, op, test)
        parsed_monkeys[mn] = pm
        ops.append([tm, fm])

    for i in range(len(ops)):
        tm = ops[i][0]
        fm = ops[i][1]
        parsed_monkeys[i].set_test_targets(True,tm)
        parsed_monkeys[i].set_test_targets(False, fm)

    return parsed_monkeys

test_monkeys = parse_monkeys(test_data)
test_monkeys[0].operation(79)