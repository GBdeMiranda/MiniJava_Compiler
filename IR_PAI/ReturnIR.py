from Quadruple import Quadruple

class ReturnIR(Quadruple):
    # return y
    def __init__(self, y):
        super(ReturnIR, self).__init__()
        self.op = "return"
        self.arg1 = y
        self.arg2 = None
        self.result = None

    def __str__(self):
        return (self.op + " " + self.arg1)
    