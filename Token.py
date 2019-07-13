
class Token(object):
    value = object()
    line = int()
    col = int()

    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col

    def getValue(self):
        return self.value

    def getLine(self):
        return self.line

    def getCol(self):
        return self.col

