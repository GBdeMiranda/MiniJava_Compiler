from Quadruple import Quadruple

class NewArrayIR(Quadruple):
	# x := new TYPE, SIZE
    def __init__(self, TYPE, SIZE, x):
        super(NewArrayIR, self).__init__()
        self.op = "new"
        self.arg1 = TYPE
        self.arg2 = SIZE
        self.result = x

    def __str__(self):
        return (self.result + " := " + self.op + " " + self.arg1 + ", " + self.arg2)

