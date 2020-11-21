# HW10 Problem6
#
# Instructions:
# Input:
# Enter the text file name in the console(ex: test.txt), the file should be in the same folder with this python file. Press Enter.
# In the file, please type in the form of the example in the problem description.


from z3 import *
from itertools import combinations

class board:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.grids =[[0 for i in range(n)] for j in range(m)]
        for i in range(m):
            for j in range(n):
                self.grids[i][j] = grid(i, j)

    def get_grid_val(self, row, col):
        return self.grids[row][col].val

    def set_grid_val(self, row, col, value):
        self.grids[row][col].val = value

    def get_adjc(self, row, col):
        ret = []
        if row > 1:
            ret.append(self.grids[row - 1][col])
        if row < self.m - 1:
            ret.append(self.grids[row + 1][col])
        if col > 1:
            ret.append(self.grids[row][col - 1])
        if col < self.n - 1:
            ret.append(self.grids[row][col + 1])
        return ret

class grid:
    def __init__(self, row, col):
            self.row = row
            self.col = col
            self.val = Bool("(" + str(row) + "," + str(col) + ")")

def get_bool_list(set):
    ret = []
    for g in set:
        ret.append(g.val)
    return ret

def input_process(file_name):
    f = open(file_name, "r")
    input = f.readlines()
    size = input[0][:-1].split('=')[1]
    PierPos = eval(input[1][:-1].split('=')[1])
    BlockedPos = eval(input[2].split('=')[1])
    return size, PierPos, BlockedPos

def main(file_name):
    s = Solver()
    w_sum = Int("sum")

    size, PierPos, BlockedPos = input_process(file_name)
    m = int(size.split(',')[0][2:])
    n = int(size.split(',')[1][:-1])
    b = board(m, n)

    for p in PierPos:
        (i, j) = p
        i = i-1
        j = j-1
        b.set_grid_val(i, j, True)
        neighbors = b.get_adjc(i, j)
        neighbors_bool = [n.val for n in neighbors]
        s.add(Or(neighbors_bool))
        for neighbor in neighbors:
            others = list(set(neighbors) - set([neighbor]))
            others_bool = [o.val for o in others]
            s.add(Implies(neighbor.val, Not(Or(others_bool))))

    for p in BlockedPos:
        (i, j) = p
        i = i-1
        j = j-1
        b.set_grid_val(i, j, False)

    for i in range(b.m):
        for j in range(b.n):
            neighbors = b.get_adjc(i, j)
            select_neighbors = combinations(neighbors, 2)
            s.add(Implies(b.get_grid_val(i,j), Or([And(get_bool_list(select_neighbor)) for select_neighbor in select_neighbors])))

    weight = 0
    for i in range(b.m):
        for j in range(b.n):
            weight += IntSort().cast(Not(b.get_grid_val(i, j)))
    s.add(w_sum == weight)

    if s.check() == unsat:
        print("Unsatisfiable!")
        quit()
    while s.check() == sat:
        model = s.model()
        s.add(w_sum > model[w_sum])

    assign = []
    for i in range(b.m):
        for j in range(b.n):
            if model[b.get_grid_val(i,j)] == True:
                assign.append((i,j))
    print(assign)


# def input_process():
if __name__ == "__main__":
    file_name = input("Enter the file name: ")
    main(file_name)





