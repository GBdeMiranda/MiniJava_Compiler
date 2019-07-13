
class Quadruple(object):
    op = object()
    arg1 = object()
    arg2 = object()
    result = object()

    def __str__(self):
    	pass
    
    def getOp(self):
        return self.op

    def getArg1(self):
        return self.arg1

    def getArg2(self):
        return self.arg2

    def getResult(self):
        return self.result

    def setOp(self, o):
        self.op = o

    def setArg1(self, o):
        self.arg1 = o

    def setArg2(self, o):
        self.arg2 = o

    def setResult(self, o):
        self.result = o
        