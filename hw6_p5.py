from z3 import *
ina0, outa0, outa1, outa2 = Ints('ina0, outa0, outa1, outa2')
inb0, outb0 = Ints('inb0, outb0')


phi_a, phi_b = Bools('phi_a, phi_b')

phi_a = And((outa0 == ina0), (outa1 == outa0 * ina0), (outa2 == outa1 * ina0))
phi_b = (outb0 == (inb0 * inb0) * inb0)

phi = Implies(And((ina0 == inb0), phi_a, phi_b), (outa2 == outb0))
not_phi = Not(phi)

s = Solver()
print(s.check(not_phi))