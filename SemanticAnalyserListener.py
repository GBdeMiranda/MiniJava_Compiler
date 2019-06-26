#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 02:50:19 2019

@author: vitor
"""
import sys
from antlr4 import *
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from SymbolTable import SymbolTable
from InfoFunction import InfoFunction

class SemanticAnalyserListener(MiniJavaListener):
    
    def __init__(self,table):
        self.table = table #lista com as tabelas de cada classe.
        self.tableAtual = self.table[0]
        self.funcAux = InfoFunction()
        self.iterador = 0 #usado para saber em qual classe esta na lista table
        self.iteradorMetodo = 0
        self.dicionarioTipos = dict()
        self.funcAtual = 0
    
    #retorna true se a é subtipo de b, ou seja, a extends b ou a extends... extends b
    def ehSubtipo(a, b):
        if a == b:
            return True
        else:
            son = 0
            for i in range(len(self.table)):
                if self.table[i].name[0] == a:
                    son = self.table[i]
                    break
            father = son.extendedTable
            while father != None:
                if father.name[0] == b:
                    return True
                father = father.extendedTable            
            return False
                
    # Enter a parse tree produced by MiniJavaParser#classDecl.
    def enterClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        self.iterador = self.iterador+1
        self.tableAtual = self.table[self.iterador]

    # Exit a parse tree produced by MiniJavaParser#classDecl.
    def exitClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        self.iteradorMetodo = 0

    # Enter a parse tree produced by MiniJavaParser#metodo.
    def enterMetodo(self, ctx:MiniJavaParser.MetodoContext):
        self.funcAtual = self.table[self.iterador].functions[self.iteradorMetodo]
        self.tableAtual = self.tableAtual.descendants[self.iteradorMetodo]
        self.iteradorMetodo = self.iteradorMetodo + 1
        

    # Exit a parse tree produced by MiniJavaParser#metodo.
    def exitMetodo(self, ctx:MiniJavaParser.MetodoContext):
        returnType = self.dicionarioTipos[ctx.exp().__hash__()]
        #verifica se o retorno é do mesmo tipo da função
        if returnType == 'int' or returnType == 'int[]' or returnType == 'boolean':
            if returnType != self.funcAtual.returnType:
                print("Retorno diferente do tipo da função")
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                sys.exit()
        else:
            if not self.ehSubtipo(returnType, self.funcAtual.returnType):
                print("Retorno diferente do tipo da função")
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                sys.exit()
        self.tableAtual = self.tableAtual.previous
      
    # Exit a parse tree produced by MiniJavaParser#ifElseStatement.
    def exitIfElseStatement(self, ctx:MiniJavaParser.IfElseStatementContext):
        tipo = self.dicionarioTipos[ctx.exp().__hash__()]
        if(tipo != 'boolean'):
            print("Expressão do condicional deve ser boolean.")
            linha = ctx.LPAREN().symbol.line
            coluna = ctx.LPAREN().symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                    

    # Exit a parse tree produced by MiniJavaParser#whileStatement.
    def exitWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        aux = ctx.exp()
        tipo = self.dicionarioTipos[aux.__hash__()]
        if(tipo != 'boolean'):
            print("Expressão do condicional deve ser boolean.")
            linha = ctx.exp().symbol.line
            coluna = ctx.exp().symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
            

    # Exit a parse tree produced by MiniJavaParser#printStatement.
    def exitPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        tipo = self.dicionarioTipos[ctx.exp().__hash__()]
        #verifica se o tipo do argumento do system.out.println é inteiro
        if tipo != 'int':
            print("\nO argumento para a impressão deve ser do tipo 'int'")
            linha = ctx.exp().symbol.line
            coluna = ctx.exp().symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" .\n" )

        
    # Exit a parse tree produced by MiniJavaParser#variableAssignmentStatement.
    def exitVariableAssignmentStatement(self, ctx:MiniJavaParser.VariableAssignmentStatementContext):
        name = ctx.ID().getText()
        tipo1 = self.tableAtual.findID(name)
        if tipo1 == None:
            print("Variavel '" + name + "' não declarada!")
        else:         
            tipo2 = self.dicionarioTipos[ctx.exp().__hash__()]
            if tipo1 == 'int' or tipo1 == 'boolean' or tipo1 == 'int[]':
                if tipo1 != tipo2:
                    print("Erro na atribuição pois as variaveis são de tipos diferentes!")
                    linha = ctx.ID().symbol.line
                    coluna = ctx.ID().symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
            else:
                if tipo2 != 'null' and not(self.ehSubtipo(tipo2, name)) :
                    print("Erro na atribuição pois as variaveis são de tipos diferentes!")
                    linha = ctx.ID().symbol.line
                    coluna = ctx.ID().symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                   
                    
    # Exit a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def exitArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        tipo_argumento = self.dicionarioTipos[ctx.exp(0).__hash__()]
        if tipo_argumento != 'int':
            print("A posição do array não é Inteiro.")
            linha = ctx.exp(0).symbol.line
            coluna = ctx.exp(0).symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                    
        name = ctx.ID().getText()
        tipo_id = self.tableAtual.find(name)

        if tipo_id == None:
            print("Variavel '" + name + "' não declarada!")
            linha = ctx.ID().symbol.line
            coluna = ctx.ID().symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                            
        if tipo_id != 'int[]':
            print("Variavel não é do tipo int[]")
            linha = ctx.ID().symbol.line
            coluna = ctx.ID().symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
        
        tipo_attr = self.dicionarioTipos[ctx.exp(1).__hash__()]
        if tipo_attr != 'int':
            print("tipo de atribuição não é inteiro")
            linha = ctx.exp(1).symbol.line
            coluna = ctx.exp(1).symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )        

    # Exit a parse tree produced by MiniJavaParser#exp.
    def exitExp(self, ctx:MiniJavaParser.ExpContext):
        #caso o número de filhos seja 1
        if ctx.getChildCount() == 1:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.rexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.rexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.exp_aux().__hash__()]
            if not(tipo_l == tipo_r and tipo_l == 'boolean'):
                print('Expressão do IF não é boolean!')
                linha = ctx.exp_aux().AND().symbol.line
                coluna = ctx.exp_aux().AND().symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )        
            self.dicionarioTipos[ctx.__hash__()] = 'boolean'
        

    # Exit a parse tree produced by MiniJavaParser#exp_aux.
    def exitExp_aux(self, ctx:MiniJavaParser.Exp_auxContext):
        if ctx.getChildCount() == 2:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.rexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.rexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.exp_aux().__hash__()]
            self.dicionarioTipos[ctx.__hash__()] = 'boolean'
            if not (tipo_l == tipo_r == 'boolean'):
                print('Operadores da operação do if não são boolean')
                linha = ctx.AND().symbol.line
                coluna = ctx.AND().symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )        
                  

    # Exit a parse tree produced by MiniJavaParser#rexp.
    def exitRexp(self, ctx:MiniJavaParser.RexpContext):
        if ctx.getChildCount() == 1:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.aexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.aexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.rexp_aux().__hash__()]
            operador = ctx.rexp_aux().getChild(0).getText()
            if tipo_l == tipo_r:
                if operador == '<':
                    if tipo_l != 'int':
                        print("Não é possível comparar '" + str(tipo_l) + "'s com o operador '" + str(operador) + "'.")
                        linha = ctx.rexp_aux().child(0).symbol.line
                        coluna = ctx.rexp_aux().child(0).symbol.column
                        print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                else:
                    if tipo_l != 'int' and tipo_l != 'boolean' and tipo_l != 'null':
                        print("Não é possível fazer a operação '" + operador + "' com variáveis '" + tipo_l)
                        linha = ctx.rexp_aux().child(0).symbol.line
                        coluna = ctx.rexp_aux().child(0).symbol.column
                        print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                        
            else:
                if tipo_l != 'null' and tipo_r != 'null':
                    print("Tipos não são os mesmos!")
                    linha = ctx.rexp_aux().child(0).symbol.line
                    coluna = ctx.rexp_aux().child(0).symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )

            self.dicionarioTipos[ctx.__hash__()] = 'boolean'


    # Exit a parse tree produced by MiniJavaParser#rexp_aux.
    def exitRexp_aux(self, ctx:MiniJavaParser.Rexp_auxContext):
        if ctx.getChildCount() == 2:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.aexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.aexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.rexp_aux().__hash__()]
            self.dicionarioTipos[ctx.__hash__()] = 'boolean'
            if ctx.LT() != None:
                if not (tipo_l == tipo_r and tipo_l == 'int') :
                    print("Operador lógico binário '<' deve ter ambos os lados da expressão do tipo 'int'.")
                    linha = ctx.child(0).symbol.line
                    coluna = ctx.child(0).symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )

            else:
                if not (tipo_l == tipo_r == 'int' or tipo_l == tipo_r == 'boolean'):
                    print("Comparação entre tipos diferentes no IF!")
                    linha = ctx.child(0).symbol.line
                    coluna = ctx.child(0).symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )


    # Exit a parse tree produced by MiniJavaParser#aexp.
    def exitAexp(self, ctx:MiniJavaParser.AexpContext):
        if ctx.getChildCount() == 1:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.mexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.mexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.aexp_aux().__hash__()]
            operador = ctx.aexp_aux().getChild(0).getText()
            if tipo_l == tipo_r and tipo_l == 'int':
                self.dicionarioTipos[ctx.__hash__()] = tipo_l
            else:
                print("Tipos não são os mesmos!")
                linha = ctx.aexp_aux().getChild(0).symbol.line
                coluna = ctx.aexp_aux().getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'
            

    # Exit a parse tree produced by MiniJavaParser#aexp_aux.
    def exitAexp_aux(self, ctx:MiniJavaParser.Aexp_auxContext):
        if ctx.getChildCount() == 2:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.mexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.mexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.aexp_aux().__hash__()]
            operador = ctx.aexp_aux().getChild(0).getText()
            if tipo_l == tipo_r and tipo_l == 'int':
                self.dicionarioTipos[ctx.__hash__()] = tipo_l
            else:
                print("Tipos não são os mesmos!")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'


    # Exit a parse tree produced by MiniJavaParser#mexp.
    def exitMexp(self, ctx:MiniJavaParser.MexpContext):
        if ctx.getChildCount() == 1:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.sexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.sexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.mexp_aux().__hash__()]
            operador = ctx.mexp_aux().getChild(0).getText()
            if tipo_l == tipo_r == 'int':
                self.dicionarioTipos[ctx.__hash__()] = tipo_l
            else:
                print("Tipos não são os mesmos!")
                linha = ctx.mexp_aux().getChild(0).symbol.line
                coluna = ctx.mexp_aux().getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'


    # Exit a parse tree produced by MiniJavaParser#mexp_aux.
    def exitMexp_aux(self, ctx:MiniJavaParser.Mexp_auxContext):
        if ctx.getChildCount() == 2:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.sexp().__hash__()]
        else:
            tipo_l = self.dicionarioTipos[ctx.sexp().__hash__()]
            tipo_r = self.dicionarioTipos[ctx.mexp_aux().__hash__()]
            if tipo_l == tipo_r == 'int':
                self.dicionarioTipos[ctx.__hash__()] = tipo_l
            else:
                print("Tipos não são os mesmos!")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'

    # Exit a parse tree produced by MiniJavaParser#sexp.
    def exitSexp(self, ctx:MiniJavaParser.SexpContext):
        if ctx.getChildCount() == 1:
            if ctx.TRUE() != None or ctx.FALSE() != None:
                self.dicionarioTipos[ctx.__hash__()] = 'boolean'
            elif ctx.INTEIRO() != None:
                self.dicionarioTipos[ctx.__hash__()] = 'int'
            elif ctx.NULL() != None:
                self.dicionarioTipos[ctx.__hash__()]  = 'null'
            elif ctx.pexp() != None:
                self.dicionarioTipos[ctx.__hash__()]  = self.dicionarioTipos[ctx.pexp().__hash__()]                
        elif ctx.getChildCount() == 2:
            tipo_d = self.dicionarioTipos[ctx.sexp().__hash__()]  
            if ctx.NOT() != None:
                if tipo_d == 'boolean':
                    self.dicionarioTipos[ctx.__hash__()]  = 'boolean'
                else:
                    print("Erro ao tentar aplicar o operador 'NOT' em uma variável do tipo '" + tipo_d + "'! ")
                    linha = ctx.getChild(0).symbol.line
                    coluna = ctx.getChild(0).symbol.column
                    print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
                    sys.exit()
            elif tipo_d == 'int':
                self.dicionarioTipos[ctx.__hash__()] = 'int'    
            else:
                print("Erro ao tentar aplicar operador '-' em uma variável do tipo '" + tipo_d + "'! ")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
                sys.exit()
        elif ctx.getChildCount() == 3:
            tipo_d = self.dicionarioTipos[ctx.pexp().__hash__()]
            if tipo_d != 'int[]':
                print("Não é possível aplicar o método length em uma variável do tipo '" + tipo_d+ "'!")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
                sys.exit()
            else:
                self.dicionarioTipos[ctx.__hash__()] = 'int'
        elif ctx.getChildCount() == 4:
            tipo_pexp = self.dicionarioTipos[ctx.pexp().__hash__()]
            tipo_exp = self.dicionarioTipos[ctx.exp().__hash__()]
            
            if tipo_exp != 'int':
                print("A posição do vetor deve ser um número inteiro.")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )        
            if tipo_pexp != 'int[]':
                print("A variável não é um vetor.")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
            self.dicionarioTipos[ctx.__hash__()] = 'int'
        else:
            tipo_exp = self.dicionarioTipos[ctx.exp().__hash__()]
            if tipo_exp != 'int':
                print("O tamanho de um vetor deve ser um número inteiro")
                linha = ctx.LBRACKET().symbol.line
                coluna = ctx.LBRACKET().symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )
            self.dicionarioTipos[ctx.__hash__()] = 'int[]'
                

    # Exit a parse tree produced by MiniJavaParser#pexp.
    def exitPexp(self, ctx:MiniJavaParser.PexpContext):
        if ctx.getChildCount() == 1:
            if ctx.ID() != None :
                tipo_id = self.tableAtual.findID(ctx.ID().getText())
                if tipo_id != None :
                    self.dicionarioTipos[ctx.__hash__()] = tipo_id
                else:
                    id_aux = ctx.ID()
                    print("Tipo de Erro: variável '"+ ctx.ID().getText() + "' não declarada!")
                    linha = id_aux.symbol.line
                    coluna = id_aux.symbol.column
                    print("Erro na linha "+ str(linha) +", coluna " + str(coluna) + ". " )
                    sys.exit()                    
            elif ctx.THIS() != None :
                tipo_classe = self.table[self.iterador].name[0]  #obter tipo da classe 
                self.dicionarioTipos[ctx.__hash__()] = tipo_classe
                
        elif ctx.getChildCount() == 2:
            if ctx.ID() != None :    
                for i in range(len(self.table)):
                    if(ctx.ID().getText() == self.table[i].name[0]):
                        if(ctx.pexp_aux().LPAREN() != None ):
                            funcaoAux = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(), len(self.table))
                            if funcaoAux != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o método usado")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )                            
                                sys.exit()
                            break
                        else:
                            idAux = self.table[i].findID(ctx.pexp_aux().getChild(1).getText())
                            if idAux != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o identificador usado")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )                            
                                sys.exit()
                            break

                            
                        
            elif ctx.THIS() != None :
                tipo_classe = self.table[self.iterador]  #obter tipo da classe 
                if(ctx.pexp_aux().LPAREN() != None ):
                    funcaoAux = tipo_classe.findFunction(ctx.pexp_aux().getChild(1).getText(), len(self.table))
                    if funcaoAux != None:
                        self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                    else: 
                        print("Não existe o método '" + ctx.pexp_aux().getChild(1).getText() + "'.")
                        linha = ctx.getChild(0).symbol.line
                        coluna = ctx.getChild(0).symbol.column
                        print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )        
                        sys.exit()
                else:
                    idAux = tipo_classe.findID(ctx.pexp_aux().getChild(1).getText())
                    if idAux != None:
                        self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                    else: 
                        print("Não existe a variavel '" + ctx.pexp_aux().getChild(1).getText() + "'.")
                        linha = ctx.getChild(0).symbol.line
                        coluna = ctx.getChild(0).symbol.column
                        print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )        
                        sys.exit()

        elif ctx.getChildCount() == 3:
            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.exp().__hash__()]
        
        elif ctx.getChildCount() == 4:
            if ctx.NEW() != None :
                for i in range(len(self.table)):
                    if(ctx.ID().getText() == self.table[i].name[0]):
                        self.dicionarioTipos[ctx.__hash__()] = ctx.ID().getText()
                        return
                print("Não existe o tipo '" + ctx.ID().getText() + "'.")
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +". " )
                sys.exit()
            else:
                tipo_exp = self.dicionarioTipos[ctx.exp().__hash__()]
                for i in range(len(self.table)):
                    if(tipo_exp == self.table[i].name[0]):
                        if ctx.pexp_aux().LPAREN() != None :
                            funcaoAux = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(), len(self.table))
                            if funcaoAux != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o método usado")                            
                                sys.exit()
                            break
                        else:
                            idAux = self.table[i].findID(ctx.pexp_aux().getChild(1).getText())
                            if idAux != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o identificador usado")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                            
                                sys.exit()
                            break
        else: #5 filhos
            tipo_id = ctx.ID().getText()
            for i in range(len(self.table)):
                if(tipo_id == self.table[i].name[0]):
                    if(ctx.pexp_aux().LPAREN() != None ):
                        funcaoAux = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(), len(self.table))
                        if funcaoAux != None:
                            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                        else:
                            print("Não existe o método usado")
                            linha = ctx.getChild(0).symbol.line
                            coluna = ctx.getChild(0).symbol.column
                            print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                            
                            sys.exit()
                        break           
                    else:
                        idAux = self.table[i].findID(ctx.pexp_aux().getChild(1).getText())
                        if idAux != None:
                            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                        else:
                            print("Não existe o identificador usado")
                            linha = ctx.getChild(0).symbol.line
                            coluna = ctx.getChild(0).symbol.column
                            print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                            
                            sys.exit()
                        break
                        

    # Exit a parse tree produced by MiniJavaParser#pexp_aux.
    def exitPexp_aux(self, ctx:MiniJavaParser.Pexp_auxContext): 
        if ctx.getChildCount() == 2:
            name = ctx.ID().getText()
            for i in range(self.table):
                if self.table[i].findID(name) != None:
                    if self.table[i].findID(name) != 'class':
                        self.dicionarioTipos[ctx.__hash__()] = self.table[i].findID(name)
                    else:
                        self.dicionarioTipos[ctx.__hash__()] = name
                else:
                    print("Variável'" + name + "'nao encontrada.")
                    linha = ctx.ID().symbol.line
                    coluna = ctx.ID().symbol.column
                    print("Linha: " + str(linha) + " Coluna: "+str(coluna))
                    sys.exit()

        elif ctx.pexp_aux() != None: #se tiver um pexp_aux no final
            if ctx.LPAREN() !=None: #se tiver id. ( params? ) pexp_aux
                funcaoAux = None
                pos = 0
                
                #buscando funcao cujo identificador é ID
                while funcaoAux == None and pos < len(self.table):
                    table_aux = self.table[pos]
                    funcaoAux = table_aux.findFunction(ctx.ID().getText, len(self.table))
                    pos = pos+1
                    
                #funcaoAux é a funcao referente ao ID
                #caso ela tenha sido implementada
                if funcaoAux != None:
                    name_aux = ctx.pexp_aux().getChild(1).getText() #nome do metodo ou id do pexp_aux
                    class_name = funcaoAux.returnType               #tipo do retorno do metodo referente a ID
                    
                    ind = self.findClass(class_name) #indice da classe encontrada do retorno do ID
                    
                    if ind != None:  #se o tipo do retorno for uma classe                              
                        if ctx.pexp_aux().LPAREN() != None:
                            fun = self.table[ind].findFunction(name_aux) #tipo do retorno de pexp_aux
                            if fun != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o método '" + name_aux + "'. ")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                            
                                sys.exit()                                 
                        else:
                            ident = self.table[ind].findID(name_aux) #tipo do retorno de pexp_aux
                            if ident != None :
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o atributo '" + name_aux + "' na classe '" + class_name + "'.")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )
                                sys.exit()
                    else:
                        print("Tipo do retorno do método não é uma classe. Por isso não é possível acessar métodos ou parâmetros")
                        linha = ctx.getChild(0).symbol.line
                        coluna = ctx.getChild(0).symbol.column
                        print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )
                        sys.exit()
                        
                    if ctx.exps() != None: # .id (exps) . pexp_aux
                        #verificação do tipo dos parametros passados para a funcao
                        listParametros =  funcaoAux.getParamsList()
                        tamList = len(listParametros)
                        paramsRecebidos = self.dicionarioTipos[ctx.exps().__hash__()]
                        tamParamsRecebidos = len(paramsRecebidos)

                        # Verifica se os parametros passados para uma função são 
                        # compativeis com os tipos dos parametros que a funcao recebe    
                        if tamParamsRecebidos == tamList:                        
                            for i in range(tamList):
                                param_a = listParametros[i]
                                param_b = paramsRecebidos[i]
                                if param_a != param_b and not(self.ehSubtipo(param_b, param_a)):
                                    print("Parametro '" + ctx.exps().exp(i).getText() + "'' passado pra função' " + funcaoAux.name + "'' não é do tipo " + paramsRecebidos[i] +".")
                                    linha = ctx.getChild(0).symbol.line
                                    coluna = ctx.getChild(0).symbol.column
                                    print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                            
                        else:
                            print("Numero de parametros passados para a função '" + funcaoAux.name + "' é incompativel.")
                            linha = ctx.getChild(0).symbol.line
                            coluna = ctx.getChild(0).symbol.column
                            print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                          
                else:
                    print("Não existe '" + ctx.pexp_aux().getChild(1).getText() + "' em '" + ctx.ID().getText() + "'.")
                    sys.exit()
                      
            else: #.id . pexp_aux
                for i in range(len(self.table)):
                    if(ctx.ID().getText() == self.table[i].name[0]):
                        if(ctx.pexp_aux().LPAREN() != None ):
                            funcaoAux = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(), len(self.table))
                            if funcaoAux != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o método usado")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )                            
                                sys.exit()
                            break
                        else:
                            idAux = self.table[i].findID(ctx.pexp_aux().getChild(1).getText())
                            if idAux != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o identificador usado")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + ", coluna " + str(coluna) +" ." )                            
                                sys.exit()
                            break
                        
        #caso seja .id(params?)                            
        else:
            funcaoAux = None
            pos = 0
            
            #buscando funcao cujo identificador é ID
            while funcaoAux == None and pos < len(self.table):
                table_aux = self.table[pos]
                funcaoAux = table_aux.findFunction(ctx.ID().getText(), len(self.table))
                pos = pos+1
    
            if funcaoAux != None:
                self.dicionarioTipos[ctx.__hash__()] = funcaoAux.returnType
                if ctx.exps() != None:  #.id(exps)
                                        #verificação do tipo dos parametros passados para a funcao
                    listParametros =  funcaoAux.getParamsList()
                    tamList = len(listParametros)
                    paramsRecebidos = self.dicionarioTipos[ctx.exps().__hash__()]
                    tamParamsRecebidos = len(paramsRecebidos)
                
                    # Verifica se os parametros passados para uma função são 
                    # compativeis com os tipos dos parametros que a funcao recebe    
                    if tamParamsRecebidos == tamList:                        
                        for i in range(tamList):
                            param_a = listParametros[i]
                            param_b = paramsRecebidos[i]
                            if param_a != param_b and not(self.ehSubtipo(param_b, param_a)):
                                print("Parametro '" + ctx.exps().exp(i).getText() + "'' passado pra função' " + funcaoAux.name + "'' não é do tipo " + param_a +".")
                                linha = ctx.getChild(0).symbol.line
                                coluna = ctx.getChild(0).symbol.column
                                print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                            
                    else:
                        print("Numero de parametros passados para a função '" + funcaoAux.name + "' é incompativel.")
                        linha = ctx.getChild(0).symbol.line
                        coluna = ctx.getChild(0).symbol.column
                        print("Erro na linha "+ str(linha) + " coluna " + str(coluna) +" ." )                          

            else:
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print(ctx.ID().getText())
                print("Função '" + ctx.ID.getText() + "' não encontrada")
                print("linha: " + str(linha) + " coluna: "+str(coluna))
                sys.exit()        

    # Exit a parse tree produced by MiniJavaParser#exps.
    def exitExps(self, ctx:MiniJavaParser.ExpsContext):
        tamExps = ctx.getChildCount() + 1
        tamExps = int(tamExps/2)
        lista = []
        for i in range(tamExps):
            lista.append(self.dicionarioTipos[ctx.exp(i).__hash__()])
        self.dicionarioTipos[ctx.__hash__()] = lista            
    
    def findClass(self, name):
        for i in range(self.table):
            if self.table[i].name[0] == name:
                return i
        return None