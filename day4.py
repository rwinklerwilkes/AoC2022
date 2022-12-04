from aocd import get_data

data = get_data(day=4, year=2022)
test_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

def parse_data(data):
    parsed = [[[int(j) for j in i.split('-')] for i in row.split(',')] for row in data.split('\n')]
    return parsed

def find_overlap(first, second, part_two=True):
    first_range = set(list(range(first[0],first[1]+1)))
    second_range = set(list(range(second[0], second[1] + 1)))
    overlap = first_range.intersection(second_range)
    if not part_two:
        if overlap == first_range or overlap == second_range:
            ret_overlap = 1
        else:
            ret_overlap = 0
    else:
        ret_overlap = (len(overlap) >= 1)*1
    return ret_overlap

def part_one(data):
    parsed = parse_data(data)
    answer = 0
    for first,second in parsed:
        answer += find_overlap(first, second)
    return answer

def part_two(data):
    parsed = parse_data(data)
    answer = 0
    for first, second in parsed:
        answer += find_overlap(first, second, part_two=True)
    return answer

part_one_test = part_one(test_data)
assert part_one_test == 2
part_one_answer = part_one(data)

part_two_test = part_two(test_data)
assert part_two_test == 4
part_two_answer = part_two(data)