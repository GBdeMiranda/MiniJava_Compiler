"""
Created on Wed May 25 13:38:50 2019

@author: Gabriel Brandao de Miranda     - 201565514B
         Vitor Monteiro Andrade Goulart - 201665511B
"""
from antlr4 import *
from MiniJavaLexer import MiniJavaLexer
from MiniJavaParser import MiniJavaParser
from MiniJavaListener import MiniJavaListener
from MiniJavaBaseListener import MiniJavaBaseListener
from CompleteSymbolTableListener import CompleteSymbolTableListener

import sys

def main( text ):
    lexer = MiniJavaLexer( text ) # Get our lexer 
    token_stream = CommonTokenStream(lexer) # Get a list of matched tokens

    return MiniJavaParser(token_stream) # Pass the tokens to the parser

if __name__ == '__main__':
#    if len(sys.argv) > 1:
#        input_stream = FileStream(sys.argv[1])
#    else:
#        print("Insert the file content: ")
#        input_stream = InputStream(sys.stdin.readline())'
    input_stream = FileStream("Teste.java")
    parser = main( input_stream )
#    parser.buildParseTrees = True
    tree = parser.program()
    
    if parser.getNumberOfSyntaxErrors() <= 0:
        print( "NO LANGUAGE ERRORS FOUND! \n " )
#        print( tree.toStringTree(recog=parser) )
    else:
        print( "SYNTAX ERROR! \n " )
        
    listenerStat = CompleteSymbolTableListener()
    walker = ParseTreeWalker()
    walker.walk(listenerStat,tree)