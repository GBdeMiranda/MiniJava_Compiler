#!/usr/bin/env python
class Temporary(object):
    nextNumber = int()
    num = int()

    def __init__(self):
        self.num = self.nextNumber
        self.nextNumber += 1

    def __str__(self):
        return ("t" + self.num)

    def getNum(self):
        return self.num

    def reset(self):
        self.nextNumber = -1

