#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 19:46:13 2019

@author: vitor
"""

from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from SymbolTablePack import *
from IR_PAI import *

from Temporary import Temporary
from Label import Label

class BuildSymbolTableListener(MiniJavaListener):

    symbolTable = SymbolTableNew()
    currentScope = Scope()
    blockNumber = int()
    errorDetected = bool()
          
    def __init__(self):
        self.blockNumber = 0
        self.currentScope = self.symbolTable
        self.errorDetected = False
        
    def getFirstScope(self):
        return self.symbolTable
    
    def nextBlockNumber(self):
        self.blockNumber = self.blockNumber + 1
        return ("" + self.blockNumber)
    
    def getTypeStr(self, ttype):
        typpe = ttype.getText()
        return typpe     
        
    
    # Enter a parse tree produced by MiniJavaParser#program.
    def enterProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#program.
    def exitProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#mainClass.
    def enterMainClass(self, ctx:MiniJavaParser.MainClassContext):
        name = str(ctx.ID(0).getText())
        self.symbolTable.addClass(name)
        self.currentScope = self.symbolTable.enterScope(name)
        
        paramNames = ["output"]
        paramTypes = ["int"]
        
        cst = cp.copy(self.currentScope)
        cst.addMethod("System.out.println", paramNames, paramTypes, "void")
        
        paramTypes[0] = "String[]"
        paramNames[0] = str(ctx.ID(1).getText())
        
        cst.addMethod("main", paramNames, paramTypes, "void")
        
        self.currentScope = self.currentScope.enterScope("main")
        
        
        
    # Exit a parse tree produced by MiniJavaParser#mainClass.
    def exitMainClass(self, ctx:MiniJavaParser.MainClassContext):
        self.currentScope = self.currentScope.exitScope()
        self.currentScope = self.currentScope.exitScope()

    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        #caso nao extenda nenhuma classe
        if ctx.getChild(2).getText() == '{':
            name = str(ctx.ID(0).getText())
            self.symbolTable.addClass(name)
            self.currentScope = self.symbolTable.enterScope(name)
            
            paramNames = ["output"]
            paramTypes = ["int"]
        
            cst = cp.copy(self.currentScope)
            cst.addMethod("System.out.println", paramNames, paramTypes, "void")
        else:
            name = str(ctx.ID(0).getText())
            nameParent = str(ctx.ID(1).getText())
            self.symbolTable.addClass(name)
            self.currentScope = self.symbolTable.enterScope(name)
                      

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


    # Enter a parse tree produced by MiniJavaParser#metodo.
    def enterMetodo(self, ctx:MiniJavaParser.MetodoContext):
        cst = cp.copy(self.currentScope)
        returnType = self.getTypeStr(ctx.tipo())
        name = ctx.ID().getText()
        paramNames = ["this"]
        paramTypes = [cst.getName()]
        
        if ctx.getChild(4) != ")":
            for i in range(len(ctx.parametros().tipo())):
                paramNames.append(ctx.parametros().ID(i).getText())
                paramTypes.append(ctx.parametros().tipo(i).getText())
        
        cst.addMethod(name, paramNames, paramTypes, returnType)
        self.currentScope = cst.enterScope(name)
        

    # Exit a parse tree produced by MiniJavaParser#metodo.
    def exitMetodo(self, ctx:MiniJavaParser.MetodoContext):
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

    
    bstNestedStatement = BlockSymbolTable(None)

    # Enter a parse tree produced by MiniJavaParser#nestedStatement.
    def enterNestedStatement(self, ctx:MiniJavaParser.NestedStatementContext):
        self.bstNestedStatement = cp.copy(self.currentScope)
        blockNum = self.nextBlockNumber()
        self.bstNestedStatement.addBlock(blockNum)
        self.currentScope = self.bstNestedStatement.enterScope( blockNum )
        
        

    # Exit a parse tree produced by MiniJavaParser#nestedStatement.
    def exitNestedStatement(self, ctx:MiniJavaParser.NestedStatementContext):
        self.currentScope = self.bstNestedStatement
        


    # Enter a parse tree produced by MiniJavaParser#ifElseStatement.
    def enterIfElseStatement(self, ctx:MiniJavaParser.IfElseStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#ifElseStatement.
    def exitIfElseStatement(self, ctx:MiniJavaParser.IfElseStatementContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#whileStatement.
    def enterWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#whileStatement.
    def exitWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#printStatement.
    def enterPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#printStatement.
    def exitPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#variableAssignmentStatement.
    def enterVariableAssignmentStatement(self, ctx:MiniJavaParser.VariableAssignmentStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#variableAssignmentStatement.
    def exitVariableAssignmentStatement(self, ctx:MiniJavaParser.VariableAssignmentStatementContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def enterArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def exitArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#exp.
    def enterExp(self, ctx:MiniJavaParser.ExpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#exp.
    def exitExp(self, ctx:MiniJavaParser.ExpContext):
        pass


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
        pass


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
        pass


    # Enter a parse tree produced by MiniJavaParser#aexp_aux.
    def enterAexp_aux(self, ctx:MiniJavaParser.Aexp_auxContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#aexp_aux.
    def exitAexp_aux(self, ctx:MiniJavaParser.Aexp_auxContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#mexp.
    def enterMexp(self, ctx:MiniJavaParser.MexpContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#mexp.
    def exitMexp(self, ctx:MiniJavaParser.MexpContext):
        pass


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


    