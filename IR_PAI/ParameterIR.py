from Quadruple import Quadruple

class ParameterIR(Quadruple):
    # param x
    def __init__(self, x):
        super(ParameterIR, self).__init__()
        self.op = "param"
        self.arg1 = x
        self.arg2 = None
        self.result = None

    def __str__(self):
        return (self.op + " " + self.arg1)

