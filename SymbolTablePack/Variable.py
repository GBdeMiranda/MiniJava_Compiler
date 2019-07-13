#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 02:50:19 2019

@author: gbm
"""

class Variable(object):
    
    name = str()
    type_ = str()
    offset = int()    # Used by class member variables for an offset
    register = str()    # Used by local variables to store the register string mapped to it by the register allocator
    
    def __init__(self, name, type_, x = -1):
        self.name = name
        self.type_ = type_
        if(type(x) == int):
            self.offset   = x
            self.register = None
        elif(type(x) == str):
            self.offset   = -1
            self.register = x

    def setRegister(self, reg):
        self.register = reg

    def setOffset(self, x):
        self.offset = x

    def getName(self):
        return self.name

    def __str__(self):
        return self.__name__

    def getType(self):
        return self.type_

    def getOffset(self):
        return self.offset

    def getRegister(self):
        return self.register

