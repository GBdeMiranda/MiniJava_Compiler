#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 04:17:24 2019

@author: vitor
"""
from copy import *

class InfoFunction:
    
    def __init__(self):
        self.name = ''
        self.returnType = ''
        self.paramsType = []

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setReturnType(self,ttype):
        self.returnType = ttype
    
    def getReturnType(self):
        return self.returnType
        
    def addParamsType(self, param):
        self.paramsType.append(param)
    
    def getParamsList(self):
        return self.paramsType
    
    def cleanFunction(self):
        self.name = []
        self.returnType = []
        self.paramsType = []