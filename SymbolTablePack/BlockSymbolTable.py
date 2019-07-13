#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 00:38:15 2019

@author: vitor
"""

from SymbolTablePack import SymbolTableNew, Scope, BlockSymbolTable, ClassSymbolTable, MethodSymbolTable, Variable

class BlockSymbolTable(Scope):
    parent = Scope()
    vars_dictionary = dict()
    blocks_dictionary = dict()
    
    def __init__(self, parent):
        self.parent = parent

    def enterScope(self, name):
        try:
            return self.blocks_dictionary[str(name)]
        except:
            return False
    
    def exitScope(self):
        return self.parent
    
    def addBlock(self, name):
        self.blocks_dictionary[str(name)] = BlockSymbolTable(self)

    def localVarLookup(self, name):
        try:
            return self.vars_dictionary[str(name)]
        except:
            print("Nao existe a variavel procurada")
            return False
    
    def lookupVariable(self, name):
        try:
            return self.vars_dictionary[str(name)]
        except:
            if parent!=None:
                return self.parent.lookupVariable(name)
            else:
                return None
    
    def lookupMethod(self, name, paramNames, paramTypes, returnType):
        return self.parent.lookupMethod(name, paramNames, paramTypes, returnType)
    
    def printIdentation(self, identLevel):
        print("")
        for i in range(identLevel):
            print("\t")
    
    def printt(self, identLevel):
        keys = sorted(self.vars_dictionary.keys())
        for i in range(len(keys)):
            self.printIdentation(identLevel)
            print(self.vars_dictionary[keys[i]].getType() + " " + self.vars_dictionary[keys[i]].getName() + ";")

        keys = sorted(self.blocks_dictionary.keys())
        for i in range(len(keys)):
            self.blocks_dictionary[keys[i]].printt(identLevel+1)        