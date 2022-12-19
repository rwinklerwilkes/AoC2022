from aocd import get_data
import numpy as np

data = get_data(day=8,year=2022)
test_data = """30373
25512
65332
33549
35390"""

def parse_array(data):
    return np.array([[int(i) for i in row] for row in data.split('\n')])

# def roll_visibility(array, i, j, row_col, ascending_descending):
#     is_visible = True
#     prev_value = array[i][j]
#     start = 0
#     end = 0
#     it = 0
#     if row_col == 'row':
#         start = i
#         if ascending_descending == 'ascending':
#             start += 1
#             end = array.shape[0]
#             it = 1
#         elif ascending_descending == 'descending':
#             start -= 1
#             end = -1
#             it = -1
#     elif row_col == 'col':
#         start = j
#         if ascending_descending == 'ascending':
#             start += 1
#             end = array.shape[1]
#             it = 1
#         elif ascending_descending == 'descending':
#             start -= 1
#             end = -1
#             it = -1
#
#     for k in range(start, end, it):
#         if row_col == 'row':
#             comp_value = array[k][j]
#         else:
#             comp_value = array[i][k]
#         if comp_value >= prev_value:
#             is_visible = False
#             break
#         prev_value = comp_value
#     return is_visible

def roll_visibility(array, i, j, row_col, ascending_descending):
    if row_col == 'row' and ascending_descending == 'ascending':
        chk = np.max(array[i,j+1:array.shape[1]])
    if row_col == 'row' and ascending_descending == 'descending':
        chk = np.max(array[i,0:j])
    if row_col == 'col' and ascending_descending == 'ascending':
        chk = np.max(array[i+1:array.shape[0],j])
    if row_col == 'col' and ascending_descending == 'descending':
        chk = np.max(array[0:i,j])
    is_visible = chk < array[i][j]
    return is_visible

def calculate_scenic_component(value, array):
    if not np.any(array >= value):
        comp = len(array)
    else:
        comp = np.argmax(array>=value)+1
    return comp

def scenic_score(array, i, j):
    if i == 0 or j == 0:
        ss = 0
    elif i == array.shape[0]-1 or j == array.shape[0]-1:
        ss = 0
    value = array[i][j]
    ra = array[i,j+1:array.shape[1]]
    rd = np.flip(array[i, 0:j])
    ca = array[i+1:array.shape[0],j]
    cd = np.flip(array[0:i,j])
    rav = calculate_scenic_component(value, ra)
    rdv = calculate_scenic_component(value, rd)
    cav = calculate_scenic_component(value, ca)
    cdv = calculate_scenic_component(value, cd)
    ss = rav*rdv*cav*cdv
    return ss

def check_visible(array, i, j):
    value = array[i][j]
    #on edge
    if i == 0 or j == 0:
        is_visible = True
    elif i == array.shape[0]-1 or j == array.shape[0]-1:
        is_visible = True
    else:
        #go along row descending
        is_visible = False
        is_visible_rd = roll_visibility(array, i, j, row_col='row', ascending_descending='descending')
        if is_visible_rd:
            is_visible = True
        else:
            #go along col descending
            is_visible_cd = roll_visibility(array, i, j, row_col='col', ascending_descending='descending')
            if is_visible_cd:
                is_visible = True
            else:
                # go along row ascending
                is_visible_ra = roll_visibility(array, i, j, row_col='row', ascending_descending='ascending')
                if is_visible_ra:
                    is_visible = True
                else:
                    # go along col ascending
                    is_visible_ca = roll_visibility(array, i, j, row_col='col', ascending_descending='ascending')
                    if is_visible_ca:
                        is_visible = True
    return is_visible

def part_two(data):
    array = parse_array(data)
    max_scenic_score = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            ss = scenic_score(array,i,j)
            if ss > max_scenic_score:
                max_scenic_score = ss
    return max_scenic_score

def part_one(data):
    array = parse_array(data)
    sum_visible = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            sum_visible += check_visible(array,i,j)*1
    return sum_visible

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 21
part_one_answer = part_one(data)

test_part_two_answer = part_two(test_data)
assert test_part_two_answer == 8
part_two_answer = part_two(data)