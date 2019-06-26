#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 20:24:59 2019

@author: vitor
"""
import sys
from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaBaseListener import MiniJavaBaseListener
from SymbolTable import SymbolTable
from InfoFunction import InfoFunction

class CompleteClassSymbolTableListener(MiniJavaBaseListener):

    def __init__(self):
        self.table = [SymbolTable()] #lista com as tabelas de cada classe.
        self.tableAtual = self.table[0]
        self.rodada = 0
        self.funcAux = InfoFunction()


    def enterProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#program.
    #para cada classe na table de classes que for filha de outra 
    #classe define um ponteiro para a classe pai
    def exitProgram(self, ctx:MiniJavaParser.ProgramContext):
        for i in range(len(self.table)):
            if self.table[i].extendedName != "":
                flag = 0;
                for j in range(len(self.table)):
                    if self.table[i].extendedName == self.table[j].name[0] :
                        flag = 1
                        if i==j:
                            print("Não é possível a classe herdar ela própria!")
                        else:
                            self.table[i].extending(self.table[j])
                if flag == 0:
                    print("classe '" + self.table[i].name[0] + "' herda da classe '" + self.table[i].extendedName + "'. Mas a classe '" + self.table[i].extendedName + "' não existe!")

        for i in range(len(self.table)):
            if self.table[i].visitado == 0:
                self.table[i].visitado = 1
                name = self.table[i].name[0]
                p = self.table[i].extendedTable
                
                while p != None and p.visitado == 0 and p.name[0] != name:
                    p.visitado = 1
                    p = p.extendedTable
                if p != None and p.name[0] == name:
                    print("Erro de Herança Circular")

                    
    # Enter a parse tree produced by MiniJavaParser#mainClass.
    def enterMainClass(self, ctx:MiniJavaParser.MainClassContext):
        name = ctx.ID(0).getText()
        self.tableAtual.addSymbol(name,"classe")


    # Exit a parse tree produced by MiniJavaParser#mainClass.
    def exitMainClass(self, ctx:MiniJavaParser.MainClassContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        newTable = SymbolTable()
        name = ctx.ID(0).getText()
        newTable.addSymbol(name,"classe") 
        
        if ctx.getChild(2).getText() != '{':
            newTable.extendedName = ctx.getChild(3).getText()
        
        self.table.append(newTable)
        self.tableAtual = self.table[-1]
            
        


    # Exit a parse tree produced by MiniJavaParser#classDecl.
    def exitClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#var.
    def enterVar(self, ctx:MiniJavaParser.VarContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#var.
    def exitVar(self, ctx:MiniJavaParser.VarContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#metodo.
    def enterMetodo(self, ctx:MiniJavaParser.MetodoContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#metodo.
    def exitMetodo(self, ctx:MiniJavaParser.MetodoContext):
        pass


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
        pass

    # Exit a parse tree produced by MiniJavaParser#nestedStatement.
    def exitNestedStatement(self, ctx:MiniJavaParser.NestedStatementContext):
        pass


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