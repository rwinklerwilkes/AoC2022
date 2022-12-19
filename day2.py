from aocd import get_data

data = get_data(day=2,year=2022)
test_data = """A Y
B X
C Z"""

def score_round(p1, p2):
    beats = {'rock':'scissors','paper':'rock','scissors':'paper'}
    points = {'rock':1,'paper':2,'scissors':3}
    p1_score = points[p1]
    p2_score = points[p2]
    if beats[p1] == p2:
        #player 1 beats player 2
        p1_score += 6
    elif beats[p2] == p1:
        #player 2 beats player 1
        p2_score += 6
    elif p1 == p2:
        p1_score += 3
        p2_score += 3
    return p1_score, p2_score


def run_round(p1, p2):
    options = ['rock','paper','scissors']
    p1_play = options[(ord(p1) - 65) % 23]
    p2_play = options[(ord(p2) - 65) % 23]
    p1_score, p2_score = score_round(p1_play, p2_play)
    return p1_score, p2_score

def run_round_part_two(p1, p2):
    options = ['rock','paper','scissors']
    p1_play = (ord(p1) - 65) % 23
    p2_play = (ord(p2) - 65) % 23
    if p2_play == 0:
        #lose
        p2_play = (p1_play - 1)%3
    elif p2_play == 1:
        #tie
        p2_play = p1_play
    else:
        #win
        p2_play = (p1_play + 1)%3

    p1_play = options[p1_play]
    p2_play = options[p2_play]
    p1_score, p2_score = score_round(p1_play, p2_play)
    return p1_score, p2_score

def parse_data(data):
    return [sp.split(' ') for sp in data.split('\n')]

def run_game(data, part_two=False):
    p1_total = 0
    p2_total = 0
    for row in data:
        if not part_two:
            p1, p2 = run_round(row[0], row[1])
        else:
            p1, p2 = run_round_part_two(row[0], row[1])
        p1_total += p1
        p2_total += p2
    return p1_total, p2_total

def part_one(data):
    parsed_data = parse_data(data)
    p1_total, p2_total = run_game(parsed_data)
    return p1_total, p2_total

def part_two(data):
    parsed_data = parse_data(data)
    p1_total, p2_total = run_game(parsed_data,part_two=True)
    return p1_total, p2_total

p1_p1, p1_p2 = part_one(data)
p2_p1, p2_p2 = part_two(data)