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
    def __init__(self, starting_items: list, operation: str, test: int, name: int,
                 part_one: bool=True):
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.true_monkey = None
        self.false_monkey = None
        self.inspect_count = 0
        self.name = name
        self.part_one = part_one
        self.all_divisors = 1

    def set_all_divisors(self, all_divisors):
        self.all_divisors = all_divisors

    def __repr__(self):
        return f'Monkey {self.name}: ' + ', '.join([str(s) for s in self.items])

    def exec_operation(self, val):
        return eval(self.operation.replace('old',str(val)))

    def set_test_targets(self, true_false, tf_monkey):
        if true_false:
            self.true_monkey = tf_monkey
        else:
            self.false_monkey = tf_monkey

    def apply_boredom(self, val):
        if self.part_one:
            bored = val//3
        else:
            bored = val%self.all_divisors
        return bored

    def inspect(self, item):
        worry = self.exec_operation(item)
        bored = self.apply_boredom(worry)
        pass_test = (bored % self.test) == 0
        if pass_test:
            self.true_monkey.items.append(bored)
        else:
            self.false_monkey.items.append(bored)
        self.inspect_count += 1

    def round(self):
        for i in range(len(self.items)):
            item = self.items.pop(0)
            self.inspect(item)

def parse_monkeys(data, part_one=True):
    monkeys = [monkey.split('\n') for monkey in data.split('\n\n')]
    parsed_monkeys = {}
    ops = []
    all_divisors = 1
    for m in monkeys:
        mn = int(re.match(r'Monkey ([0-9]+):', m[0]).group(1))
        msi = [int(i) for i in re.match(r'Starting items: ([0-9,\s]+)', m[1].strip()).group(1).split(',')]
        op_match = re.match('Operation: new = (old [-0-9+*/ a-z]+)', m[2].strip()).group(1)
        test = int(re.match(r'Test: divisible by ([0-9]+)', m[3].strip()).group(1))
        all_divisors *= test
        tm = int(re.match(r'If true: throw to monkey ([0-9]+)', m[4].strip()).group(1))
        fm = int(re.match(r'If false: throw to monkey ([0-9]+)', m[5].strip()).group(1))
        pm = Monkey(msi, op_match, test, mn, part_one=part_one)
        parsed_monkeys[mn] = pm
        ops.append([tm, fm])

    for i in range(len(ops)):
        tm = ops[i][0]
        fm = ops[i][1]
        parsed_monkeys[i].set_test_targets(True, parsed_monkeys[tm])
        parsed_monkeys[i].set_test_targets(False, parsed_monkeys[fm])
        parsed_monkeys[i].set_all_divisors(all_divisors)

    return parsed_monkeys

def run_round(monkeys:dict):
    for i in range(len(monkeys.keys())):
        mky = monkeys[i]
        mky.round()

def part_one(data):
    monkeys = parse_monkeys(data)
    for i in range(20):
        run_round(monkeys)
    inspect_count_all = [m.inspect_count for m in monkeys.values()]
    inspect_count_all = sorted(inspect_count_all,reverse=True)
    score = inspect_count_all[0]*inspect_count_all[1]
    return score

def part_two(data):
    monkeys = parse_monkeys(data, part_one=False)
    for i in range(10000):
        run_round(monkeys)
    inspect_count_all = [m.inspect_count for m in monkeys.values()]
    inspect_count_all = sorted(inspect_count_all, reverse=True)
    score = inspect_count_all[0]*inspect_count_all[1]
    return score


test_answer_part_one = part_one(test_data)
assert test_answer_part_one == 10605
answer_part_one = part_one(data)

test_answer_part_two = part_two(test_data)
assert test_answer_part_one == 2713310158
answer_part_two = part_two(data)