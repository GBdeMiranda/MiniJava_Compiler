from Quadruple import Quadruple
class IndexedAssignmentIR1(Quadruple):
    # x := y[i]
    def __init__(self, y, i, x):
        super(IndexedAssignmentIR1, self).__init__()
        self.op = None
        self.arg1 = y
        self.arg2 = i
        self.result = x
        
    def __str__(self):
        return (self.result + " := " + self.arg1 + "[" + self.arg2 + "]")

