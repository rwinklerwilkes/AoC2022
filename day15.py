from aocd import get_data
import re

data = get_data(day=15,year=2022)
test_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

def parse_line(line):

    line_regex = r'Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)'
    m = re.match(line_regex, line)
    sx, sy, bx, by = [int(i) for i in m.groups()]
    return (sx, sy), (bx, by)

def pl(line):

    line_regex = r'Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)'
    m = re.match(line_regex, line)
    sx, sy, bx, by = [int(i) for i in m.groups()]
    return (sx, sy, bx, by)

def parse_data(data):
    points = [parse_line(line) for line in data.split('\n')]
    return points

def taxicab_distance(s, b):
    return abs(s[0]-b[0]) + abs(s[1]-b[1])

def in_radius(s, b, point):
    radius = taxicab_distance(s,b)
    check_distance = taxicab_distance(s, point)
    if check_distance <= radius:
        return True
    else:
        return False

def get_all_radii(points):
    return [(p[0], taxicab_distance(p[0],p[1])) for p in points]

def get_ranges(radii):
    checks = [(p[0][0]-p[1],p[0][0]+p[1],p[0][1]-p[1], p[0][1]+p[1]) for p in radii]
    mnc = min([p[0] for p in checks])
    mxc = max([p[0] for p in checks])
    mnr = min([p[1] for p in checks])
    mxr = max([p[1] for p in checks])
    return mnc, mxc, mnr, mxr

def check_row_coverage(row_number, points, radii):
    intervals_covered = []
    for point, radius in radii:
        x, y = point
        diff = abs(y-row_number)
        remaining = radius - diff
        if remaining >= 0:
            intervals_covered.append((x-remaining,x+remaining))

    x_covered = set.union(*[set(range(a,b+1)) for a,b in intervals_covered])
    has_beacon = {point[1][0] for point in points if point[1][1] == row_number}
    covered_points = x_covered - has_beacon
    return covered_points

def check_point(radii, point):
    #Checks if a point is contained within any radius of a sensor
    for sensor, radius in radii:
        if taxicab_distance(sensor, point) <= radius:
            return True
    return False

def check_outsides(radii, search_size):
    for point, radius in radii:
        px, py = point
        for xdiff in [-1,1]:
            for ydiff in [-1,1]:
                for dx in range(0,radius+2):
                    #Still has to be the same distance, i.e. abs(dx - bx) + abs(dy - by) <= radius + 1
                    dy = radius + 1 - dx
                    newx = px + dx * xdiff
                    newy = py + dy * ydiff
                    if newx < 0 or newy < 0 or newx > search_size or newy > search_size:
                        continue
                    else:
                        check = check_point(radii, (newx, newy))
                        if not check:
                            return newx*4000000+newy


def part_one(data, row_number):
    points = parse_data(data)
    radii = get_all_radii(points)
    cvg = check_row_coverage(row_number, points, radii)

    return len(cvg)

def part_two(data, search_size):
    points = parse_data(data)
    radii = get_all_radii(points)
    answer = check_outsides(radii, search_size)
    return answer


test_part_one_answer = part_one(test_data, 10)
assert test_part_one_answer == 26
part_one_answer = part_one(data, 2000000)

test_part_two_answer = part_two(test_data, 20)
assert test_part_two_answer == 56000011
part_two_answer = part_two(data, 4000000)