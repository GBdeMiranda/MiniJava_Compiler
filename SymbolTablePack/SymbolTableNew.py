#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:33:26 2019

@author: vitor
"""
from SymbolTablePack import SymbolTableNew, Scope, BlockSymbolTable, ClassSymbolTable, MethodSymbolTable, Variable

class SymbolTableNew(Scope):    
    def __init__(self):
        self.dictionaryClasses = dict()
        
    def addClass(self, name, parentName=None):
        if parentName == None:
            self.addClass(self, name, None)
        else:
            newClass = ClassSymbolTable(self, name, parentName)
            self.dictionaryClasses[str(name)] = newClass

    def enterScope(self, name):
        return self.dictionaryClasses[str(name)]
    
    def exitScope(self):
        return None

    def getClass(self, name):
        if(self.isClass(self,name)):
            return ClassSymbolTable(self.dictionaryClasses[str(name)])
        else:
            return None
        
    def isClass(self, name):
        return (name in self.dictionaryClasses.keys())

    def lookupVariable(self, name):
        return None

    def lookupMethod(self,name):
        return False
    
    def printt(self, identLevel):
        print("-------Symbol Table-------")
        keys = sorted(self.dictionaryClasses.keys())
        for i in range(len(keys)):
            self.dictionaryClasses[keys[i]].printt(identLevel + 1)
            print()
              
    def getClasses(self):
        return self.dictionaryClasses