from aocd import get_data

data = get_data(day=10, year=2022)
test_data_sm = """noop
addx 3
addx -5"""

test_data_lg = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

class Program:
    def __init__(self):
        self.registers = {'X': 1}
        self.cycle = 1
        self.inst_loc = 0
        self.instructions = []
        self.interesting_cycles = {i:0 for i in range(20,240,40)}
        self.crt = {i: '.' for i in range(0,240)}

    def run_line(self, line):
        sp = line.split(' ')
        if len(sp) == 1:
            inst = sp[0]
        else:
            inst, val = sp
        if inst == 'noop':
            self.instructions.append(['noop', 1, 0])
        elif inst == 'addx':
            self.instructions.append(['addx',2,int(val)])

    def draw_crt_pixel(self):
        #self.cycle is always 1 ahead of crt
        cur_pos = (self.cycle - 1)%40
        row = (self.cycle-1)//40
        if abs(self.registers['X'] - cur_pos) <= 1:
            self.crt[row*40+cur_pos] = '#'

    def draw_crt_all(self):
        out_str = ''
        for i in range(6):
            out_str += ''.join(list(self.crt.values())[40*i:40*(i+1)])
            out_str += '\n'
        print(out_str)

    def run_program(self, data):
        all_inst = data.split('\n')
        while self.inst_loc < len(all_inst) or self.instructions:
            if self.inst_loc < len(all_inst):
                ln = all_inst[self.inst_loc]
                #start of cycle
                if not self.instructions:
                    self.run_line(ln)
                    self.inst_loc += 1

            self.draw_crt_pixel()

            if self.cycle in self.interesting_cycles:
                self.interesting_cycles[self.cycle] = self.registers['X']*self.cycle
            #end of cycle
            cur_inst = self.instructions.pop(0)
            cur_inst[1] -= 1
            if cur_inst[1] > 0:
                self.instructions.append(cur_inst)
            else:
                self.registers['X'] += cur_inst[2]
            self.cycle += 1


def part_one(data):
    p = Program()
    p.run_program(data)
    answer = sum(p.interesting_cycles.values())
    return answer

def part_two(data):
    p = Program()
    p.run_program(data)
    p.draw_crt_all()

test_part_one_answer = part_one(test_data_lg)
assert test_part_one_answer == 13140
part_one_answer = part_one(data)

part_two(data)