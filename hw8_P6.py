# HW8 Problem6: weighted stability problem based on PB function
#
# Instructions:
# -Input:
# In the console, there will be instructions to enter the weight function and the capacity function.
# Here is a valid input example:
# Enter the weight function:[100, 100, 100, 1, 100]
# Enter the capacity function:[[0,7,1,0,8],[7,0,5,4,3],[1,5,0,2,6],[0,4,2,0,1],[8,3,6,1,0]]
# Press "Return" after completion for each function.
# -Output:
# The characteristic vector of the set S: the {0,1} assignment to the sequence (x1, x2, ..., xn); The value of the max_weight_independent_set.
import ast
from z3 import *

if __name__ == "__main__":
    vertex_w = ast.literal_eval(input("Enter the weight function:"))
    edge_c = ast.literal_eval(input("Enter the capacity function:"))
    num_v = len(vertex_w)

    # Initialize a list of integer variables:x1...xn; constraint: xi == 1 or xi == 0
    s = Solver()
    x = [Int("x" + str(i)) for i in range(1, num_v+1)]
    for i in range(num_v):
        s.add(Or(x[i] == 1, x[i] == 0))

    # Compute objective function
    max_indset = Int("max_weight_independent_set")
    sum1 = 0
    sum2 = 0
    max_w = max(vertex_w)
    for i in range(num_v):
        sum1 += vertex_w[i] * x[i]
        for j in range(i+1, num_v):
            sum2 += edge_c[i][j] * x[i] * x[j]
    temp = sum1 - (1 + max_w)*sum2
    s.add(max_indset == temp)

    # Print the model with the max_weight_independent_set value
    while s.check() == sat:
        sat_model = s.model()
        s.add(max_indset > sat_model[max_indset])
    print(sat_model)