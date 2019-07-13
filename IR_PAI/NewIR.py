from Quadruple import Quadruple
class NewIR(Quadruple):
    # x := new TYPE
    def __init__(self, TYPE, x):
        super(NewIR, self).__init__()
        self.op = "new"
        self.arg1 = TYPE
        self.arg2 = None
        self.result = x

    def __str__(self):
        return (self.result + " := " + self.op + " " + self.arg1)

