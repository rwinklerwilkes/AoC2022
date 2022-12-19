from aocd import get_data
import ast
import functools

data = get_data(day=13,year=2022)
test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

def parse_data(data):
    pairs = data.split('\n\n')
    all_pairs = [[ast.literal_eval(pairstr) for pairstr in row.split('\n')] for row in pairs]
    return all_pairs

def parse_data_part_two(data):
    strdata = data.replace('\n\n','\n')
    all_data = [ast.literal_eval(datastr) for datastr in strdata.split('\n')]
    all_data.append([[2]])
    all_data.append([[6]])
    return all_data

def comp(left, right):
    if isinstance(left, list) and isinstance(right, list):
        if not left and right:
            return -1
        elif left and not right:
            return 1
        elif not left and not right:
            return 0
        else:
            lc = left.copy()
            rc = right.copy()
            l = lc.pop(0)
            r = rc.pop(0)
            first = comp(l,r)
            if first == 0:
                #Keep going, first was equal
                return comp(lc, rc)
            else:
                return first
    elif isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left == right:
            #How do I handle stopping at 3 here: [1,1,3,1,1] <-> [1,1,5,1,1]
            return 0
        elif left > right:
            return 1
    else:
        if isinstance(left, int):
            return comp([left], right)
        else:
            return comp(left, [right])

def compare_p1(left, right):
    flag = comp(left, right)
    if flag in [0,-1]:
        return True
    else:
        return False

def part_one(data):
    pairs = parse_data(data)
    sum_correct = 0
    for i, pair in enumerate(pairs):
        left = pair[0]
        right = pair[1]
        sum_correct += compare_p1(left,right) * (i+1)
    return sum_correct

def part_two(data):
    parsed = parse_data_part_two(data)
    parsed.sort(key=functools.cmp_to_key(comp))
    decoder = (parsed.index([[2]])+1)*(parsed.index([[6]])+1)
    return decoder

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 13
part_one_answer = part_one(data)

test_part_two_answer = part_two(test_data)
assert test_part_two_answer == 140
part_two_answer = part_two(data)