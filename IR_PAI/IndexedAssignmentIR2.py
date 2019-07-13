from Quadruple import Quadruple
class IndexedAssignmentIR2(Quadruple):
    # y[i] := x
    def __init__(self, x, i, y):
        super(IndexedAssignmentIR2, self).__init__()
        self.op = None
        self.arg1 = x
        self.arg2 = i
        self.result = y
        
    def __str__(self):
        return (self.result + "[" + self.arg2 + "]" + " := " + self.arg1)

