#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 22:15:54 2019

@author: vitor
"""

from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from SymbolTablePack import *
from IR_PAI import *


from Temporary import Temporary
from Label import Label

import copy as cp

class IntermediateRepresentationListener(MiniJavaListener):

    currentScope = ''
    blockNumber = int()
    IRList = []
    labels = dict()    
    workList = dict() #labels to methods 
    
    def __init__(self, symbolTable):
        self.currentScope = symbolTable
        self.blockNumber = 0
    
    def getLabels(self):
        return self.labels
    
    def getWorkList(self):
        return self.workList
    
    def getIR(self):
        return self.IRList
    
    def addLabel(self, q, p):
        if type(p) == bool:            
            temp = self.labels.get(q)
            
            if temp == None:
                temp = []
                
            l = Label(p)
            temp.append(l)
            self.labels[q] = temp
            
            return l.getName()
        else:
            temp = self.labels.get(q)
            if temp == None:
                temp = []
            temp.append(p)
            self.labels[q] = temp
            return p.getName()
        
    #Create unique numbers for the blocsk in each scope
    def nextBlockNumber(self):
        self.blockNumber = self.blockNumber + 1
        return ("" + self.blockNumber)
        
        
    # Enter a parse tree produced by MiniJavaParser#program.
    def enterProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#program.
    def exitProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#mainClass.
    def enterMainClass(self, ctx:MiniJavaParser.MainClassContext):
        name = str(ctx.ID(0).getText())
        self.currentScope = self.currentScope.enterScope(name)
        self.currentScope = self.currentScope("main")
                      
        
    # Exit a parse tree produced by MiniJavaParser#mainClass.
    def exitMainClass(self, ctx:MiniJavaParser.MainClassContext):
        labelName = self.addLabel(self.IRList.get(0), True)
        
        self.IRList.append( CallIR("System.exit", "0", None) )
        self.workList["main"] = labelName
        self.currentScope = self.currentScope.exitScope()
        self.currentScope = self.currentScope.exitScope()
        
    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        #caso nao extenda nenhuma classe
        name = str(ctx.ID(0).getText())
        self.currentScope = self.currentScope.enterScope(name)
                      
    # Exit a parse tree produced by MiniJavaParser#classDecl.
    def exitClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):  
        self.currentScope = self.currentScope.exitScope()
        
    # Enter a parse tree produced by MiniJavaParser#var.
    def enterVar(self, ctx:MiniJavaParser.VarContext):
        typee = self.getTypeStr(ctx.tipo())
        bst = cp.copy(self.currentScope)
        
        bst.addVariable(ctx.ID().getText(),typee)

    # Exit a parse tree produced by MiniJavaParser#var.
    def exitVar(self, ctx:MiniJavaParser.VarContext):
        pass


    sizeMetodo = int()
    # Enter a parse tree produced by MiniJavaParser#metodo.
    def enterMetodo(self, ctx:MiniJavaParser.MetodoContext):
        name = ctx.ID().getText()
        self.currentScope = self.currentScope.enterScope(name)
        self.sizeMetodo = len(self.IRList)
        
    # Exit a parse tree produced by MiniJavaParser#metodo.
    def exitMetodo(self, ctx:MiniJavaParser.MetodoContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        self.IRList.append(ReturnIR(t))
        
        labelName = addLabel(self.IRList[self.sizeMetodo], True)
        self.workList[ctx.ID(0).getText()] = labelName
        
        self.currentScope = self.currentScope.exitScope()
        
        

    # Enter a parse tree produced by MiniJavaParser#parametros.
    def enterParametros(self, ctx:MiniJavaParser.ParametrosContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#parametros.
    def exitParametros(self, ctx:MiniJavaParser.ParametrosContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#intVet.
    def enterIntVet(self, ctx:MiniJavaParser.IntVetContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#intVet.
    def exitIntVet(self, ctx:MiniJavaParser.IntVetContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#bool.
    def enterBool(self, ctx:MiniJavaParser.BoolContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#bool.
    def exitBool(self, ctx:MiniJavaParser.BoolContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#int.
    def enterInt(self, ctx:MiniJavaParser.IntContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#int.
    def exitInt(self, ctx:MiniJavaParser.IntContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#id.
    def enterId(self, ctx:MiniJavaParser.IdContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#id.
    def exitId(self, ctx:MiniJavaParser.IdContext):
        pass

    

    # Enter a parse tree produced by MiniJavaParser#nestedStatement.
    def enterNestedStatement(self, ctx:MiniJavaParser.NestedStatementContext):
        blockNum = nextBlockNumber()
        self.currentScope = self.currentScope.enterScope(blockNum)        
        

    # Exit a parse tree produced by MiniJavaParser#nestedStatement.
    def exitNestedStatement(self, ctx:MiniJavaParser.NestedStatementContext):
        self.currentScope = self.currentScope.exitScope()
        
    l1IF = bool()
    l2IF = bool()
    # Enter a parse tree produced by MiniJavaParser#ifElseStatement.
    def enterIfElseStatement(self, ctx:MiniJavaParser.IfElseStatementContext):
        self.l1IF = Label(True)
        self.l2IF = Label(False)
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")

        self.IRList.append(ConditionalJumpIR(t, self.l1IF))
        
        

    # Exit a parse tree produced by MiniJavaParser#ifElseStatement.
    def exitIfElseStatement(self, ctx:MiniJavaParser.IfElseStatementContext):
        self.IRList.append(UnconditionalJumpIR(self.l2IF))
        self.addLabel(self.IRList[-2],self.l1IF)
        self.addLabel(self.IRList[-1],self.l2IF)


    l1W = bool()
    l2W = bool()
    # Enter a parse tree produced by MiniJavaParser#whileStatement.
    def enterWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        self.l1W = Label(False)
        self.l2W = Label(False)
        
        self.addLabel(self.IRList[-1],self.l1W)
        

    # Exit a parse tree produced by MiniJavaParser#whileStatement.
    def exitWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        self.IRList.append(ConditionalJumpIR(t,self.l2W))
        self.IRList.append(UnconditionalJumpIR(self.l1W))
        self.addLabel(self.IRList[-1],self.l2W)
        


    # Enter a parse tree produced by MiniJavaParser#printStatement.
    def enterPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#printStatement.
    def exitPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        self.IRList.append(ParameterIR(t))
        self.IRList.append(CallIR("System.out.println","1",None))
        


    # Enter a parse tree produced by MiniJavaParser#variableAssignmentStatement.
    def enterVariableAssignmentStatement(self, ctx:MiniJavaParser.VariableAssignmentStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#variableAssignmentStatement.
    def exitVariableAssignmentStatement(self, ctx:MiniJavaParser.VariableAssignmentStatementContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        self.IRList.append(CopyIR(t,self.currentScope.lookupVariable(ctx.ID(0).getText())))
        
        


    # Enter a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def enterArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def exitArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        self.IRList.append(IndexedAssignmentIR2(t,self.currentScope.lookupVariable(ctx.ID(0).getText())))


    # Enter a parse tree produced by MiniJavaParser#exp.
    def enterExp(self, ctx:MiniJavaParser.ExpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#exp.
    def exitExp(self, ctx:MiniJavaParser.ExpContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        temp = Temporary()
        r = Variable(temp.toString(), "temporary")
        temp = Temporary()
        s = Variable(temp.toString(), "temporary")
        self.IRList.append(AssignmentIR("&&",t,r,s))
        

    # Enter a parse tree produced by MiniJavaParser#exp_aux.
    def enterExp_aux(self, ctx:MiniJavaParser.Exp_auxContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#exp_aux.
    def exitExp_aux(self, ctx:MiniJavaParser.Exp_auxContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#rexp.
    def enterRexp(self, ctx:MiniJavaParser.RexpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#rexp.
    def exitRexp(self, ctx:MiniJavaParser.RexpContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        temp = Temporary()
        r = Variable(temp.toString(), "temporary")
        temp = Temporary()
        s = Variable(temp.toString(), "temporary")
        self.IRList.append(AssignmentIR("<",t,r,s))



    # Enter a parse tree produced by MiniJavaParser#rexp_aux.
    def enterRexp_aux(self, ctx:MiniJavaParser.Rexp_auxContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#rexp_aux.
    def exitRexp_aux(self, ctx:MiniJavaParser.Rexp_auxContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#aexp.
    def enterAexp(self, ctx:MiniJavaParser.AexpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#aexp.
    def exitAexp(self, ctx:MiniJavaParser.AexpContext):
        temp = Temporary()
        t = Variable(temp.toString(), "temporary")
        temp = Temporary()
        r = Variable(temp.toString(), "temporary")
        temp = Temporary()
        s = Variable(temp.toString(), "temporary")
        self.IRList.append(AssignmentIR("+",t,r,s))

    # Enter a parse tree produced by MiniJavaParser#mexp_aux.
    def enterMexp_aux(self, ctx:MiniJavaParser.Mexp_auxContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#mexp_aux.
    def exitMexp_aux(self, ctx:MiniJavaParser.Mexp_auxContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#sexp.
    def enterSexp(self, ctx:MiniJavaParser.SexpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#sexp.
    def exitSexp(self, ctx:MiniJavaParser.SexpContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#pexp.
    def enterPexp(self, ctx:MiniJavaParser.PexpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#pexp.
    def exitPexp(self, ctx:MiniJavaParser.PexpContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#pexp_aux.
    def enterPexp_aux(self, ctx:MiniJavaParser.Pexp_auxContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#pexp_aux.
    def exitPexp_aux(self, ctx:MiniJavaParser.Pexp_auxContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#exps.
    def enterExps(self, ctx:MiniJavaParser.ExpsContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#exps.
    def exitExps(self, ctx:MiniJavaParser.ExpsContext):
        pass


    