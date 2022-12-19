from aocd import get_data
import numpy as np

data = get_data(day=1,year=2022)
test_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

def parse_data(data):
    elves = data.split('\n\n')
    each_elf = [[int(i) for i in elf.split('\n')] for elf in elves]
    return each_elf

def elf_sum(elves,n=1):
    sums = np.array([sum(i) for i in elves])
    max_val = np.argsort(-1*sums)
    return sums[max_val[0:n]]

def part_one(data):
    parsed_data = parse_data(data)
    max_val = elf_sum(parsed_data)
    return max_val

def part_two(data):
    parsed_data = parse_data(data)
    max_val = elf_sum(parsed_data,n=3)
    return sum(max_val)

test_elves = parse_data(test_data)
test_max = elf_sum(test_elves)

part_one_answer = part_one(data)
part_two_answer = part_two(data)