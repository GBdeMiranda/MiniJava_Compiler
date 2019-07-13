from Quadruple import Quadruple
class CallIR(Quadruple):
    # x := call f, NUMPARAMS
    def __init__(self, f, NUMPARAMS, x):
        super(CallIR, self).__init__()
        self.op = "call"
        self.arg1 = f
        self.arg2 = NUMPARAMS
        self.result = x
        
    def __str__(self):
        if self.result != None:
            return (self.result + " := " + self.op + " " + self.arg1 + ", " + self.arg2)
        else:
            return (self.op + " " + self.arg1 + ", " + self.arg2)

