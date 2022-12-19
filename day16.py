from aocd import get_data
import re
import networkx as nx

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

class State(object):
    def __init__(self, minute, position, opened, rate, total):
        self.minute = minute
        self.position = position
        self.opened = opened
        self.rate = rate
        self.total = total

    def __repr__(self):
        return "T%s @%s OP:%s r%d total: %d flow: %d" % (
        self.minute, self.position, self.opened, self.rate, self.total, self.flow())

    def flow(self, end=30):
        return self.total + (end - self.minute + 1) * self.rate


def parse_line(line):
    re_str = r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnel[s]{0,1} lead[s]{0,1} to valve[s]{0,1} ([A-Z, ]+)'
    valve, flow, other_valves = re.match(re_str, line).groups()
    return valve, flow, other_valves

def parse_data(data):
    G = nx.DiGraph()
    neighbors = {}
    for line in data.split('\n'):
        valve, flow, other_valves = parse_line(line)
        G.add_node(valve, flow=int(flow), worth_opening=(int(flow) > 0))
        neighbors[valve] = other_valves

    for v, n in neighbors.items():
        ns = n.split(', ')
        for ngh in ns:
            G.add_edge(v, ngh, weight=1)

    return G

def part_one(data):
    graph = parse_data(data)
    all_distances = nx.algorithms.floyd_warshall(graph)

    worthwhile_nodes = [i for i in graph.nodes if graph.nodes[i]['flow'] > 0]
    initial_state = State(1,'AA',[],0,0)
    max_flow = 0
    states = [initial_state]
    while states:
        state = states.pop()
        max_flow = max(max_flow, state.flow())
        valve = graph.nodes[state.position]
        if state.minute == 30:
            continue
        if state.position not in state.opened and valve['worth_opening']:
            new_state = State(state.minute + 1,
                              state.position,
                              state.opened.copy() + [state.position],
                              state.rate + valve['flow'],
                              state.total + state.rate
                              )
            states.append(new_state)
            #Open if we can, otherwise go to a new worthwhile node and open one of those instead
            continue

        for nd in worthwhile_nodes:
            if nd not in state.opened:
                distance = all_distances[state.position][nd]
                if state.minute + distance > 29:
                    continue
                states.append(State(state.minute + distance,
                                    nd,
                                    state.opened.copy(),
                                    state.rate,
                                    state.total + (state.rate*distance)))
    return max_flow

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 1651
part_one_answer = part_one(data)