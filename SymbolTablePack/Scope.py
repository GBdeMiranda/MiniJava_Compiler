#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:26:43 2019

@author: vitor
"""

class Scope:
    
    def enterScope(self,name):
        pass
    
    def lookupVariable(self,name):
        pass

    def lookupMethod(self, name, paramNmaes, paramTypes, returnType):
        pass

    def exitScope(self,name):
        pass

    def printt(self, identLevel):
        pass
