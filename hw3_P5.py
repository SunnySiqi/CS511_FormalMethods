from z3 import *

class task:
    def __init__(self, name, duration):
        self.name = name
        self.starttime = Int(name)
        self.duration = duration
        self.endtime = self.starttime + duration

def not_overlap(task1, task2):
    return Or((task1.endtime <= task2.starttime), (task2.endtime <= task1.starttime))

def main():
    A = task('A', 2)
    B = task('B', 1)
    C = task('C', 2)
    D = task('D', 2)
    E = task('E', 7)
    F = task('F', 5)

    s = Solver()
    AC_not_overlap = not_overlap(A, C)
    BD_not_overlap = not_overlap(B, D)
    BE_not_overlap = not_overlap(B, E)
    DE_not_overlap = not_overlap(D, E)
    DE_before_F = And((D.endtime <= F.starttime), (E.endtime <= F.starttime))
    A_before_B = A.endtime <= B.starttime
    start_non_neg = And(A.starttime >=0, B.starttime >=0, C.starttime >=0, D.starttime >=0, E.starttime >=0, F.starttime >=0)
    end = Int('end')
    done_before_end = And(A.endtime <= end, B.endtime <= end, C.endtime <= end, D.endtime <= end, E.endtime <= end, F.endtime <= end)
    s.add(AC_not_overlap)
    s.add(BD_not_overlap)
    s.add(BE_not_overlap)
    s.add(DE_not_overlap)
    s.add(DE_before_F)
    s.add(A_before_B)
    s.add(start_non_neg)
    s.add(done_before_end)

    if s.check() == sat:
        return s.model()
    else:
        return None

if __name__ == "__main__":
    m = main()
    print(m)

