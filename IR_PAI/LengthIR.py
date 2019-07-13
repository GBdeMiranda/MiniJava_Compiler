from Quadruple import Quadruple
class LengthIR(Quadruple):
    # x := length y
    def __init__(self, y, x):
        super(LengthIR, self).__init__()
        self.op = "length"
        self.arg1 = y
        self.arg2 = None
        self.result = x

    def __str__(self):
        return self.result + " := " + self.op + " " + self.arg1

