from aocd import get_data
import re
from collections import deque

data = get_data(day=19, year=2022)
test_data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

def parse_blueprint(blueprint):
    blueprint_regex = r'Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.'
    bp, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = [int(i) for i in re.match(blueprint_regex, blueprint).groups()]
    return bp, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost

def parse_input(data):
    return [parse_blueprint(blueprint) for blueprint in data.split('\n')]

def solve(ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost, time):
    best = 0
    # state is (ore, clay, obsidian, geodes, num_ore, num_clay, num_obsidian, num_geode, time)
    state = (0, 0, 0, 0, 1, 0, 0, 0, time)
    q = deque(state)
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



bp_all = parse_input(test_data)