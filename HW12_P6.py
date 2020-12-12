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

    # Constraint 1
    for i in queen_rows:
        cons1 = Or(queen_bools[i])

    # Constraint 2
    for i in rook_rows:
        cons2 = Or(rook_bools[i])

    # Constraint 3
    cons3 = True
    for i in range(size):
        for j in range(size):
            cons3 = And(cons3, Implies(queen_bools[i][j], Not(rook_bools[i][j])))

    # Constraint 4
    cons4 = True
    for i in range(size):
        for j in range(size):
            cons4 = And(cons4, Implies(queen_bools[i][j], And([And(Not(queen_bools[i][l]), Not(rook_bools[i][l])) for l in range(size) if l != j])))

    # Constraint 5
    cons5 = True
    for i in range(size):
        for j in range(size):
            cons5 = And(cons5, Implies(queen_bools[i][j], And([And(Not(queen_bools[k][j]), Not(rook_bools[k][j])) for k in range(size) if k != i])))

    # Constraint 6
    cons6 = True
    for i in range(size):
        for j in range(size):
            cons6 = And(cons6, Implies(rook_bools[i][j],
                          And([And(Not(queen_bools[i][l]), Not(rook_bools[i][l])) for l in range(size) if l != j])))

    # Constraint 7
    cons7 = True
    for i in range(size):
        for j in range(size):
            cons7 = And(cons7, Implies(rook_bools[i][j],
                          And([And(Not(queen_bools[k][j]), Not(rook_bools[k][j])) for k in range(size) if k != i])))

    # Constraint 8
    cons8 = True
    for i in range(size):
        for j in range(size):
            cons8 = And(cons8, Implies(queen_bools[i][j], And([And(Not(queen_bools[k][l]), Not(rook_bools[k][l])) for k in range(size)
                                                  for l in range(size) if k != i and l != j and k - l == i - j])))

    # Constraint 9
    cons9 = True
    for i in range(size):
        for j in range(size):
            cons9 = And(cons9,
                Implies(queen_bools[i][j], And([And(Not(queen_bools[k][l]), Not(rook_bools[k][l])) for k in range(size)
                                                for l in range(size) if k != i and l != j and k + l == i + j])))
    all_cons = [cons1, cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9]
    s0 = Solver()
    s0.add(all_cons)
    if s0.check() == unsat:
        print("Unsatisfiable!")
    else:
        for rm in range(9):
            s = Solver()
            new_cons = [all_cons[select] for select in range(9) if rm != select]
            s.add(And(new_cons))
            if s.check() == sat:
                model0 = s0.model()
                model1 = s.model()
                flag = True
                for i in range(size):
                    for j in range(size):
                        b0 = "N"
                        b1 = "N"
                        if model0[queen_bools[i][j]] == True:
                            b0 = "Q"
                        elif model0[rook_bools[i][j]] == True:
                            b0 = "R"
                        if model1[queen_bools[i][j]] == True:
                            b1 = "Q"
                        elif model1[rook_bools[i][j]] == True:
                            b1 = "R"
                        if b0 != b1:
                            flag = False
                            break
                if flag:
                    print(rm+1)



if __name__ == "__main__":
    n = int(input('input value of n:'))
    main(n)