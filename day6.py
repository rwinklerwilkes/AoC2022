from aocd import get_data

data = get_data(day=6,year=2022)
test_data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'

def find_marker(data, length_to_search=4):
    first_marker = 0
    for i in range(len(data)):
        j = i+length_to_search
        if len(set(data[i:j])) == length_to_search:
            first_marker = j
            break

    return first_marker

part_one_test = find_marker(test_data)
assert part_one_test == 7
part_one_answer = find_marker(data)

part_two_test = find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14)
assert part_two_test == 29
part_two_answer = find_marker(data, 14)