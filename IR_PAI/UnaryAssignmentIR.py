from Quadruple import Quadruple

class UnaryAssignmentIR(Quadruple):
    # x := op y
    def __init__(self, operator, y, x):
        super(UnaryAssignmentIR, self).__init__()
        self.op = operator
        self.arg1 = y
        self.arg2 = None
        self.result = x

    def __str__(self):
        return(self.result + " := " + self.op + " " + self.arg1)

