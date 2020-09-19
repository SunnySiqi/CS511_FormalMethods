from z3 import *
'''
truth-table:
p1, p2, p3, p4, \phi
0, 0, 0, 0 -> 1
0, 0, 0, 1 -> 0
0, 0, 1, 0 -> 0
0, 0, 1, 1 -> 1
0, 1, 0, 0 -> 0
0, 1, 0, 1 -> 1
0, 1, 1, 0 -> 1
0, 1, 1, 1 -> 0
1, 0, 0, 0 -> 0
1, 0, 0, 1 -> 1
1, 0, 1, 0 -> 1
1, 0, 1, 1 -> 0
1, 1, 0, 0 -> 1
1, 1, 0, 1 -> 0
1, 1, 1, 0 -> 0
1, 1, 1, 1 -> 1

CNF: (not(p1) or not(p2) or not(p3) or p4) and (not(p1) or not(p2) or p3 or not(p4))
and (not(p1) or p2 or not(p3) or not(p4)) and (p1 or not(p2) or not(p3) or not(p4))
and (p1 or p2 or p3 or not(p4)) and (p1 or p2 or not(p3) or p4) and (p1 or not(p2) or p3 or p4)
and (not(p1) or p2 or p3 or p4)

DNF: (not(p1) and not(p2) and not(p3) and not(p4)) or (not(p1) and not(p2) and p3 and p4)
or (not(p1) and p2 and not(p3) and p4) or (not(p1) and p2 and p3 and not(p4)) 
or (p1 and not(p2) and not(p3) and p4) or (p1 and not(p2) and p3 and not(p4))
or (p1 and p2 and not(p3) and not(p4)) or (p1 and p2 and p3 and p4)

<->: ((p1 <-> p2) <-> (p3 <-> p4)) <-> ((p1 <-> p3) <-> (p2 <-> p4)) <-> ((p1 <-> p4) <-> (p2 <-> p3))

'''
p1, p2, p3, p4 = Bools('p1 p2 p3 p4')
phi = And(Or(Not(p1), Not(p2), Not(p3), p4), Or(Not(p1), Not(p2), p3, Not(p4)), Or(Not(p1), p2, Not(p3), Not(p4)),
          Or(p1, Not(p2), Not(p3), Not(p4)), Or(Not(p1), p2, p3, p4), Or(p1, Not(p2), p3, p4),
          Or(p1, p2, Not(p3), p4), Or(p1, p2, p3, Not(p4)))

psi = Or(And(Not(p1), Not(p2), Not(p3), Not(p4)), And(Not(p1), Not(p2), p3, p4),
         And(Not(p1), p2, p3, Not(p4)), And(Not(p1), p2, Not(p3), p4),
         And(p1, Not(p2), Not(p3), p4), And(p1, Not(p2), p3, Not(p4)),
         And(p1, p2, Not(p3), Not(p4)), And(p1, p2, p3, p4))

theta = (p1 == p2) == (p3 == p4)

s = Solver()
#equ_condition = Or(phi != psi, phi != theta, psi != theta)
equ_condition = Not(And(phi == psi, phi == theta, psi == theta))
s.add(equ_condition)
print(s.check())
# the result is "unsat": Not(And(phi == psi, phi == theta, psi == theta)) is unsat, so And(phi == psi, phi == theta, psi == theta) is a tautology

# #check the truth table for each formula
# s = Solver()
# s.add(phi) #phi/psi/theta
# results = []
# while s.check() == sat:
#     m = s.model()
#     results.append (m)
#     s.add(Or(p1 != m[p1], p2 != m[p2], p3 != m[p3], p4 != m[p4]))
#
# for example in results:
#     print(example)
