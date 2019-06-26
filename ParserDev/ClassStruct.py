#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 04:17:24 2019

@author: vitor
"""
from copy import *

class ClassStruct:
    def __init__(self, name, extends = None):
        self.name = name
        self.extends = ''
        if extends is not None:
            self.extends = extends        
        