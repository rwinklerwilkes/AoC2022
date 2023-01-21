from aocd import get_data
import re
from collections import deque

data = get_data(day=19, year=2022)
test_data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

def parse_blueprint(blueprint, time_left=24):
    blueprint_regex = r'Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.'
    bp, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = [int(i) for i in re.match(blueprint_regex, blueprint).groups()]
    return bp, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost, time_left

def parse_input(data, time_left=24):
    return [parse_blueprint(blueprint,time_left) for blueprint in data.split('\n')]

def solve(blueprint, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost, time):
    best = 0
    # state is (ore, clay, obsidian, geodes, num_ore, num_clay, num_obsidian, num_geode, time)
    state = (0, 0, 0, 0, 1, 0, 0, 0, time)
    q = deque([state])
    visited = set()
    while q:
        cur_state = q.popleft()
        ore, clay, obsidian, geodes, num_ore, num_clay, num_obsidian, num_geode, time_left = cur_state
        best = max(best, geodes)
        if time_left <= 0:
            continue

        highest_ore_cost = max(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)

        #Some scrapping heuristics here - don't keep more robots on hand than you can spend per turn
        if num_ore >= highest_ore_cost:
            num_ore = highest_ore_cost
        if num_clay >= obsidian_clay_cost:
            num_clay = obsidian_clay_cost
        if num_obsidian >= geode_obsidian_cost:
            num_obsidian = geode_obsidian_cost

        #More ore than we could spend with the remaining time
        if ore >= time_left*highest_ore_cost-num_ore*(time_left-1):
            ore = time_left*highest_ore_cost-num_ore*(time_left-1)
        #Same with clay and obsidian
        if clay >= time_left*obsidian_clay_cost-num_clay*(time_left-1):
            clay = time_left*obsidian_clay_cost-num_clay*(time_left-1)
        if obsidian >= time_left * geode_obsidian_cost - num_obsidian * (time_left - 1):
            obsidian = time_left * geode_obsidian_cost - num_obsidian * (time_left - 1)

        cur_state = (ore, clay, obsidian, geodes, num_ore, num_clay, num_obsidian, num_geode, time_left)
        if cur_state in visited:
            continue
        visited.add(cur_state)
        next_state = (ore + num_ore, clay + num_clay, obsidian + num_obsidian, geodes + num_geode,
                      num_ore, num_clay, num_obsidian,num_geode, time_left - 1)
        q.append(next_state)
        #Create states for each possible robot we could buy
        if ore >= ore_ore_cost:
            next_state = (ore -ore_ore_cost + num_ore, clay + num_clay, obsidian + num_obsidian, geodes + num_geode,
                          num_ore+1, num_clay, num_obsidian, num_geode, time_left - 1)
            q.append(next_state)
        if ore >= clay_ore_cost:
            next_state = (ore - clay_ore_cost + num_ore, clay + num_clay, obsidian + num_obsidian, geodes + num_geode,
                          num_ore, num_clay+1, num_obsidian, num_geode, time_left - 1)
            q.append(next_state)
        if ore >= obsidian_ore_cost and clay >= obsidian_clay_cost:
            next_state = (ore - obsidian_ore_cost + num_ore, clay - obsidian_clay_cost + num_clay,
                          obsidian + num_obsidian, geodes + num_geode,
                          num_ore, num_clay, num_obsidian + 1, num_geode, time_left - 1)
            q.append(next_state)
        if ore >= geode_ore_cost and obsidian >= geode_obsidian_cost:
            next_state = (ore - geode_ore_cost + num_ore, clay + num_clay,
                          obsidian - geode_obsidian_cost + num_obsidian, geodes + num_geode,
                          num_ore, num_clay, num_obsidian, num_geode + 1, time_left - 1)
            q.append(next_state)
    return best*blueprint

def part_one(data):
    bp_all = parse_input(data)
    answer = 0
    for blueprint in bp_all:
        component = solve(*blueprint)
        answer += component

    return answer

def part_two(data):
    bp_all = parse_input(data, time_left=32)
    bp_all = bp_all[:3]
    answer = 1
    for blueprint in bp_all:
        component = solve(*blueprint)/blueprint[0]
        print(component)
        answer *= component

    return answer

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 33
part_one_answer = part_one(data)

test_part_two_answer = part_two(test_data)
part_two_answer = part_two(data)