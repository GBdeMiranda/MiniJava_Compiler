
#from SymbolTablePack import SymbolTableNew, Scope, BlockSymbolTable, ClassSymbolTable, MethodSymbolTable, Variable
from SymbolTablePack import *

class MethodSymbolTable(BlockSymbolTable):

    name = str()
    args = dict()
    argNames = []
    returnType = str()
    
    def __init__(self, parent, name, paramNames, paramTypes, returnType):
#        super(MethodSymbolTable, self)._init_(parent)
        self.name = name
        self.args = dict()
        self.argNames = paramNames
        i = 0
        while i < paramNames.length:
            reg = "$a" + i
            self.args[paramNames[i]] = Variable(paramNames[i], paramTypes[i], reg)
            i += 1
        self.returnType = returnType

    def getParameters(self):
        params = [None]*len(self.argNames)
        i = 0
        while i < params.length:
            params[i] = self.args.get(self.argNames[i])
            i += 1
        return params

    def numParameters(self):
        return len(self.getParameters())

    def getReturnType(self):
        return self.returnType

    def getName(self):
        return self.name

    def localVarLookup(self, name):
        try:
            return self.BlockSymbolTable.vars_dictionary.get(name)
        except:
            try:
                return self.args.get(name)
            except:
                return None

    def assignRegisters(self, allocator):
        keys = sorted(self.BlockSymbolTable.vars_dictionary.keys())
        i = 0
        while i < len(keys):
            v = self.BlockSymbolTable.vars_dictionary.get(keys[i])
            v.setRegister(allocator.allocateReg())
            i += 1