from Quadruple import Quadruple
class CopyIR(Quadruple):
    # x := y
    def __init__(self, argument1, result):
        super(CopyIR, self).__init__()
        self.op = None
        self.arg1 = self.argument1
        self.arg2 = None
        self.result = self.result

    def __str__(self):
        return (self.result + " := " + self.arg1)

