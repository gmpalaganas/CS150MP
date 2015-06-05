from puto.lexer import runLexer
from puto.interpreter import interpret
from puto.parser import runParser
import sys

def main():
    #print runParser(sys.argv[1])
    ast = runParser(sys.argv[1])
    interpret(ast) 

if __name__ == "__main__":
    main()
