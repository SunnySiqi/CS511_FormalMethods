# HW9 Problem5/Problem6 MaxSAT and Bayesian Network
#
# Instructions:
# Input:
# Enter the problem name in the console(MPE or MAP). Press Enter.
# Enter the text file name in the console(ex: test.txt), the file should be in the same folder with this python file. Press Enter.
# Output:
# It will show the assignment for the variables.
#
# The code is not completed... I didn't figure out the solution for these two problems, only some ideas:
# 1. Transfer this problem to a MaxSAT problem:
# For [Cs, [V,v], p], let p be the weight, make a formula: Cs -> V=v, where Cs: X1 == x1 and X2 == x2 and ... and Xn == xn
# 2. The solution should be the optimal value for P(V1=v1, ..., Vn=vn| Os)
from z3 import *
import ast

def input_process_MAP(file_name):
    with open(file_name, "r") as fd:
        inputlist = fd.readlines()
    CPTs = ast.literal_eval("".join(inputlist[:-2]))
    Os = ast.literal_eval(inputlist[-2])
    Vs = ast.literal_eval(inputlist[-1])
    return CPTs, Os, Vs

def input_process_MPE(file_name):
    with open(file_name, "r") as fd:
        inputlist = fd.readlines()
    CPTs = ast.literal_eval("".join(inputlist[:-2]))
    Os = ast.literal_eval(inputlist[-2])
    return CPTs, Os

def cons2sat(row, var_dict):
    Cs = row[0]
    v = row[1]
    row_list = []
    for c in Cs:
        if c[0] not in var_dict:
            var_dict[c[0]] = Bool(c[0])
        if c[1] == 0:
            row_list.append(Not(var_dict[c[0]]))
        else:
            row_list.append(var_dict[c[0]])
    if v[0] not in var_dict:
        var_dict[v[0]] = Bool(v[0])
    if v[1] == 0:
        formula = Implies(And(row_list), Not(var_dict[v[0]]))
    else:
        formula = Implies(And(row_list), var_dict[v[0]])
    return formula

if __name__ == "__main__":
    problem = input("Enter the Problem (MPE or MAP):")
    file_name = input("Enter the file name: ")
    o = Optimize()
    if problem == 'MPE':
        CPTs, Os = input_process_MPE(file_name)
        var_dict = dict()
        for ob in Os:
            var_dict[ob[0]] = Bool(ob[0])
            if ob[1] == 0:
                o.add(var_dict[ob[0]] == False)
            else:
                o.add(var_dict[ob[0]] == True)
        for x in CPTs:
            cs = x[1]
            for row in cs:
                consSAT = cons2sat(row, var_dict)
                o.add_soft(consSAT, row[-1])
        print(o.check())
        print(o.model())

    if problem == 'MAP':
        CPTs, Os, Vs = input_process_MAP(file_name)
        var_dict = dict()
        for ob in Os:
            var_dict[ob[0]] = Bool(ob[0])
            if ob[1] == 0:
                o.add(var_dict[ob[0]] == False)
            else:
                o.add(var_dict[ob[0]] == True)
        for v in Vs:
            if v not in var_dict:
                var_dict[v] = Bool(v)

        for x in CPTs:
            cs = x[1]
            for row in cs:
                consSAT = cons2sat(row, var_dict)
                o.add_soft(consSAT, row[-1])
        print(o.check())
        print(o.model())







