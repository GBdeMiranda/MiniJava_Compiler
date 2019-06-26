#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 23:01:19 2019

@author: vitor
"""
import sys
from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from SymbolTable import SymbolTable
from InfoFunction import InfoFunction

class MiniJavaBaseListener(MiniJavaListener):
    
    def __init__(self):
        self.table = [SymbolTable()] #lista com as tabelas de cada classe.
        self.tableAtual = self.table[0]
        self.rodada = 0
        self.funcAux = InfoFunction()

#    def enterParametros(self, ctx:MiniJavaParser.ParametrosContext):
#        ttype = ctx.getChild(0)
#        ident = ctx.getChild(1)
#        self.table.addSymbol(str(ident),str(ttype))

    # Enter a parse tree produced by MiniJavaParser#program.
    def enterProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#program.
    def exitProgram(self, ctx:MiniJavaParser.ProgramContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#mainClass.
    def enterMainClass(self, ctx:MiniJavaParser.MainClassContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#mainClass.
    def exitMainClass(self, ctx:MiniJavaParser.MainClassContext):
        pass


    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        pass

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


        
