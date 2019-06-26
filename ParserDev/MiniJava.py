"""
Created on Wed Jun 19 13:38:50 2019

@author: Gabriel Brandao de Miranda     - 201565514B
         Vitor Monteiro Andrade Goulart - 201665511B
"""
from antlr4 import *
from MiniJavaLexer import MiniJavaLexer
from MiniJavaParser import MiniJavaParser
from CompleteSymbolTableListener import CompleteSymbolTableListener
from CompleteClassSymbolTableListener import CompleteClassSymbolTableListener
from SemanticAnalyserListener import SemanticAnalyserListener

import sys

if __name__ == '__main__':
#    if len(sys.argv) > 1:
#        input_stream = FileStream(sys.argv[1])
#    else:
#        print("Insert the file content: ")
#        input_stream = InputStream(sys.stdin.readline())
    input_stream = FileStream("Teste.java")
    lexer = MiniJavaLexer( input_stream )   
    token_stream = CommonTokenStream(lexer) 
    parser = MiniJavaParser(token_stream)
    tree = parser.program() #constroi a arvore de derivação
    
    #Se a analise sintática for bem sucedida, será feita a análise Semantica
    if parser.getNumberOfSyntaxErrors() <= 0:
        #Percorre as classes e insere elas na tabela de simbolos
        semanticClass = CompleteClassSymbolTableListener()        
        walker = ParseTreeWalker()
        walker.walk(semanticClass, tree)
        
        #preenche a tabela de simbolos
        tabela = semanticClass.table
        semanticSymbolTable = CompleteSymbolTableListener(tabela)
        walker.walk(semanticSymbolTable, tree)
        
        #Faz a analise semantica
        tabela = semanticSymbolTable.table
        semanticAnalysis = SemanticAnalyserListener(tabela)
        walker.walk(semanticAnalysis,tree)

    else:
        print( "SYNTAX ERROR! \n " )
        