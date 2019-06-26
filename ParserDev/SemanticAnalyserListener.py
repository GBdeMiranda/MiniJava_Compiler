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

class VerificaTipoListener(MiniJavaListener):
    
    def __init__(self,table):
        self.table = table #lista com as tabelas de cada classe.
        self.tableAtual = self.table[0]
        self.rodada = 0
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
        self.iterador = self.iterador+1
        self.tableAtual = self.table[self.iterador]

    # Exit a parse tree produced by MiniJavaParser#classDecl.
    def exitClassDecl(self, ctx:MiniJavaParser.ClassDeclContext):
        self.iteradorMetodo = 0

    # Enter a parse tree produced by MiniJavaParser#var.
    def enterVar(self, ctx:MiniJavaParser.VarContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#var.
    def exitVar(self, ctx:MiniJavaParser.VarContext):
        pass

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
                print("Erro na linha "+ linha +", coluna " + coluna +" ." )
                sys.exit()
        else:
            if not self.ehSubtipo(returnType, self.funcAtual.returnType):
                print("Retorno diferente do tipo da função")
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print("Erro na linha "+ linha +", coluna " + coluna +" ." )
                sys.exit()
        self.tableAtual = self.tableAtual.previous

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
        tipo = self.dicionarioTipos[ctx.exp().__hash__()]
        if(tipo != 'boolean'):
            print("Expressão do condicional deve ser boolean.")
            linha = ctx.LPAREN().symbol.line
            coluna = ctx.LPAREN().symbol.column
            print("Erro na linha "+ str(linha) +", coluna " + str(coluna) +" ." )
                    
    # Enter a parse tree produced by MiniJavaParser#whileStatement.
    def enterWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#whileStatement.
    def exitWhileStatement(self, ctx:MiniJavaParser.WhileStatementContext):
        aux = ctx.exp()
        tipo = self.dicionarioTipos[aux.__hash__()]
        if(tipo != 'boolean'):
            print("Expressão do condicional deve ser boolean.")
            linha = ctx.exp().symbol.line
            coluna = ctx.exp().symbol.column
            print("Erro na linha "+ linha +", coluna " + coluna +" ." )
            
    # Enter a parse tree produced by MiniJavaParser#printStatement.
    def enterPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#printStatement.
    def exitPrintStatement(self, ctx:MiniJavaParser.PrintStatementContext):
        tipo = self.dicionarioTipos[ctx.exp().__hash__()]
        #verifica se o tipo do argumento do system.out.println é inteiro
        if tipo != 'int':
            print("\nO argumento para a impressão deve ser do tipo 'int'")
            linha = ctx.exp().symbol.line
            coluna = ctx.exp().symbol.column
            print("Erro na linha "+ linha +", coluna " + coluna +" .\n" )

    # Enter a parse tree produced by MiniJavaParser#variableAssignmentStatement.
    def enterVariableAssignmentStatement(self, ctx:MiniJavaParser.VariableAssignmentStatementContext):
        pass
        
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
                    print("Erro na linha "+ linha +", coluna " + coluna +" ." )
            else:
                if tipo2 != 'null' and not(self.ehSubtipo(tipo2, name)) :
                    print("Erro na atribuição pois as variaveis são de tipos diferentes!")
                    linha = ctx.ID().symbol.line
                    coluna = ctx.ID().symbol.column
                    print("Erro na linha "+ linha +", coluna " + coluna +" ." )
                   
                    
    # Enter a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def enterArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        pass


    # Exit a parse tree produced by MiniJavaParser#arrayAssignmentStatement.
    def exitArrayAssignmentStatement(self, ctx:MiniJavaParser.ArrayAssignmentStatementContext):
        tipo_argumento = self.dicionarioTipos[ctx.exp(0).__hash__()]
        if tipo_argumento != 'int':
            print("A posição do array não é Inteiro.")
            linha = ctx.exp(0).symbol.line
            coluna = ctx.exp(0).symbol.column
            print("Erro na linha "+ linha +", coluna " + coluna +" ." )
                    
        name = ctx.ID().getText()
        tipo_id = self.tableAtual.find(name)

        if tipo_id == None:
            print("Variavel '" + name + "' não declarada!")
            linha = ctx.ID().symbol.line
            coluna = ctx.ID().symbol.column
            print("Erro na linha "+ linha +", coluna " + coluna +" ." )
                            
        if tipo_id != 'int[]':
            print("Variavel não é do tipo int[]")
            linha = ctx.ID().symbol.line
            coluna = ctx.ID().symbol.column
            print("Erro na linha "+ linha +", coluna " + coluna +" ." )
        
        tipo_attr = self.dicionarioTipos[ctx.exp(1).__hash__()]
        if tipo_attr != 'int':
            print("tipo de atribuição não é inteiro")
            linha = ctx.exp(1).symbol.line
            coluna = ctx.exp(1).symbol.column
            print("Erro na linha "+ linha +", coluna " + coluna +" ." )        

    # Enter a parse tree produced by MiniJavaParser#exp.
    def enterExp(self, ctx:MiniJavaParser.ExpContext):
        pass

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
        

    # Enter a parse tree produced by MiniJavaParser#exp_aux.
    def enterExp_aux(self, ctx:MiniJavaParser.Exp_auxContext):
        pass

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
                  

    # Enter a parse tree produced by MiniJavaParser#rexp.
    def enterRexp(self, ctx:MiniJavaParser.RexpContext):
        pass 

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
                        print("Não é possível comparar '" + tipo_l + "'s com o operador '" + operador + "'.)
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


    # Enter a parse tree produced by MiniJavaParser#rexp_aux.
    def enterRexp_aux(self, ctx:MiniJavaParser.Rexp_auxContext):
        pass

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


    # Enter a parse tree produced by MiniJavaParser#aexp.
    def enterAexp(self, ctx:MiniJavaParser.AexpContext):
        pass
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
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'
            

    # Enter a parse tree produced by MiniJavaParser#aexp_aux.
    def enterAexp_aux(self, ctx:MiniJavaParser.Aexp_auxContext):
        pass

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
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'


    # Enter a parse tree produced by MiniJavaParser#mexp.
    def enterMexp(self, ctx:MiniJavaParser.MexpContext):
        pass

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



    # Enter a parse tree produced by MiniJavaParser#mexp_aux.
    def enterMexp_aux(self, ctx:MiniJavaParser.Mexp_auxContext):
        pass

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
                print("Erro na linha "+ linha +", coluna " + coluna +" ." )
                self.dicionarioTipos[ctx.__hash__()] = 'int'


    # Enter a parse tree produced by MiniJavaParser#sexp.
    def enterSexp(self, ctx:MiniJavaParser.SexpContext):
        pass

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
                self.dicionarioTipos[ctx.__hash__()]  = self.dicionarioTipos[ctx.pexp(0).__hash__()]                
        elif ctx.getChildCount() == 2:
            tipo_d = self.dicionarioTipos[ctx.sexp().__hash__()]  
            if ctx.NOT() != None:
                if tipo_d == 'boolean':
                    self.dicionarioTipos[ctx.__hash__()]  = 'boolean'
                else:
                    print("Erro ao tentar aplicar o operador 'NOT' em uma variável do tipo '" + tipo_d + "'! ")
                    linha = ctx.getChild(0).symbol.line
                    coluna = ctx.getChild(0).symbol.column
                    print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
                    sys.exit()
            elif tipo_d == 'int':
                self.dicionarioTipos[ctx.__hash__()] = 'int'    
            else:
                print("Erro ao tentar aplicar operador '-' em uma variável do tipo '" + tipo_d + "'! ")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
                sys.exit()
        elif ctx.getChildCount() == 3:
            tipo_d = self.dicionarioTipos[ctx.pexp().__hash__()]
            if tipo_d != 'int[]':
                print("Não é possível aplicar o método length em uma variável do tipo '" + tipo_d+ "'!")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
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
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )        
            if tipo_pexp != 'int[]':
                print("A variável não é um vetor.")
                linha = ctx.getChild(0).symbol.line
                coluna = ctx.getChild(0).symbol.column
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
            self.dicionarioTipos[ctx.__hash__()] = 'int'
        else:
            tipo_exp = self.dicionarioTipos[ctx.exp().__hash__()]
            if tipo_exp != 'int':
                print("O tamanho de um vetor deve ser um número inteiro")
                linha = ctx.LBRACKET().symbol.line
                coluna = ctx.LBRACKET().symbol.column
                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )
            self.dicionarioTipos[ctx.__hash__()] = 'int[]'
                
    # Enter a parse tree produced by MiniJavaParser#pexp.
    def enterPexp(self, ctx:MiniJavaParser.PexpContext):
        pass

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
                    print("Erro na linha "+ linha +", coluna " + coluna + ". " )
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
                                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )                            
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
                                print("Erro na linha "+ linha + ", coluna " + coluna +" ." )                            
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
                        print("Erro na linha "+ linha + ", coluna " + coluna +" ." )        
                        sys.exit()
                else:
                    idAux = tipo_classe.findID(ctx.pexp_aux().getChild(1).getText())
                    if idAux != None:
                        self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                    else: 
                        print("Não existe a variavel '" + ctx.pexp_aux().getChild(1).getText() + "'.")
                        linha = ctx.getChild(0).symbol.line
                        coluna = ctx.getChild(0).symbol.column
                        print("Erro na linha "+ linha + ", coluna " + coluna +" ." )        
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
                print("Erro na linha "+ linha + ", coluna " + coluna +". " )
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
                                print("Erro na linha "+ linha + " coluna " + coluna +" ." )                            
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
                            print("Erro na linha "+ linha + " coluna " + coluna +" ." )                            
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
                            print("Erro na linha "+ linha + " coluna " + coluna +" ." )                            
                            sys.exit()
                        break
                        

    # Enter a parse tree produced by MiniJavaParser#pexp_aux.
    def enterPexp_aux(self, ctx:MiniJavaParser.Pexp_auxContext):
        pass

    # Exit a parse tree produced by MiniJavaParser#pexp_aux.
    def exitPexp_aux(self, ctx:MiniJavaParser.Pexp_auxContext): 
        if ctx.getChildCount() == 2:
            self.dicionarioTipos[ctx.__hash__()] = ctx.getChild(1).getText()    
    
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
                                sys.exit()                                 
                        else:
                            ident = self.table[ind].findID(name_aux) #tipo do retorno de pexp_aux
                            if ident != None :
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o atributo '" + name_aux + "' na classe '" + class_name + "'.")
                    else:
                        print("Tipo do retorno do método não é uma classe. Por isso não é possível acessar métodos ou parâmetros")
                    
                    if ctx.exps() != None: # .id (exps) . pexp_aux
                        #verificação do tipo dos parametros passados para a funcao
                        listParametros =  funcaoAux.getParamsList()
                        tamList = len(listParametros)
                        paramsRecebidos = self.dicionarioTipos[ctx.exps().__hash__()]
                        tamParamsRecebidos = len(paramsRecebidos)
    
                        if tamParamsRecebidos == tamList:                        
                            for i in range(tamList):
                                if listParametros[i] != paramsRecebidos[i]:
                                    print("Parametro '" + ctx.exps().exp(i).getText() + "'' passado pra função' " + funcaoAux.name + "'' não é do tipo " + paramsRecebidos[i] +".")                        
                                #falta verificar caso o tipo da parada seja subtipo da outra                        
                        else:
                            print("Numero de parametros passados para a função '" + funcaoAux.name + "' é incompativel.")
    
                else:
                    print("não existe '" + ctx.pexp_aux().getChild(1).getText() + "' em '" + ctx.ID().getText() + "'.")
                    sys.exit()
                      
            else: #.id . pexp_aux
                for i in range(len(self.table)):
                    name_aux = ctx.pexp_aux().getChild(1).getText()
                    if(ctx.ID().getText() == self.table[i].name[0]):
                        if ctx.pexp_aux().LPAREN() != None:
                            fun = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(),len(self.table)) #tipo do retorno de pexp_aux
                            if fun != None:
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o metodo '" + name_aux + "'. ")
                                sys.exit()                                 
                        else:
                            ident = self.table[i].findID(name_aux) #tipo do retorno de pexp_aux
                            if ident != None :
                                self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                            else:
                                print("Não existe o atributo '" + name_aux + "' na classe '" + class_name + "'.")
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
    
                    if tamParamsRecebidos == tamList:
                        for i in range(tamList):
                            if listParametros[i] != paramsRecebidos[i]:
                                print("Parametro '" + ctx.exps().exp(i).getText() + "'' passado pra função' " + funcaoAux.name + "'' não é do tipo " + paramsRecebidos[i] +".")                        
                            #falta verificar caso o tipo da parada seja subtipo da outra
                    else:
                        print("Numero de parametros passados para a função '" + funcaoAux.name + "' é incompativel.")
            else:
                linha = ctx.ID().symbol.line
                coluna = ctx.ID().symbol.column
                print(ctx.ID().getText())
                print("Erro!!! pexp_aux")
                print("linha: " + str(linha) + " coluna: "+str(coluna))
                sys.exit()        

    # Enter a parse tree produced by MiniJavaParser#exps.
    def enterExps(self, ctx:MiniJavaParser.ExpsContext):
        pass

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