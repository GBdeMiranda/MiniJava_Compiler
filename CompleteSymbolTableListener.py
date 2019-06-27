#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:06:59 2019

@author: vitor
"""
import sys
from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from InfoFunction import InfoFunction
from SymbolTable import SymbolTable
import copy as cp

class CompleteSymbolTableListener(MiniJavaListener):
    
    def __init__(self,table):
        self.table = table #lista com as tabelas de cada classe.
        self.tableAtual = self.table[0]
        self.rodada = 0
        self.funcAux = InfoFunction()
        self.iterador = 0 #usado para saber em qual classe esta na lista table
        

    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        self.iterador = self.iterador + 1
        self.tableAtual = self.table[self.iterador]

    
    # Enter a parse tree produced by MiniJavaParser#var.
    def enterVar(self, ctx:MiniJavaParser.VarContext):
        ttype = ctx.tipo().getText()
        name = ctx.ID().getText()
        
        flag = 0
        #caso o tipo seja ID verifica se existe uma classe com aquele nome
        if(ttype != 'int[]' and ttype != 'boolean' and ttype != 'int'):
            for i in range(len(self.table)):
                className = self.table[i].name[0]
                if className == ttype:
                    flag = 1    
            if flag == 0:
                print("Variável '" + name + "' declarada como" + ttype + " mas a classe não existe")
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                sys.exit()
            else:
                self.tableAtual.addSymbol(name,ttype)
        else:
            self.tableAtual.addSymbol(name,ttype)


    # Enter a parse tree produced by MiniJavaParser#metodo.
    def enterMetodo(self, ctx:MiniJavaParser.MetodoContext):
        ttype = ctx.tipo().getText()
        ident = ctx.ID().getText()
        
        flag = 0
        
        #caso o tipo seja ID verifica se existe uma classe com aquele nome
        if(ttype != 'int[]' and ttype != 'boolean' and ttype != 'int'):
            for i in range(len(self.table)):
                className = self.table[i].name[0]
                if className == ttype:
                    flag = 1    
            if flag == 0:
                print("Método '" + ttype + "' tem retorno do tipo " + ttype + " mas a classe não existe")
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                sys.exit()
            else:
                self.tableAtual.addSymbol(ident,ttype)
                
                self.funcAux.setName(ident)
                self.funcAux.setReturnType(ttype)
                #escopo do metodo
                newTable = SymbolTable(self.tableAtual)
                self.tableAtual = self.tableAtual.descendants[-1]
        else:
            self.tableAtual.addSymbol(ident,ttype)            
            self.funcAux.setName(ident)
            self.funcAux.setReturnType(ttype)
            
            #escopo do metodo
            newTable = SymbolTable(self.tableAtual)
            self.tableAtual = self.tableAtual.descendants[-1]
        
    # Exit a parse tree produced by MiniJavaParser#metodo.
    def exitMetodo(self, ctx:MiniJavaParser.MetodoContext):
        self.tableAtual = self.tableAtual.previous
        newFunction = InfoFunction()
        newFunction = cp.copy(self.funcAux)
        self.tableAtual.addFunction(newFunction)
        self.funcAux.cleanFunction()


    # Enter a parse tree produced by MiniJavaParser#parametros.
    def enterParametros(self, ctx:MiniJavaParser.ParametrosContext):
        for i in range(len(ctx.tipo())):
            name = ctx.ID(i).getText()
            ttype = ctx.tipo(i).getText()
    
            if(ttype != 'int[]' and ttype != 'boolean' and ttype != 'int'):
                for i in range(len(self.table)):
                    className = self.table[i].name[0]
                    if className == ttype:
                        flag = 1    
                if flag == 0:
                    print("Parametro '" + str(ctx.ID(i).getText()) + "' é do tipo '" + ttype + "'' mas a classe não existe")
                    linha = ctx.ID(i).symbol.line
                    coluna = ctx.ID(i).symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                    sys.exit()


            self.funcAux.addParamsType(ttype)
            self.tableAtual.addSymbol(name,ttype)