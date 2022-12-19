import numpy as np
import networkx as nx
from aocd import get_data

data = get_data(day=12,year=2022)
test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

def parse_data(data):
    elevation = np.array([[ord(c) for c in row] for row in data.split('\n')])
    start = np.where(elevation == 83)
    end = np.where(elevation == 69)
    elevation -= 97
    elevation[start] = 0
    elevation[end] = 25
    return elevation, start, end

def find_neighbors(array, location):
    row = location[0]
    col = location[1]
    neighbors = [(row-1, col),
                 (row+1, col),
                 (row, col-1),
                 (row, col+1)]
    if row == 0:
        neighbors.remove((row-1,col))
    elif row == array.shape[0]-1:
        neighbors.remove((row+1,col))
    if col == 0:
        neighbors.remove((row,col-1))
    elif col == array.shape[1]-1:
        neighbors.remove((row,col+1))
    return neighbors


def dijkstra(elevation_graph, start, end):
    dist = np.full(elevation_graph.shape, np.inf)
    prev = {}
    q = []
    for i in range(elevation_graph.shape[0]):
        for j in range(elevation_graph.shape[1]):
            q.append((i,j))
    dist[start] = 0
    while q:
        q = sorted(q, key=lambda x: dist[x])
        cur_loc = q.pop(0)

        neighbors = find_neighbors(elevation_graph, cur_loc)
        neighbors = [n for n in neighbors if n in q]
        for n in neighbors:
            chng = elevation_graph[n] - elevation_graph[cur_loc]
            if chng <= 1:
                alt = dist[cur_loc] + 1
                if alt < dist[n]:
                    dist[n] = alt
                    prev[n] = cur_loc

    return dist, prev

# def part_one(data):
#     parsed, start, end = parse_data(data)
#     dist, prev = dijkstra(parsed, start, end)
#     answer = dist[end][0]
#     return answer

def construct_graph(data):
    parsed, start, end = parse_data(data)
    dg = nx.DiGraph()
    for i in range(parsed.shape[0]):
        for j in range(parsed.shape[1]):
            cur_loc = (i,j)
            dg.add_node(cur_loc)
            neighbors = find_neighbors(parsed, cur_loc)
            for n in neighbors:
                chng = parsed[n] - parsed[cur_loc]
                if chng <= 1:
                    dg.add_edge(cur_loc, n)
    return dg

def part_one(data):
    parsed, start, end = parse_data(data)
    dg = construct_graph(data)
    path = nx.shortest_path(dg, (start[0][0], start[1][0]), (end[0][0], end[1][0]))
    answer = len(path) - 1
    return answer

def find_starting_points(parsed):
    starting_points = []
    for i in range(parsed.shape[0]):
        for j in range(parsed.shape[1]):
            if parsed[(i,j)] == 0:
                starting_points.append((i,j))
    return starting_points

def part_two(data):
    parsed, _, end = parse_data(data)
    dg = construct_graph(data)
    starting_points = find_starting_points(parsed)
    min_len = parsed.shape[0]*parsed.shape[1]
    for s in starting_points:
        try:
            path = nx.shortest_path(dg, s, (end[0][0], end[1][0]))
        except nx.NetworkXNoPath:
            continue
        lp = len(path) - 1
        if lp < min_len:
            min_len = lp
    return min_len


test_part_one = part_one(test_data)
assert test_part_one == 31
part_one_answer = part_one(data)

test_part_two = part_two(test_data)
assert test_part_two == 29
part_two_answer = part_two(data)