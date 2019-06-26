#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 20:24:59 2019

@author: vitor
"""
import sys
from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from SymbolTable import SymbolTable
from InfoFunction import InfoFunction

class CompleteClassSymbolTableListener(MiniJavaListener):

    def __init__(self):
        self.table = [SymbolTable()] #lista com as tabelas de cada classe.
        self.tableAtual = self.table[0]
        self.funcAux = InfoFunction()

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
                            linha = ctx.getChild(i).ID(0).symbol.line
                            coluna = ctx.getChild(i).ID(0).symbol.column
                            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                            sys.exit()
                        else:
                            self.table[i].extending(self.table[j])
                if flag == 0:
                    print("classe '" + self.table[i].name[0] + "' herda da classe '" + self.table[i].extendedName + "'. Mas a classe '" + self.table[i].extendedName + "' não existe!")
                    linha = ctx.getChild(i).ID(0).symbol.line
                    coluna = ctx.getChild(i).ID(0).symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                    sys.exit()

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
                    linha = ctx.getChild(i).ID(0).symbol.line
                    coluna = ctx.getChild(i).ID(0).symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                    sys.exit()

                    
    # Enter a parse tree produced by MiniJavaParser#mainClass.
    def enterMainClass(self, ctx:MiniJavaParser.MainClassContext):
        name = ctx.ID(0).getText()
        self.tableAtual.addSymbol(name,"classe")

    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        newTable = SymbolTable()
        name = ctx.ID(0).getText()
        newTable.addSymbol(name,"classe") 
        
        if ctx.getChild(2).getText() != '{':
            newTable.extendedName = ctx.getChild(3).getText()
        
        self.table.append(newTable)
        self.tableAtual = self.table[-1]       