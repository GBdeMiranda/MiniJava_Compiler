from Quadruple import Quadruple

class AssignmentIR(Quadruple):    
    # x := y op z
    def __init__(self, operator, y, z, x):
        super(AssignmentIR, self).__init__()
        self.op = operator
        self.arg1 = y
        self.arg2 = z
        self.result = x

    def __str__(self):
        return (self.result + " := " + self.arg1 + " " + self.op + " " + self.arg2)

