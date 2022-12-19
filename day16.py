from aocd import get_data
import re

data = get_data(day=16,year=2022)

test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

class Valve:
    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = set()

    def set_neighbor(self, other):
        self.neighbors.add(other)

def parse_line(line):
    re_str = r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnel[s]{0,1} lead[s]{0,1} to valve[s]{0,1} ([A-Z, ]+)'
    valve, flow, other_valves = re.match(re_str, line).groups()
    return valve, flow, other_valves

def parse_data(data):
    valves = {}
    neighbors = {}
    for line in data.split('\n'):
        valve, flow, other_valves = parse_line(line)
        v = Valve(name=valve, flow_rate=int(flow))
        valves[valve] = v
        neighbors[valve] = other_valves

    for v, n in neighbors.items():
        ns = n.split(', ')
        for ngh in ns:
            valves[v].set_neighbor(valves[ngh])

    return valves

v = parse_data(test_data)