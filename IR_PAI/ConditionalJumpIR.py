from Quadruple import Quadruple
class ConditionalJumpIR(Quadruple):
    # if false x goto LABEL
    def __init__(self, x, label):
        super(ConditionalJumpIR, self).__init__()
        self.op = "iffalse"
        self.arg1 = x
        self.arg2 = "goto"
        self.result = label
        
    def __str__(self):
        return (self.op + " " + self.arg1 + " " + self.arg2 + " " + self.result)

