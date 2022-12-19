from aocd import get_data
import re

data = get_data(day=5,year=2022)
test_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        if isinstance(item, list):
            self.stack += item
        else:
            self.stack.append(item)

    def pop(self, n=1):
        if n == 1:
            item = self.stack.pop()
        else:
            stk = self.stack.copy()
            item = stk[-n:]
            self.stack = stk[:-n]
        return item

    def reverse(self):
        self.stack.reverse()

    def peek(self):
        return self.stack[-1]

    def __repr__(self):
        actual_stacked = self.stack.copy()
        actual_stacked.reverse()
        return '\n'.join(actual_stacked)

def parse_data(data):
    stack_string, inst_string = data.split('\n\n')
    stacks = parse_stacks(stack_string)
    instructions = parse_instructions(inst_string)
    return stacks, instructions

def parse_stacks(stack_string):
    sp = stack_string.split('\n')
    unparsed_initial_state = sp[:-1]
    number_of_stacks = max([int(i) for i in sp[-1].split(' ') if i != ''])
    parsed_stacks = [Stack() for i in range(number_of_stacks)]
    for row in unparsed_initial_state:
        for i in range(number_of_stacks):
            start = 4*i
            end = start + 3
            box = row[start+1:end-1]
            if box != ' ':
                parsed_stacks[i].push(box)

    for p in parsed_stacks:
        p.reverse()
    return parsed_stacks


def parse_instructions(inst_string):
    move_matcher = r'move ([0-9]{1,}) from ([0-9]{1,}) to ([0-9]{1,})'
    parsed_instructions = []
    for row in inst_string.split('\n'):
        m = re.match(move_matcher, row)
        parsed_instructions.append([int(i) for i in [m.group(1),m.group(2),m.group(3)]])
    return parsed_instructions

def part_one(data):
    stacks, instructions = parse_data(data)
    for number, from_stack, to_stack in instructions:
        #Off by one compared to list
        fs = from_stack - 1
        ts = to_stack - 1
        for i in range(number):
            box = stacks[fs].pop()
            stacks[ts].push(box)
    answer = ''.join([s.peek() for s in stacks])
    return answer

def part_two(data):
    stacks, instructions = parse_data(data)
    for number, from_stack, to_stack in instructions:
        #Off by one compared to list
        fs = from_stack - 1
        ts = to_stack - 1
        box = stacks[fs].pop(number)
        stacks[ts].push(box)
    answer = ''.join([s.peek() for s in stacks])
    return answer

test_answer = part_one(test_data)
assert test_answer == 'CMZ'
part_one_answer = part_one(data)
print(part_one_answer)

test_answer = part_two(test_data)
assert test_answer == 'MCD'
part_two_answer = part_two(data)
print(part_two_answer)