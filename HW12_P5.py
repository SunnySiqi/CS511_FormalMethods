from z3 import *
import numpy as np
# input the value of n in the console
def main(n):
    size = n
    num_queens = int(n/3)
    # Variables
    queen_bools = [[Bool("q" + str(i + 1) + "," + str(j + 1)) for j in range(size)] for i in range(size)]
    rook_bools = [[Bool("r" + str(i + 1) + "," + str(j + 1)) for j in range(size)] for i in range(size)]

    queen_rows = np.random.choice(range(size), size=num_queens)
    rook_rows = list(set(range(size)) - set(queen_rows))

    s = Solver()
    # Constraint 1
    for i in queen_rows:
        s.add(Or(queen_bools[i]))

    # Constraint 2
    for i in rook_rows:
        s.add(Or(rook_bools[i]))

    # Constraint 3
    for i in range(size):
        for j in range(size):
            s.add(Implies(queen_bools[i][j], Not(rook_bools[i][j])))

    # Constraint 4
    for i in range(size):
        for j in range(size):
            s.add(Implies(queen_bools[i][j], And([And(Not(queen_bools[i][l]), Not(rook_bools[i][l])) for l in range(size) if l != j])))

    # Constraint 5
    for i in range(size):
        for j in range(size):
            s.add(Implies(queen_bools[i][j], And([And(Not(queen_bools[k][j]), Not(rook_bools[k][j])) for k in range(size) if k != i])))

    # Constraint 6
    for i in range(size):
        for j in range(size):
            s.add(Implies(rook_bools[i][j],
                          And([And(Not(queen_bools[i][l]), Not(rook_bools[i][l])) for l in range(size) if l != j])))

    # Constraint 7
    for i in range(size):
        for j in range(size):
            s.add(Implies(rook_bools[i][j],
                          And([And(Not(queen_bools[k][j]), Not(rook_bools[k][j])) for k in range(size) if k != i])))

    # Constraint 8
    for i in range(size):
        for j in range(size):
            s.add(Implies(queen_bools[i][j], And([And(Not(queen_bools[k][l]), Not(rook_bools[k][l])) for k in range(size)
                                                  for l in range(size) if k != i and l != j and k - l == i - j])))

    # Constraint 9
    for i in range(size):
        for j in range(size):
            s.add(
                Implies(queen_bools[i][j], And([And(Not(queen_bools[k][l]), Not(rook_bools[k][l])) for k in range(size)
                                                for l in range(size) if k != i and l != j and k + l == i + j])))

    if s.check() == unsat:
        print("Unsatisfiable!")
    else:
        model = s.model()
        b = [[" " for j in range(n)] for i in range(n)]
        for i in range(size):
            print_s = ''
            for j in range(size):
                if model[queen_bools[i][j]] == True:
                    b[i][j] = "Q"
                elif model[rook_bools[i][j]] == True:
                    b[i][j] = "R"
                print_s += '|' + b[i][j]
                if j == size -1:
                    print(print_s+'|')
                    print('-'*2*size)


if __name__ == "__main__":
    n = int(input('input value of n:'))
    main(n)