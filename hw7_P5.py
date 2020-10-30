# HW7 Problem5 Pseudo-Boolean satisfiability and optimization solver with Z3Py
#
# Instructions:
# Input:
# Enter the file name in the console, the file should be in the same folder with this python file. Press Enter.
# In the file, please type the encoding list in the form of the example in the problem description.
# Output:
# false/true. If true, it will show the assignment for the variables.

from z3 import *
import math
import ast

class var:
    def __init__(self, index):
        self.name = 'x' + str(index)
        self.bool = Bool(index)

def ini_var_list(input):
# Get a list of variables from the input
    var_list = []
    name_list = []
    for f in input:
        for ele in f:
            for s in ele[1]:
                name = s[1]
                if name not in name_list:
                    name_list.append(name)
                    var_list.append(var(name))
    return var_list

def input_process(file_name):
    input = ""
    with open(file_name, "r") as fd:
        for line in fd:
            line = line.strip()
            input += line
    input = ast.literal_eval(input)
    target_f = input[0]
    constraints_f = input[1:]
    var_list = ini_var_list(input)
    return var_list, target_f, constraints_f

def eval_formula(formula, model):
    sum = 0
    for term in formula:
        const = term[0]
        mul_var = 1
        for i in range(len(term[1])):
            if term[1][i] == []:
                break
            ele = term[1][i]
            ele_var = var(ele[1])
            if ele[0] == 0 and not model.evaluate(ele_var.bool, model_completion=True) or ele[0] == 1 and model.evaluate(ele_var.bool, model_completion=True):
                mul_var = 0
                break
        sum += const*mul_var
    return sum

def check_constraints(flist, model):
    for f in flist:
        if eval_formula(f, model) > 0:
            return False
    return True

def assignment(var_list, model):
    result = []
    for var in var_list:
        if model[var.bool]:
            result.append((var.name, 1))
        else:
            result.append((var.name, 0))
    return result


def main(file_name):
    # Try all the possible values for the boolean variables. Check whether the constraints are satisfied with this assignment. If so, record the model that could minimize the objective function.
    s = Solver()
    var_list, target_f, constraints_f = input_process(file_name)
    var_bool_list1 = [var.bool for var in var_list]
    var_bool_list2 = [Not(var.bool) for var in var_list]
    s.add(Or(var_bool_list1+var_bool_list2))
    count = 0
    flag = False
    min_target = math.inf
    while s.check() == sat and count<10000:
        m = s.model()
        count += 1
        if check_constraints(constraints_f, m):
            flag = True
            if eval_formula(target_f, m) < min_target:
                min_m = m
                min_target = eval_formula(target_f, m)
            comparison_list = []
            for x in var_list:
                comparison_list.append((x.bool != m[x.bool]))
            s.add(Or(comparison_list))
    if not flag:
        print("false")
    else:
        print("true")
        assign = assignment(var_list, min_m)
        print(assign)


if __name__ == "__main__":
    file_name = input("Enter the file name: ")
    main(file_name)

