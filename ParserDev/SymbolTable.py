#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 04:17:24 2019

@author: vitor
"""
#class No:
#    def __init__(self, name, ttype, scope):
#        self.name = name
#        self.ttype = ttype
#        self.scope = scope

import InfoFunction
import SymbolTable

class SymbolTable:
    
    def __init__(self,previous=None):
        self.name = []
        self.ttype = []
        self.functions = []
        self.previous = previous    # Referencia para o pai, ou seja, o escopo o qual ele ta inserido
        self.descendants = []       # Referencia para os filhos.. Cada abre e fecha colchete 
                                    # Gera um novo filho pois inicia um novo escopo  
                                 
        self.extendedTable = None   
        self.extendedName = ""      # O nome de quem foi extendido
        
        self.visitado = 0

        if previous is not None:
            previous.addDescendant(self)

    def extending(self, newTable:SymbolTable ):
        self.extendedTable = newTable
        
    def addSymbol(self, name, ttype):
        self.name.append(name)
        self.ttype.append(ttype)

    def addDescendant (self,table):
        self.descendants.append(table)
        
    def modifySymbol(self, name, ttype):
        if name in self.name:
            i = self.name.index(name)
            self.ttype[i] = ttype
            return True
        else:
            return False

    def findID(self, name):
        pos = -1
        p = self
        while pos == -1 and p != None:
            if p.ttype[0] != 'classe':
                try:
                    pos = self.p.name.index(name)
                except Exception:
                    p = p.previous 
            else:
                try:
                    pos = self.p.name.index(name)
                except Exception:
                    p = p.extendedTable
        if p.name.index(name) == p.name[pos]:
            return p.ttype[pos]
        return None
    
    def addFunction(self, function):
        self.functions.append(function)
        
    def findFunction(self,name):
        for i in len(self.functions):
            if self.functions[i].getName() == name:
                return self.functions[i]
        #funcao nao existe
        return False
            