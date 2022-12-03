from aocd import get_data
from functools import reduce

data = get_data(day=3, year=2022)
test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

def parse_rucksack(ruck_str):
    sz = len(ruck_str)//2
    first_part = set(ruck_str[:sz])
    second_part = set(ruck_str[sz:])
    return first_part, second_part

def score_priority(common_item):
    priority = {chr(i+97):i+1 for i in range(26)}
    priority.update({chr(i + 65): i + 27 for i in range(26)})
    return priority[common_item]

def find_priority(ruck_str):
    first_part, second_part = parse_rucksack(ruck_str)
    common = list(first_part.intersection(second_part))[0]
    priority_val = score_priority(common)
    return priority_val

def part_one(data):
    answer = 0
    for row in data.split('\n'):
        answer += find_priority(row)
    return answer

def part_two(data):
    row_data = data.split('\n')
    groups_of_three = len(row_data)//3
    answer = 0
    for i in range(groups_of_three):
        rucks = [set(row) for row in row_data[3*i:3*(i+1)]]
        common = reduce(lambda x,y: x.intersection(y), rucks)
        score = score_priority(list(common)[0])
        answer += score
    return answer


test_answer = part_one(test_data)
assert test_answer == 157
part_one_answer = part_one(data)

test_answer = part_two(test_data)
assert test_answer == 70
part_two_answer = part_two(data)