#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 22:51:53 2019

@author: gbm
"""

class Label():
	nextNumber = int()
	num  = int()
	printBefore = bool()
	
	def __init__(self, printBefore):
		self.num = self.nextNumber
		self.nextNumber += 1
		self.printBefore = printBefore
	
	def getName():
		return ("L" + self.num)
	
	def toString():
		return ("L" + self.num + ":")
	
	def getNum():
		return (self.num)
	
	def reset():
		self.nextNumber = -1