from Quadruple import Quadruple

class UnconditionalJumpIR(Quadruple):
    # goto LABEL
    def __init__(self, label):
        super(UnconditionalJumpIR, self).__init__()
        self.op = "goto"
        self.arg1 = None
        self.arg2 = None
        self.result = label
        
    def __str__(self):
        return (self.op + " " + self.result)

