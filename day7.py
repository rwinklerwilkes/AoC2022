from aocd import get_data
import re

data = get_data(day=7,year=2022)
test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

class Node:
    def __init__(self, is_folder, filesize = 0, parent=None):
        self.parent = parent
        self.children = {}
        if is_folder:
            self.type = 'folder'
        else:
            self.type = 'file'
        self.filesize = filesize

    def get_size(self):
        #We may have cached the filesize previously, so just return if we did
        if self.type == 'file' or self.filesize > 0:
            return self.filesize
        else:
            size = 0
            stack = list(self.children.values())
            while stack:
                i = stack.pop()
                item_size = i.get_size()
                size += item_size
            self.filesize = size
            return size

    def add_child(self,node,node_name):
        self.children[node_name] = node

class FileSystem:
    def __init__(self, instructions):
        self.root = Node(is_folder=True, parent=None)
        self.cur_node = self.root
        self.instructions = instructions.split('\n')
        self.instructions_position = 0
        self.all_directories = [self.root]
        self.parse_instructions()

    def parse_line(self, line):
        valid_regex = {'\$ cd \.\.':self.up,
                       '\$ cd \/':self.go_to_root,
                       '\$ ls':self.ls,
                       'dir ([a-z]{1,})':self.dir,
                       '\$ cd ([a-z]{1,})': self.cd,
                       '([0-9]{1,}) ([a-z\.]{1,})':self.file,
                       }

        for pat, func in valid_regex.items():
            m = re.match(pat, line)
            if m:
                num_groups = len(m.groups())
                if num_groups == 0:
                    func()
                elif num_groups == 1:
                    param = m.group(1)
                    func(param)
                elif num_groups == 2:
                    fs, fn = m.groups()
                    func(fs, fn)

    def up(self):
        self.cur_node = self.cur_node.parent

    def go_to_root(self):
        self.cur_node = self.root

    def ls(self):
        #Move forward one past the ls line
        self.instructions_position += 1
        peek = self.instructions_position + 1
        #While we haven't reached another filesystem instruction, keep reading and parsing
        while self.instructions_position < len(self.instructions) and \
                self.instructions[self.instructions_position][0]!='$':
            cur_line = self.instructions[self.instructions_position]
            self.parse_line(cur_line)
            self.instructions_position += 1

        #Went too far so let's back off by 1
        self.instructions_position -= 1

    def cd(self, destination_folder):
        try:
            self.cur_node = self.cur_node.children[destination_folder]
        except KeyError:
            print(self.cur_node.children)
            raise KeyError

    def dir(self, new_folder):
        folder = Node(is_folder=True, parent=self.cur_node)
        self.cur_node.add_child(folder, new_folder)
        self.all_directories.append(folder)

    def file(self, fs, fn):
        file = Node(is_folder=False, parent=self.cur_node, filesize=int(fs))
        self.cur_node.add_child(file, fn)

    def parse_instructions(self):
        while self.instructions_position < len(self.instructions):
            cur_line = self.instructions[self.instructions_position]
            self.parse_line(cur_line)
            self.instructions_position += 1

def part_one(data, max_size=100000):
    fs = FileSystem(data)
    answer = sum([dir.get_size() for dir in fs.all_directories if dir.get_size() < max_size])
    return answer

def part_two(data):
    fs = FileSystem(data)
    update_size = 30000000
    fs_size = 70000000
    total_size = fs.root.get_size()
    leftover_size = fs_size-total_size
    need_to_free = update_size - leftover_size
    eligible_dirs = [dir.get_size() for dir in fs.all_directories if dir.get_size() > need_to_free]
    answer = min(eligible_dirs)
    return answer

test_part_one_answer = part_one(test_data)
assert test_part_one_answer == 95437
part_one_answer = part_one(data)

test_part_two_answer = part_two(test_data)
assert test_part_two_answer == 24933642
part_two_answer = part_two(data)