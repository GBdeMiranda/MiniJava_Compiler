#!/usr/bin/env python

from SymbolTablePack import SymbolTableNew, Scope, BlockSymbolTable, ClassSymbolTable, MethodSymbolTable, Variable

class ClassSymbolTable(BlockSymbolTable, Scope):
    name = str()
    parentClass = str()
    methods = dict()
    size = int()

    offset = int()

    def __init__(self, parent, name, parentClass):
        super(ClassSymbolTable, self).__init__(parent)
        self.parentClass = parentClass
        self.name = name
        self.methods = dict()
        self.size = -1
        self.offset = -1

    def enterScope(self, name):
        return self.methods.get(name)

    def addMethod(self, name, paramNames, paramTypes, returnType):
        self.methods[name] = MethodSymbolTable(self, name, paramNames, paramTypes, returnType)

    def getMethods(self):
        return self.methods

    #calcula o offset da variavel baseado em qual escopo ele ta insterida e qual a sua ordem localmente
    def calculateVarOffsets(self):
        parentOffset = self.getOffset()
        localOffset = 0
        keys = sorted( self.BlockSymbolTable.vars_dictionary.keys() )
        i = 0
        while i < len(keys):
            v = self.vars_dictionary[keys[i]]
            v.setOffset(parentOffset + localOffset)
            localOffset += 4
            i += 1

    def calculateSize(self):
        self.size = 0
        keys = sorted( self.methods.keys() )
        i = 0
        while i < len(keys):
            self.size += 4
            i += 1
        if self.parentClass != None:
            self.size += (ClassSymbolTable(self.parent.enterScope(self.parentClass))).getSize()
        return self.size

    def getSize(self):
        if self.size == -1:
            self.size = self.calculateSize()
        return self.size

    def calculateOffset(self):
        self.offset = 0
        if self.parentClass != None:            
            self.offset = (ClassSymbolTable(self.parent.enterScope(self.parentClass))).getSize()
        return self.offset

    def getOffset(self):
        if self.offset == -1:
            self.offset = self.calculateOffset()
        return self.offset

    def lookupParentsMethod(self, name, paramNames, paramTypes, returnType):
        if self.parentClass != None:
            temp = self.parent.enterScope(self.parentClass);
            if temp != None:
                return temp.lookupMethod(name, paramNames, paramTypes, returnType)
        return False

    def lookupMethod(self, name, paramNames, paramTypes, returnType):
        try:
            method = self.methods.get(name)
        except:
            method = None

        if method == None:
            return self.lookupParentsMethod(name, paramNames, paramTypes, returnType)
        if not method.getReturnType() == returnType:
            return self.lookupParentsMethod(name, paramNames, paramTypes, returnType)
        parameters = method.getParameters()
        if len(parameters) != len(paramNames):
            return self.lookupParentsMethod(name, paramNames, paramTypes, returnType)
        for i in range(len(parameters)):
            param = parameters[i]
            if not param.getName() == paramNames[i]:
                return self.lookupParentsMethod(name, paramNames, paramTypes, returnType)
            if not param.getType() == paramTypes[i]:
                return self.lookupParentsMethod(name, paramNames, paramTypes, returnType)
        return True

    def getMethod(self, name):
        if self.isMethod(name):
            mst =  self.methods.get(name) 
            if mst != None:
                return mst
            elif self.parentClass != None:
                return (ClassSymbolTable(self.parent.enterScope(self.parentClass))).getMethod(name)
            else:
                return None
        else:
            return None

    def isMethod(self, name):
        if not(name in self.methods.keys()):
            if self.parentClass != None:
                return self.parent.enterScope(self.parentClass).isMethod(name)
            else:
                return False
        return True

    def print_(self, indentLevel):
        print ("class " + self.name)
        if self.parentClass != None:
            print (" extends " + self.parentClass )
        keys = sorted( self.vars_dictionary.keys() )
        
        for i in range(0,len(keys)):
            self.printIndentation( indentLevel ) # BLOCKSYMBOLTABLE
            print( self.vars_dictionary.get(  keys[i].getType() + " " + self.vars_dictionary.get( keys[i] ).__name__ + ";" ) )
        keys = sorted( self.methods.keys() )
        for i in range(0,len(keys)):
            self.printIndentation(indentLevel)   # BLOCKSYMBOLTABLE
            print( " - (" + self.methods[ keys[i] ].getReturnType() + ") " + self.methods[keys[i]].__name__ + "(" )
            params = self.methods[ keys[i] ].getParameters()
            
            for j in range(0,len()):
                param = Variable( params[j] )
                print (param.getType() + " " + param.__name__ + ", ")
            param = Variable( params[len(params)-1] )
            print( param.getType() + " " + param.__name__ + ")" )
            self.methods.get( keys[i] ).print_(indentLevel + 1)

    def getName(self):
        return self.name

    def getParentClass(self):
        return self.parentClass

    def localVarLookup(self, name):
        var = self.vars_dictionary.get(name)
        if var != None:
            return var
        if self.parentClass != None:
            temp = self.parent.enterScope(self.parentClass)
            if temp != None:
                return temp.lookupVariable(name)
        return None

